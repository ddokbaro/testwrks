"""[Stage 1] 청와대 국민청원 원본 자동 수집 및 1차 아카이빙 (Raw Data & Provenance)

1차 원천 lovit/petitions_archive(GitHub)의 월별 JSONL을 고정 커밋에서 바이트 그대로 보존하고,
파일별 SHA-256, 품질 점검, RO-Crate 1.1 메타데이터를 함께 기록한다.

수록 범위: 2017-08-25 ~ 2019-08-30 청원종료 건 436,660건 (2019-09 이후 미수록).
Hugging Face heegyu/korean-petitions 는 이 원천의 재직렬화 사본이며, content 에서
"[본 게시물의 일부 내용이 ... 관리자에 의해 수정되었습니다]" 고지문과 replies 필드가
제거되어 있으므로 원본으로 쓰지 않는다. --compare-hf 로 차이를 기록할 수 있다.

사용법
  python stage1_collect_and_archive_raw.py --collector "김바로 (한국학중앙연구원)"
  python stage1_collect_and_archive_raw.py --compare-hf
"""

import argparse
import hashlib
import json
import platform
import sys
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

GH_REPO = "lovit/petitions_archive"
GH_COMMIT = "03dc3f3d69e03a0a4885350c6991e328fc0a6b81"
GH_RAW_BASE = f"https://raw.githubusercontent.com/{GH_REPO}/{GH_COMMIT}"

HF_REPO = "heegyu/korean-petitions"
HF_COMMIT = "02d8400506fe656bfd6016d3a8424e33f1b28916"
HF_RAW_BASE = f"https://huggingface.co/datasets/{HF_REPO}/resolve/{HF_COMMIT}/data"

EXPECTED_RECORDS = 436_660
MODERATION_NOTICE = "[본 게시물의 일부 내용이 국민 청원 요건에 위배되어 관리자에 의해 수정되었습니다]"
CORE_FIELDS = ["petition_idx", "category", "begin", "end", "num_agree", "status", "title", "content"]
KST = ZoneInfo("Asia/Seoul")

