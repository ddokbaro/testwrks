"""[Stage 2] 전처리 · 5대 기질/4대 리간드 규칙 태깅 · 조직적 복제(복사-붙여넣기) 탐지 · 2차 아카이빙

입력: archive_01_raw_petitions/cheongwadae_petitions_2017-08_2019-08.parquet (Stage 1)
사전: lexicon/lexicon.json (버전 관리되는 외부 사전)

기질 활성화 규칙
  strict(주 분석): 제목에 1회 이상 적중하거나 본문에 STRICT_BODY_MIN 회 이상 적중
  loose(민감도 분석): 제목+본문 어디서든 1회 이상 적중  → 컬럼명 *_loose
  리간드는 loose 기준(청원이 해당 정당화 논리를 '동원'했는가)으로 태깅한다.

산출 (archive_02_preprocessed/)
  stage2_tagged_full.parquet               전 코퍼스 태그(본문 제외, 경량) - 분모 계산용
  stage2_preprocessed_substrates.parquet   기질 1개 이상 서브코퍼스(본문 포함)
  stage2_monthly_counts.csv / stage2_weekly_counts.csv   전체 청원 수(분모)와 기질·리간드별 건수
  stage2_lexicon_diagnostics.json          사전 어휘별 적중 수, 기질-리간드 사전 중복 점검
  stage2_llm_batch_input_strat3000.csv     웍스AI LLM 정밀 주석용 층화 표본(기질×동의수 구간)
  stage2_validation_sample.csv             규칙 타당도 검증용 소표본(기질별 16 + 비해당 20)
  stage2_provenance.json                   입력·사전·산출 SHA-256 및 처리 파라미터

복제 탐지 정의
  본문에서 한글·영문·숫자 이외 문자를 제거한 정규형을 만든 뒤,
  (a) 정규형 전체가 같은 청원, (b) 정규형 앞 PREFIX_LEN 자가 같은 청원(정규형 길이 ≥ PREFIX_LEN)을
  전 코퍼스(436,660건) 기준으로 묶는다. 클러스터 크기 ≥ CLONE_MIN 이면 복제 청원으로 본다.
  초안의 '월×기질 서브코퍼스 내부' 기준은 월 경계를 넘는 복제와 비기질 청원과의 복제를 놓치므로 바꿨다.
"""

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "archive_01_raw_petitions" / "cheongwadae_petitions_2017-08_2019-08.parquet"
LEXICON_PATH = ROOT / "lexicon" / "lexicon.json"
OUT_DIR = ROOT / "archive_02_preprocessed"

STRICT_BODY_MIN = 2
PREFIX_LEN = 100
CLONE_MIN = 3
LLM_BATCH_SIZE = 3000
VALIDATION_PER_SUBSTRATE = 16
VALIDATION_NEGATIVES = 20
SEED = 20261030
KST = ZoneInfo("Asia/Seoul")
NON_WORD = re.compile(r"[^0-9A-Za-z가-힣]+")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def short_hash(s: str) -> str:
    return hashlib.blake2b(s.encode("utf-8"), digest_size=8).hexdigest()


def load_lexicon() -> dict:
    with LEXICON_PATH.open(encoding="utf-8") as f:
        lex = json.load(f)
    for group in ("substrates", "ligands"):
        for key, pattern in lex[group].items():
            lex[group][key] = re.compile(pattern, re.IGNORECASE)
    return lex


