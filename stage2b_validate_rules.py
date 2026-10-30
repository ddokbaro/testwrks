"""[Stage 2b] 규칙 태깅 타당도 검증 및 LLM 주석 일치도 산출

입력
  annotation/*.csv   gold_relevant / gold_hostile 열(쉼표 구분 기질 코드, 예: "S1,S4")을 가진 주석 파일
  (선택) annotation/llm_labels_*.csv   웍스AI 에이전트가 반환한 LLM 라벨(petition_idx, primary_substrate, ...)

산출
  archive_02_preprocessed/stage2b_rule_validation.json
    - 기질별 strict/loose 규칙의 precision / recall / F1 (gold_relevant 기준)
    - 규칙 양성 중 적대적(hostile) 발화 비율 (gold_hostile 기준)
    - LLM 라벨 파일이 있으면 규칙·LLM 간 Cohen's kappa

주의: 현재 gold 라벨은 Claude Opus 5.5(Wrks Coding Agent)가 부여한 AI 보조 주석이다.
논문 투고 전 연구자 본인(또는 2인 이상 인간 코더)의 검수가 필요하다.
"""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
ANNOT_DIR = ROOT / "annotation"
OUT = ROOT / "archive_02_preprocessed" / "stage2b_rule_validation.json"
SUBSTRATES = {
    "S1": "S1_Game_Subculture",
    "S2": "S2_LGBTQ",
    "S3": "S3_Islam_Refugee",
    "S4": "S4_Gender_Disability",
    "S5": "S5_China",
}


def code_set(cell: str) -> set[str]:
    return {c.strip() for c in str(cell).split(",") if c.strip()}


def prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * precision * recall / (precision + recall) if precision and recall else None
    rnd = lambda x: None if x is None else round(x, 3)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": rnd(precision), "recall": rnd(recall), "f1": rnd(f1)}


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    labels = set(a) | set(b)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(lab) / n) * (b.count(lab) / n) for lab in labels)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def evaluate(df: pd.DataFrame) -> dict:
    gold_rel = df["gold_relevant"].map(code_set)
    gold_hos = df["gold_hostile"].map(code_set)
    result: dict = {"n": int(len(df)), "per_substrate": {}}
    micro = {"strict": [0, 0, 0], "loose": [0, 0, 0]}
    for code, col in SUBSTRATES.items():
        entry = {}
        for mode, rule_col in (("strict", col), ("loose", f"{col}_loose")):
            pred = df[rule_col].astype(int) == 1
            truth = gold_rel.map(lambda s, c=code: c in s)
            tp, fp, fn = int((pred & truth).sum()), int((pred & ~truth).sum()), int((~pred & truth).sum())
            for i, v in enumerate((tp, fp, fn)):
                micro[mode][i] += v
            entry[mode] = prf(tp, fp, fn)
            hostile_given_pred = gold_hos[pred].map(lambda s, c=code: c in s)
            entry[mode]["hostile_share_among_rule_positive"] = (
                round(float(hostile_given_pred.mean()), 3) if len(hostile_given_pred) else None
            )
        result["per_substrate"][col] = entry
    result["micro"] = {mode: prf(*vals) for mode, vals in micro.items()}
    return result


def main() -> None:
    report: dict = {
        "annotation_note": (
            "gold 라벨은 Claude Opus 5.5(Wrks Coding Agent)의 AI 보조 주석이며 인간 검수 전 잠정치다. "
            "relevant=해당 집단·쟁점이 청원의 실질 주제, hostile=해당 집단에 대한 배제·비하·권리 제한 요구."
        ),
        "files": {},
    }
    for path in sorted(ANNOT_DIR.glob("validation_*.csv")):
        df = pd.read_csv(path, keep_default_na=False)
        report["files"][path.name] = evaluate(df)

    llm_files = sorted(ANNOT_DIR.glob("llm_labels_*.csv"))
    if llm_files:
        batch = pd.read_csv(ROOT / "archive_02_preprocessed" / "stage2_llm_batch_input_strat3000.csv", keep_default_na=False)
        for path in llm_files:
            llm = pd.read_csv(path, keep_default_na=False)
            merged = batch.merge(llm, on="petition_idx", how="inner", suffixes=("", "_llm"))
            rule = merged["primary_substrate_rule"].str[:2].tolist()
            model = merged["primary_substrate"].astype(str).str[:2].tolist()
            hub_rule = merged["hub_rule"].tolist()
            hub_llm = merged["catalytic_hub_frame"].astype(str).tolist() if "catalytic_hub_frame" in merged else []
            report["files"][path.name] = {
                "n_matched": int(len(merged)),
                "kappa_primary_substrate_rule_vs_llm": cohen_kappa(rule, model),
                "kappa_hub_rule_vs_llm": cohen_kappa(hub_rule, hub_llm) if hub_llm else None,
            }
    else:
        report["llm_agreement"] = "llm_labels_*.csv 없음 - 웍스AI 에이전트 라벨 반환 후 재실행"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    json.dump(report, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