PARQUET_SCHEMA = pa.schema(
    [
        ("petition_idx", pa.int64()),
        ("category", pa.string()),
        ("begin", pa.date32()),
        ("end", pa.date32()),
        ("num_agree", pa.int64()),
        ("status", pa.string()),
        ("title", pa.string()),
        ("content", pa.string()),
        ("replies", pa.list_(pa.string())),
        ("is_moderated", pa.bool_()),
        ("source_file", pa.string()),
    ]
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def download(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as resp, tmp.open("wb") as out:
        expected = resp.headers.get("Content-Length")
        while chunk := resp.read(1 << 20):
            out.write(chunk)
    if expected is not None and tmp.stat().st_size != int(expected):
        tmp.unlink()
        raise IOError(f"{url}: 크기 불일치 (기대 {expected}, 수신 {tmp.stat().st_size})")
    tmp.replace(dest)


def fetch_month_list() -> list[str]:
    with urllib.request.urlopen(f"{GH_RAW_BASE}/files", timeout=60) as resp:
        return [line.strip() for line in resp.read().decode("utf-8").splitlines() if line.strip()]


def collect_raw(raw_dir: Path) -> list[dict]:
    manifest = []
    for name in fetch_month_list():
        local = raw_dir / f"{name}.jsonl"
        url = f"{GH_RAW_BASE}/{name}"
        if not local.exists():
            download(url, local)
        records = read_jsonl(local)
        manifest.append(
            {
                "file": local.name,
                "source_url": url,
                "bytes": local.stat().st_size,
                "records": len(records),
                "sha256": sha256_file(local),
            }
        )
        print(f"  {local.name}: {len(records):,}건")
    return manifest


def build_dataframe(raw_dir: Path, manifest: list[dict]) -> pd.DataFrame:
    frames = []
    for entry in manifest:
        df = pd.DataFrame(read_jsonl(raw_dir / entry["file"]))
        missing = set(CORE_FIELDS) - set(df.columns)
        if missing:
            raise ValueError(f"{entry['file']}: 필수 필드 누락 {missing}")
        if "replies" not in df.columns:
            df["replies"] = None
        df["source_file"] = entry["file"]
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    df["petition_idx"] = df["petition_idx"].astype("int64")
    df["begin"] = pd.to_datetime(df["begin"], format="%Y-%m-%d").dt.date
    df["end"] = pd.to_datetime(df["end"], format="%Y-%m-%d").dt.date
    df["num_agree"] = df["num_agree"].astype("int64")
    df["is_moderated"] = df["content"].fillna("").str.contains(MODERATION_NOTICE, regex=False)
    return df.reindex(columns=[f.name for f in PARQUET_SCHEMA])


def quality_report(df: pd.DataFrame) -> dict:
    def blank(col: str) -> pd.Series:
        return df[col].fillna("").str.strip().eq("")

    return {
        "total_records": int(len(df)),
        "expected_records": EXPECTED_RECORDS,
        "matches_expected": int(len(df)) == EXPECTED_RECORDS,
        "duplicate_petition_idx": int(df["petition_idx"].duplicated().sum()),
        "begin_min": str(df["begin"].min()),
        "begin_max": str(df["begin"].max()),
        "end_max": str(df["end"].max()),
        "null_counts": {c: int(v) for c, v in df.drop(columns="replies").isna().sum().items()},
        "empty_title": int(blank("title").sum()),
        "empty_content": int(blank("content").sum()),
        "end_before_begin": int((df["end"] < df["begin"]).to_numpy().sum()),
        "records_with_replies": int(df["replies"].notna().to_numpy().sum()),
        "records_moderated": int(df["is_moderated"].to_numpy().sum()),
        "status_counts": {k: int(v) for k, v in df["status"].value_counts().items()},
        "category_counts": {k: int(v) for k, v in df["category"].value_counts().items()},
    }


def compare_with_hf(raw_dir: Path, manifest: list[dict], work_dir: Path) -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)
    per_file = []
    for entry in manifest:
        hf_path = work_dir / entry["file"]
        download(f"{HF_RAW_BASE}/{entry['file']}", hf_path)
        origin = {r["petition_idx"]: r for r in read_jsonl(raw_dir / entry["file"])}
        mirror = {r["petition_idx"]: r for r in read_jsonl(hf_path)}

        diff_fields: Counter = Counter()
        unexplained = []
        for idx in origin.keys() & mirror.keys():
            o, m = origin[idx], mirror[idx]
            for field in CORE_FIELDS:
                if o.get(field) == m.get(field):
                    continue
                diff_fields[field] += 1
                if field != "content" or o["content"].replace(MODERATION_NOTICE, "") != m["content"]:
                    unexplained.append(idx)
        per_file.append(
            {
                "file": entry["file"],
                "mirror_sha256": sha256_file(hf_path),
                "only_in_origin": len(origin.keys() - mirror.keys()),
                "only_in_mirror": len(mirror.keys() - origin.keys()),
                "differing_fields": dict(diff_fields),
                "unexplained_diff_petition_idx": unexplained,
            }
        )
        hf_path.unlink()
        print(f"  {entry['file']}: 필드 차이 {dict(diff_fields) or 0}, 설명불가 {len(unexplained)}")
    work_dir.rmdir()

    unexplained_total = sum(len(f["unexplained_diff_petition_idx"]) for f in per_file)
    membership_equal = all(f["only_in_origin"] == 0 and f["only_in_mirror"] == 0 for f in per_file)
    return {
        "mirror": f"https://huggingface.co/datasets/{HF_REPO}",
        "mirror_commit": HF_COMMIT,
        "same_petition_set": membership_equal,
        "content_diffs_total": sum(f["differing_fields"].get("content", 0) for f in per_file),
        "unexplained_diffs_total": unexplained_total,
        "conclusion": (
            "미러는 원천에서 관리자 수정 고지문과 replies 필드를 제거한 사본"
            if membership_equal and unexplained_total == 0
            else "설명되지 않는 차이 존재 - files 항목 확인 필요"
        ),
        "files": per_file,
    }


def write_ro_crate(archive_dir: Path, meta: dict) -> None:
    raw_entities = [
        {
            "@id": f"raw_jsonl/{m['file']}",
            "@type": "File",
            "encodingFormat": "application/jsonl",
            "contentSize": str(m["bytes"]),
            "sha256": m["sha256"],
            "contentUrl": m["source_url"],
        }
        for m in meta["raw_files"]
    ]
    parquet = meta["derived_parquet"]
    crate = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@id": "ro-crate-metadata.json",
                "@type": "CreativeWork",
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
                "about": {"@id": "./"},
            },
            {
                "@id": "./",
                "@type": "Dataset",
                "name": meta["dataset_title"],
                "description": meta["description"],
                "datePublished": meta["collected_at_kst"][:10],
                "temporalCoverage": f"{meta['coverage']['begin_min']}/{meta['coverage']['begin_max']}",
                "isBasedOn": {"@id": meta["source"]["url"]},
                "author": {"@id": "#collector"},
                "hasPart": [{"@id": parquet["file"]}, {"@id": "stage1_raw_provenance.json"}]
                + [{"@id": e["@id"]} for e in raw_entities],
            },
            {"@id": "#collector", "@type": "Person", "name": meta["collector"]},
            {
                "@id": meta["source"]["url"],
                "@type": "SoftwareSourceCode",
                "name": GH_REPO,
                "version": GH_COMMIT,
            },
            {
                "@id": parquet["file"],
                "@type": "File",
                "encodingFormat": "application/vnd.apache.parquet",
                "sha256": parquet["sha256"],
                "description": "raw_jsonl 전체를 명시적 스키마로 병합한 분석용 파생본",
            },
            {"@id": "stage1_raw_provenance.json", "@type": "File", "encodingFormat": "application/json"},
            *raw_entities,
        ],
    }
    with (archive_dir / "ro-crate-metadata.json").open("w", encoding="utf-8") as f:
        json.dump(crate, f, ensure_ascii=False, indent=2)