def tag(df: pd.DataFrame, lex: dict) -> tuple[list[str], list[str]]:
    s_cols, l_cols = list(lex["substrates"]), list(lex["ligands"])
    title = df["title"].fillna("")
    content = df["content"].fillna("")
    for key, rx in {**lex["substrates"], **lex["ligands"]}.items():
        title_hits = title.str.count(rx)
        body_hits = content.str.count(rx)
        df[f"{key}_hits"] = (title_hits + body_hits).astype("int32")
        df[f"{key}_loose"] = ((title_hits + body_hits) > 0).astype("int8")
        df[key] = ((title_hits > 0) | (body_hits >= STRICT_BODY_MIN)).astype("int8")
    df["substrate_count"] = df[s_cols].sum(axis=1).astype("int8")
    df["substrate_count_loose"] = df[[f"{c}_loose" for c in s_cols]].sum(axis=1).astype("int8")
    df["ligand_count"] = df[[f"{c}_loose" for c in l_cols]].sum(axis=1).astype("int8")
    for c in l_cols:
        df[c] = df[f"{c}_loose"]

    hit_matrix = df[[f"{c}_hits" for c in s_cols]].to_numpy() * df[s_cols].to_numpy()
    primary = np.where(hit_matrix.max(axis=1) > 0, hit_matrix.argmax(axis=1), -1)
    df["primary_substrate_rule"] = [s_cols[i] if i >= 0 else "None" for i in primary]

    hub_a = df[["L1_Morality_Family", "L2_Hygiene_Disease"]].max(axis=1)
    hub_b = df["L3_Meritocracy_Freeride"]
    df["hub_rule"] = np.select(
        [(hub_a == 1) & (hub_b == 1), hub_a == 1, hub_b == 1],
        ["Hub_C_Hybrid_Coalition", "Hub_A_Protestant_Moral", "Hub_B_Meritocracy_Youth"],
        default="None",
    )
    return s_cols, l_cols


def detect_clones(df: pd.DataFrame) -> None:
    norm = df["content"].fillna("").str.replace(NON_WORD, "", regex=True)
    df["content_norm_len"] = norm.str.len().astype("int32")
    df["full_hash"] = norm.map(short_hash)
    prefix = norm.str[:PREFIX_LEN]
    df["prefix_hash"] = np.where(df["content_norm_len"] >= PREFIX_LEN, prefix.map(short_hash), None)

    df["full_cluster_size"] = df.groupby("full_hash")["full_hash"].transform("size").astype("int32")
    df.loc[df["content_norm_len"] == 0, "full_cluster_size"] = 1
    prefix_size = df.groupby("prefix_hash")["prefix_hash"].transform("size")
    df["prefix_cluster_size"] = prefix_size.fillna(1).astype("int32")
    df["clone_cluster_size"] = df[["full_cluster_size", "prefix_cluster_size"]].max(axis=1)
    df["is_copy_paste_clone"] = (df["clone_cluster_size"] >= CLONE_MIN).astype("int8")


def split_top_level_alternatives(pattern: str) -> list[str]:
    body = pattern[1:-1] if pattern.startswith("(") and pattern.endswith(")") else pattern
    parts, depth, current = [], 0, ""
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "|" and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += ch
    parts.append(current)
    return [p for p in parts if p]


def lexicon_diagnostics(df: pd.DataFrame, lex_raw: dict) -> dict:
    report: dict = {"term_hits": {}, "substrate_ligand_term_overlap": []}
    text = df["text_full"]
    for group in ("substrates", "ligands"):
        for key, pattern in lex_raw[group].items():
            report["term_hits"][key] = {
                t: int(text.str.contains(re.compile(t, re.IGNORECASE)).sum())
                for t in split_top_level_alternatives(pattern)
            }
    sub_terms = {t for k in lex_raw["substrates"] for t in report["term_hits"][k]}
    lig_terms = {t for k in lex_raw["ligands"] for t in report["term_hits"][k]}
    report["substrate_ligand_term_overlap"] = sorted(sub_terms & lig_terms)
    return report


def aggregate_counts(df: pd.DataFrame, cols: list[str], freq: str) -> pd.DataFrame:
    keyed = df[cols + ["is_copy_paste_clone"]].assign(
        period=pd.to_datetime(df["begin"]).dt.to_period(freq).astype(str), total_petitions=1
    )
    out = keyed.groupby("period").sum(numeric_only=True)
    out = out.rename(columns={"is_copy_paste_clone": "clone_petitions"})
    return out.reindex(columns=["total_petitions"] + cols + ["clone_petitions"])


