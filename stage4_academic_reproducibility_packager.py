"""[Stage 4] 학술적 재현성 보존 패키지 (Academic Reproducibility Package)

Stage 1~3 스크립트, 사전, 주석 파일, 각 단계 provenance, 분석 결과와 그림, 실행 환경,
생성형 AI 사용 기록을 모아 단일 ZIP 번들과 RO-Crate 1.1 메타데이터로 보존한다.

원칙
  - 파라데이터에는 이 저장소에서 실제로 실행·검증된 사실만 기록한다.
    추정한 모델명, 사용하지 않은 도구, 실행하지 않은 단계는 쓰지 않는다.
  - 웍스AI 에이전트 라벨링처럼 아직 실행하지 않은 단계는 status="pending" 으로 남긴다.
  - 저작권·개인정보를 이유로 원문 코퍼스(원본 JSONL, 본문 포함 parquet)는 번들에서 제외한다.
    대신 원천 URL·커밋·SHA-256으로 재수집해 검증할 수 있게 한다.

산출: archive_04_academic_preservation/
  KADH_Academic_Paradata_Manifest.json
  ro-crate-metadata.json
  <YYYYMMDD>_CheongWaDae_CrossCatalysis_Reproducible_Package.zip
"""

import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from datetime import datetime
from importlib import metadata
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "archive_04_academic_preservation"
KST = ZoneInfo("Asia/Seoul")