def collect_and_archive_raw(archive_dir: Path, collector: str, compare_hf: bool) -> None:
    raw_dir = archive_dir / "raw_jsonl"
    raw_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(KST)

    print(f"[Stage 1] {GH_REPO}@{GH_COMMIT[:8]} 원본 수집...")
    manifest = collect_raw(raw_dir)

    print("[Stage 1] 병합 및 품질 점검...")
    df = build_dataframe(raw_dir, manifest)
    quality = quality_report(df)
    if quality["duplicate_petition_idx"]:
        raise ValueError(f"petition_idx 중복 {quality['duplicate_petition_idx']}건")
    if not quality["matches_expected"]:
        print(f"  [경고] 레코드 수 {len(df):,} ≠ 기대값 {EXPECTED_RECORDS:,}")

    parquet_path = archive_dir / "cheongwadae_petitions_2017-08_2019-08.parquet"
    pq.write_table(
        pa.Table.from_pandas(df, schema=PARQUET_SCHEMA, preserve_index=False),
        parquet_path,
        compression="zstd",
    )

    mirror_check = "skipped (--compare-hf 미지정)"
    if compare_hf:
        print(f"[Stage 1] {HF_REPO}@{HF_COMMIT[:8]} 미러와 대조...")
        mirror_check = compare_with_hf(raw_dir, manifest, archive_dir / "_hf_tmp")

    meta = {
        "dataset_title": "Cheong Wa Dae National Petitions Raw Corpus (2017-08 – 2019-08)",
        "description": (
            "청와대 국민청원 게시판의 청원종료 청원(제목·본문·분류·동의수, 일부 replies 포함). "
            "lovit/petitions_archive 월별 수집본을 바이트 단위로 보존. 2019-09 이후 청원은 미수록."
        ),
        "collector": collector,
        "collected_at_kst": started.isoformat(timespec="seconds"),
        "finished_at_kst": datetime.now(KST).isoformat(timespec="seconds"),
        "source": {
            "url": f"https://github.com/{GH_REPO}",
            "commit": GH_COMMIT,
            "original_platform": "https://www1.president.go.kr/petitions (현재 폐쇄)",
            "license": "명시 없음 (NOASSERTION)",
        },
        "rights_note": (
            "청원 본문의 저작권은 각 청원인에게 있을 수 있음. 원천 저장소에 라이선스가 없으므로 "
            "재배포 시 저작권법상 공정이용 범위와 개인정보 포함 여부를 검토할 것."
        ),
        "coverage": {
            "begin_min": quality["begin_min"],
            "begin_max": quality["begin_max"],
            "note": (
                "청와대 국민청원 운영기간(2017-08-17 ~ 2022-05-09) 중 일부. "
                "2019-04 이후 월별 건수가 급감(수백 건)하므로 시계열 분석 시 수집 편향 유의."
            ),
        },
        "raw_files": manifest,
        "derived_parquet": {
            "file": parquet_path.name,
            "sha256": sha256_file(parquet_path),
            "schema": {f.name: str(f.type) for f in PARQUET_SCHEMA},
            "note": (
                "is_moderated, source_file 은 파생 컬럼. 무결성 기준은 raw_files 해시이며 "
                "parquet 해시는 라이브러리 버전에 따라 달라질 수 있음."
            ),
        },
        "quality_report": quality,
        "mirror_comparison": mirror_check,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "pandas": pd.__version__,
            "pyarrow": pa.__version__,
        },
        "metadata_standard": "RO-Crate 1.1 (ro-crate-metadata.json)",
    }

    with (archive_dir / "stage1_raw_provenance.json").open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    write_ro_crate(archive_dir, meta)

    print(
        f"[완료] {len(df):,}건 ({quality['begin_min']} ~ {quality['begin_max']}), "
        f"관리자 수정 {quality['records_moderated']:,}건, replies 보유 {quality['records_with_replies']:,}건\n"
        f"  메타데이터: {archive_dir / 'stage1_raw_provenance.json'}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--archive-dir", type=Path, default=Path("./archive_01_raw_petitions"))
    parser.add_argument("--collector", default="Kim Baro (Academy of Korean Studies)")
    parser.add_argument("--compare-hf", action="store_true", help="Hugging Face 미러와 레코드 단위 대조 결과를 기록")
    args = parser.parse_args()
    collect_and_archive_raw(args.archive_dir, args.collector, args.compare_hf)


if __name__ == "__main__":
    main()