def stratified_sample(sub: pd.DataFrame, n_total: int) -> pd.DataFrame:
    sub = sub.assign(agree_tier=pd.cut(sub["num_agree"], [-1, 9, 99, 999, 9_999, np.inf], labels=False))
    strata = sub.groupby(["primary_substrate_rule", "agree_tier"])
    per_stratum = max(1, n_total // strata.ngroups)
    picked = pd.concat(g.sample(n=min(len(g), per_stratum), random_state=SEED) for _, g in strata)
    remaining = n_total - len(picked)
    if remaining > 0:
        rest = sub.drop(picked.index)
        picked = pd.concat([picked, rest.nlargest(remaining, "num_agree")])
    return picked.sort_values("petition_idx")


def preprocess_corpus() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(KST)

    with LEXICON_PATH.open(encoding="utf-8") as f:
        lex_raw = json.load(f)
    lex = load_lexicon()

    print("[Stage 2] 원본 로드...")
    df = pd.read_parquet(RAW_PATH, columns=["petition_idx", "category", "begin", "end", "num_agree", "status", "title", "content", "is_moderated"])
    df["text_full"] = (df["title"].fillna("") + " " + df["content"].fillna("")).str.strip()
    df["year_month"] = pd.to_datetime(df["begin"]).dt.to_period("M").astype(str)
    df["year_week"] = pd.to_datetime(df["begin"]).dt.to_period("W-SUN").astype(str)
    df["text_len"] = df["text_full"].str.len().astype("int32")

    print("[Stage 2] 규칙 태깅...")
    s_cols, l_cols = tag(df, lex)
    print("[Stage 2] 전 코퍼스 복제 탐지...")
    detect_clones(df)

    print("[Stage 2] 사전 진단...")
    diagnostics = lexicon_diagnostics(df, lex_raw)
    if diagnostics["substrate_ligand_term_overlap"]:
        raise ValueError(f"기질-리간드 사전 중복 어휘: {diagnostics['substrate_ligand_term_overlap']}")

    light_cols = [c for c in df.columns if c not in ("title", "content", "text_full")]
    full_path = OUT_DIR / "stage2_tagged_full.parquet"
    df[light_cols].to_parquet(full_path, index=False, compression="zstd")

    sub = df[df["substrate_count_loose"] >= 1].drop(columns=["text_full"]).reset_index(drop=True)
    sub_path = OUT_DIR / "stage2_preprocessed_substrates.parquet"
    sub.to_parquet(sub_path, index=False, compression="zstd")
    strict_sub = sub[sub["substrate_count"] >= 1]

    loose_cols = [f"{c}_loose" for c in s_cols]
    monthly = aggregate_counts(df, s_cols + loose_cols + l_cols, "M")
    weekly = aggregate_counts(df, s_cols + loose_cols + l_cols, "W-SUN")
    monthly.to_csv(OUT_DIR / "stage2_monthly_counts.csv", encoding="utf-8")
    weekly.to_csv(OUT_DIR / "stage2_weekly_counts.csv", encoding="utf-8")

    export_cols = ["petition_idx", "begin", "category", "num_agree", "title", "content", "primary_substrate_rule", "hub_rule", "ligand_count"] + s_cols + l_cols
    batch = stratified_sample(strict_sub, LLM_BATCH_SIZE)
    batch_path = OUT_DIR / "stage2_llm_batch_input_strat3000.csv"
    batch[export_cols].to_csv(batch_path, index=False, encoding="utf-8-sig")

    val_pos = pd.concat(
        strict_sub[strict_sub["primary_substrate_rule"] == s].sample(n=VALIDATION_PER_SUBSTRATE, random_state=SEED)
        for s in s_cols
    )
    val_loose_only = sub[(sub["substrate_count"] == 0)].sample(n=VALIDATION_NEGATIVES, random_state=SEED)
    val_neg = df[df["substrate_count_loose"] == 0].sample(n=VALIDATION_NEGATIVES, random_state=SEED)
    val = pd.concat([val_pos, val_loose_only, val_neg]).sample(frac=1, random_state=SEED)
    val = val.assign(
        excerpt=(val["title"].fillna("") + " ‖ " + val["content"].fillna("").str.slice(0, 380)),
        sample_stratum=np.where(
            val["substrate_count"] >= 1, "strict_positive", np.where(val["substrate_count_loose"] >= 1, "loose_only", "negative")
        ),
    )
    val_path = OUT_DIR / "stage2_validation_sample.csv"
    val[["petition_idx", "begin", "category", "num_agree", "sample_stratum", "excerpt", "primary_substrate_rule", "hub_rule"] + s_cols + loose_cols + l_cols].to_csv(
        val_path, index=False, encoding="utf-8-sig"
    )

    summary = {
        "total_petitions": int(len(df)),
        "substrate_subcorpus_loose": int(len(sub)),
        "substrate_subcorpus_strict": int(len(strict_sub)),
        "substrate_counts_strict": {c: int(df[c].sum()) for c in s_cols},
        "substrate_counts_loose": {c: int(df[f"{c}_loose"].sum()) for c in s_cols},
        "ligand_counts_in_strict_subcorpus": {c: int(strict_sub[c].sum()) for c in l_cols},
        "multi_substrate_petitions_strict": int((df["substrate_count"] >= 2).sum()),
        "clone_petitions_full_corpus": int(df["is_copy_paste_clone"].sum()),
        "clone_rate_full_corpus_pct": round(float(df["is_copy_paste_clone"].mean() * 100), 3),
        "clone_rate_strict_subcorpus_pct": round(float(strict_sub["is_copy_paste_clone"].mean() * 100), 3),
        "hub_rule_counts_strict_subcorpus": {k: int(v) for k, v in strict_sub["hub_rule"].value_counts().items()},
    }
    with (OUT_DIR / "stage2_lexicon_diagnostics.json").open("w", encoding="utf-8") as f:
        json.dump({"summary": summary, **diagnostics}, f, ensure_ascii=False, indent=2)

    outputs = [full_path, sub_path, OUT_DIR / "stage2_monthly_counts.csv", OUT_DIR / "stage2_weekly_counts.csv",
               OUT_DIR / "stage2_lexicon_diagnostics.json", batch_path, val_path]
    provenance = {
        "stage": "Stage 2 preprocessing & rule tagging",
        "script": Path(__file__).name,
        "script_sha256": sha256_file(Path(__file__)),
        "started_at_kst": started.isoformat(timespec="seconds"),
        "finished_at_kst": datetime.now(KST).isoformat(timespec="seconds"),
        "inputs": {
            RAW_PATH.relative_to(ROOT).as_posix(): sha256_file(RAW_PATH),
            LEXICON_PATH.relative_to(ROOT).as_posix(): sha256_file(LEXICON_PATH),
        },
        "lexicon_version": lex_raw["version"],
        "parameters": {
            "clone_prefix_len": PREFIX_LEN,
            "clone_min_cluster": CLONE_MIN,
            "llm_batch_size": LLM_BATCH_SIZE,
            "validation_per_substrate": VALIDATION_PER_SUBSTRATE,
            "validation_negatives": VALIDATION_NEGATIVES,
            "random_seed": SEED,
            "primary_substrate_rule": "정규식 적중 횟수 최대 기질(동률 시 사전 순서상 앞)",
            "hub_rule": "L1|L2 → Hub A, L3 → Hub B, 둘 다 → Hub C",
        },
        "summary": summary,
        "outputs": {p.relative_to(ROOT).as_posix(): sha256_file(p) for p in outputs},
        "environment": {"python": sys.version.split()[0], "pandas": pd.__version__, "numpy": np.__version__},
    }
    with (OUT_DIR / "stage2_provenance.json").open("w", encoding="utf-8") as f:
        json.dump(provenance, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    preprocess_corpus()