BUNDLE_GLOBS = [
    "stage1_collect_and_archive_raw.py",
    "stage2_preprocess_and_tag.py",
    "stage2b_validate_rules.py",
    "stage3_kinetic_analysis.py",
    "stage4_academic_reproducibility_packager.py",
    "requirements.txt",
    "README.md",
    "lexicon/*.json",
    "annotation/*.csv",
    "annotation/*.md",
    "annotation/*.json",
    "archive_01_raw_petitions/stage1_raw_provenance.json",
    "archive_01_raw_petitions/ro-crate-metadata.json",
    "archive_02_preprocessed/stage2_provenance.json",
    "archive_02_preprocessed/stage2_lexicon_diagnostics.json",
    "archive_02_preprocessed/stage2_monthly_counts.csv",
    "archive_02_preprocessed/stage2_weekly_counts.csv",
    "archive_02_preprocessed/stage2b_rule_validation.json",
    "archive_02_preprocessed/stage2_tagged_full.parquet",
    "archive_03_analysis_outputs/*",
    "paper/*.md",
    "paper/*.docx",
]
EXCLUDED = {
    "archive_01_raw_petitions/raw_jsonl/*": "원문 재배포 제한(원천 무라이선스·청원인 저작권·개인정보). 원천 URL·커밋·SHA-256으로 재수집 검증",
    "archive_01_raw_petitions/*.parquet": "원문 포함 파생본. Stage 1 재실행으로 재생성",
    "archive_02_preprocessed/stage2_preprocessed_substrates.parquet": "원문 포함. Stage 2 재실행으로 재생성",
    "archive_02_preprocessed/stage2_llm_batch_input_strat3000.csv": "원문 포함. Stage 2 재실행으로 재생성",
    "archive_02_preprocessed/stage2_validation_sample.csv": "원문 발췌 포함. 동일 시드로 재생성",
}
PACKAGES = ["pandas", "numpy", "pyarrow", "scipy", "statsmodels", "matplotlib", "python-docx"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str | None:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def collect_files() -> list[Path]:
    files: list[Path] = []
    for pattern in BUNDLE_GLOBS:
        files.extend(p for p in sorted(ROOT.glob(pattern)) if p.is_file())
    seen, unique = set(), []
    for p in files:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def load_json(rel: str) -> dict:
    path = ROOT / rel
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def build_manifest(files: list[Path]) -> dict:
    s1 = load_json("archive_01_raw_petitions/stage1_raw_provenance.json")
    s2 = load_json("archive_02_preprocessed/stage2_provenance.json")
    s2b = load_json("archive_02_preprocessed/stage2b_rule_validation.json")
    s3 = load_json("archive_03_analysis_outputs/stage3_kinetic_results_summary.json")
    llm_log = load_json("annotation/llm_run_log.json")

    versions = {}
    for pkg in PACKAGES:
        try:
            versions[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            versions[pkg] = None

    return {
        "schema_version": "KADH-Reproducibility-1.1",
        "project_title": "혐오 담론의 교차 촉매(Cross-Catalysis)와 중심축 이동: 청와대 국민청원(2017-08~2019-08)의 비선형 동역학 분석",
        "principal_investigator": {
            "name": "김바로 (Kim, Baro)",
            "affiliation": "한국학중앙연구원",
            "orcid": "https://orcid.org/0000-0002-4456-9616",
        },
        "packaged_at_kst": datetime.now(KST).isoformat(timespec="seconds"),
        "repository": {
            "remote": git("remote", "get-url", "origin"),
            "branch": git("symbolic-ref", "--short", "HEAD"),
            "commit": git("rev-parse", "HEAD"),
            "working_tree_dirty": bool(git("status", "--porcelain", "--untracked-files=no")),
        },
        "execution_environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "packages": versions,
        },
        "data_source": s1.get("source"),
        "data_coverage": s1.get("coverage"),
        "pipeline": [
            {"stage": "1 수집·원본 보존", "script": "stage1_collect_and_archive_raw.py", "status": "executed",
             "records": s1.get("quality_report", {}).get("total_records"),
             "started_at_kst": s1.get("collected_at_kst")},
            {"stage": "2 규칙 태깅·복제 탐지", "script": "stage2_preprocess_and_tag.py", "status": "executed",
             "lexicon_version": s2.get("lexicon_version"), "started_at_kst": s2.get("started_at_kst"),
             "summary": s2.get("summary")},
            {"stage": "2b 규칙 타당도 검증", "script": "stage2b_validate_rules.py", "status": "executed",
             "micro_scores": {f: r.get("micro") for f, r in s2b.get("files", {}).items() if "micro" in r}},
            {"stage": "2c 웍스AI LLM 정밀 주석", "prompt": "annotation/wrksai_coder_prompt.md",
             "status": "executed" if llm_log.get("runs") else "pending",
             "note": "웍스AI 에이전트 실행 후 annotation/llm_run_log.json 과 llm_labels_*.csv 를 추가하고 Stage 2b 를 재실행한다."},
            {"stage": "3 동역학 분석", "script": "stage3_kinetic_analysis.py", "status": "executed",
             "started_at_kst": s3.get("analysis_timestamp_kst"), "figures": s3.get("figures")},
            {"stage": "4 보존 패키지", "script": "stage4_academic_reproducibility_packager.py", "status": "executed"},
            {"stage": "5 논문 초안", "file": "paper/manuscript_draft_ko.md", "status": "draft"},
        ],
        "generative_ai_audit_trail": [
            {
                "stages": ["1", "2", "2b", "3", "4", "5"],
                "tool": "Wrks Coding Agent (한국학중앙연구원 웍스AI 코딩 에이전트)",
                "model_name_and_version": "Claude Opus 5.5 (bizrouter/anthropic/claude-opus-5.5)",
                "date": "2026-10-30",
                "role": (
                    "파이프라인 코드 작성·수정 및 실행, 규칙 사전 개정, 검증 표본 180건 1차 주석(AI 보조 라벨), "
                    "통계 결과 요약, 논문 초안 문장 작성"
                ),
                "human_verification_required": [
                    "annotation/validation_*.csv 의 gold_relevant·gold_hostile 라벨 전수 검수",
                    "논문 초안의 해석·인용·서술 전면 검토",
                ],
            },
            {
                "stages": ["2c"],
                "tool": "웍스AI '나만의 에이전트'",
                "model_name_and_version": "미실행 - 실행 시 UI 표시 모델명을 그대로 기록",
                "role": "층화 표본 3,000건 다중 라벨 주석(예정)",
            },
        ],
        "excluded_from_bundle": EXCLUDED,
        "rights": {
            "code": "MIT (저장소 LICENSE 참조)",
            "derived_data_and_figures": "CC BY-NC-ND 4.0 (KADH 제21조 준용)",
            "source_corpus": "원천 저장소 라이선스 없음(NOASSERTION). 원문은 재배포하지 않음",
        },
        "artifact_checksums_sha256": {p.relative_to(ROOT).as_posix(): sha256_file(p) for p in files},
    }


def write_ro_crate(manifest: dict, zip_name: str) -> Path:
    graph = [
        {"@id": "ro-crate-metadata.json", "@type": "CreativeWork",
         "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}, "about": {"@id": "./"}},
        {"@id": "./", "@type": "Dataset", "name": manifest["project_title"],
         "datePublished": manifest["packaged_at_kst"][:10],
         "author": {"@id": manifest["principal_investigator"]["orcid"]},
         "license": {"@id": "https://creativecommons.org/licenses/by-nc-nd/4.0/"},
         "isBasedOn": {"@id": (manifest.get("data_source") or {}).get("url", "")},
         "hasPart": [{"@id": zip_name}, {"@id": "KADH_Academic_Paradata_Manifest.json"}]},
        {"@id": manifest["principal_investigator"]["orcid"], "@type": "Person",
         "name": manifest["principal_investigator"]["name"],
         "affiliation": manifest["principal_investigator"]["affiliation"]},
        {"@id": zip_name, "@type": "File", "encodingFormat": "application/zip",
         "sha256": sha256_file(OUT_DIR / zip_name)},
        {"@id": "KADH_Academic_Paradata_Manifest.json", "@type": "File", "encodingFormat": "application/json"},
        {"@id": "#wrks-coding-agent", "@type": "SoftwareApplication",
         "name": "Wrks Coding Agent (Claude Opus 5.5)", "description": "코드 작성·실행 및 초안 작성 보조"},
    ]
    path = OUT_DIR / "ro-crate-metadata.json"
    path.write_text(json.dumps({"@context": "https://w3id.org/ro/crate/1.1/context", "@graph": graph},
                               ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_academic_bundle() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = collect_files()
    manifest = build_manifest(files)
    manifest_path = OUT_DIR / "KADH_Academic_Paradata_Manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    zip_name = f"{datetime.now(KST):%Y%m%d}_CheongWaDae_CrossCatalysis_Reproducible_Package.zip"
    with zipfile.ZipFile(OUT_DIR / zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(manifest_path, arcname="KADH_Academic_Paradata_Manifest.json")
        for p in files:
            zf.write(p, arcname=p.relative_to(ROOT).as_posix())
    write_ro_crate(manifest, zip_name)
    print(f"[Stage 4 완료] {len(files)}개 파일 → {OUT_DIR / zip_name}")


if __name__ == "__main__":
    build_academic_bundle()
