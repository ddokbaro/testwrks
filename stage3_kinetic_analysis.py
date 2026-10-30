"""[Stage 3] 교차 촉매(γ_ij) · 자가촉매 누적곡선 · 리간드 결합 수에 따른 비선형 증폭(+NLE) · 중심축 이동 분석

입력: archive_02_preprocessed/stage2_tagged_full.parquet (Stage 2, 436,660건 전 코퍼스 태그)
산출: archive_03_analysis_outputs/
  stage3_kinetic_results_summary.json   전체 결과(계수·검정통계·표본 수·분석 설정)
  stage3_table_*.csv                    논문 표 원자료
  fig1~fig5 *.png                       한글 그래프 (300 dpi)

초안 대비 수정한 분석 설계 (근거는 summary.json 의 "design_notes"에 함께 기록)
  1. 월별 OLS(관측 19개, 회귀계수 6개)는 자유도가 부족해 γ_ij 추정이 불안정하다.
     → 주별 시계열(분석 창 2017-09-04 ~ 2019-03-31, 82주)에 대해 VAR(p) 를 적합하고,
       기질 쌍별 Granger 인과 검정 20개에 Benjamini-Hochberg FDR 보정을 적용한다.
  2. 청원 총량 자체가 주마다 크게 변동하므로(수집 공백·게시판 개편) 건수 대신
     '전체 청원 1,000건당 기질 청원 수'(농도)에 log1p 를 취해 사용한다.
  3. 2019-04 이후는 원천 수집량이 월 수백 건으로 급감하여 분석 창에서 제외한다.
  4. +NLE 검정은 청원 단위 회귀로 수행하고 본문 길이·월 고정효과·청원 분류·복제 여부·기질을 통제한다.
     장문일수록 여러 리간드 어휘가 우연히 적중하므로 길이 통제가 필수다.
     리간드 효과가 혐오 기질 고유의 현상인지 보기 위해 비기질 청원과의 상호작용 모형을 함께 적합한다.
  5. 중심축 이동은 Hub A(도덕·위생)와 Hub B(공정·무임승차)의 상대 우세를
     ee = (B - A) / (B + A) 로 요약하고(거울상 과잉률의 유비), 반기별 추이와 로지스틱 추세 검정을 보고한다.
"""

import json
import sys
import warnings
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib import font_manager
from scipy.optimize import curve_fit
from statsmodels.stats.multitest import multipletests
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parent
IN_PATH = ROOT / "archive_02_preprocessed" / "stage2_tagged_full.parquet"
OUT_DIR = ROOT / "archive_03_analysis_outputs"
FONT_DIR = ROOT / "assets" / "fonts"
KST = ZoneInfo("Asia/Seoul")

WINDOW_START = "2017-09-04"
WINDOW_END = "2019-03-31"
VAR_MAXLAGS = 4
SEED = 20261030

S_COLS = ["S1_Game_Subculture", "S2_LGBTQ", "S3_Islam_Refugee", "S4_Gender_Disability", "S5_China"]
S_LABEL = {
    "S1_Game_Subculture": "S1 게임·서브컬처",
    "S2_LGBTQ": "S2 성소수자",
    "S3_Islam_Refugee": "S3 이슬람·난민",
    "S4_Gender_Disability": "S4 젠더·장애",
    "S5_China": "S5 중국",
}
L_COLS = ["L1_Morality_Family", "L2_Hygiene_Disease", "L3_Meritocracy_Freeride", "L4_Security_Sovereignty"]

warnings.filterwarnings("ignore", category=FutureWarning)


def setup_font() -> str:
    for ttf in FONT_DIR.glob("*.ttf"):
        font_manager.fontManager.addfont(str(ttf))
    plt.rcParams["font.family"] = "NanumGothic"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 110
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    return "NanumGothic"


def rnd(x: float, n: int = 4) -> float | None:
    return None if x is None or not np.isfinite(x) else round(float(x), n)


def load() -> pd.DataFrame:
    df = pd.read_parquet(IN_PATH)
    df["begin"] = pd.to_datetime(df["begin"])
    return df


def weekly_concentration(df: pd.DataFrame) -> pd.DataFrame:
    w = df[(df["begin"] >= WINDOW_START) & (df["begin"] <= WINDOW_END)]
    week = w["begin"].dt.to_period("W-SUN").dt.start_time
    counts = w[S_COLS].groupby(week).sum()
    total = w.groupby(week).size()
    conc = counts.div(total, axis=0) * 1000
    conc["total_petitions"] = total
    return conc


def cross_catalysis(conc: pd.DataFrame) -> dict:
    y = np.log1p(conc[S_COLS])
    adf = {c: {"stat": rnd(adfuller(y[c], autolag="AIC")[0]), "p": rnd(adfuller(y[c], autolag="AIC")[1])} for c in S_COLS}
    nonstationary = [c for c, r in adf.items() if r["p"] is not None and r["p"] > 0.05]
    series = y.diff().dropna() if nonstationary else y
    transform = "first_difference_of_log1p" if nonstationary else "log1p_level"

    model = VAR(series)
    order = model.select_order(maxlags=VAR_MAXLAGS)
    p = max(1, int(order.aic))
    res = model.fit(p)

    gamma = {}
    for tgt in S_COLS:
        gamma[tgt] = {}
        for src in S_COLS:
            coefs = [res.params.loc[f"L{lag}.{src}", tgt] for lag in range(1, p + 1)]
            gamma[tgt][src] = rnd(sum(coefs))

    tests = []
    for tgt in S_COLS:
        for src in S_COLS:
            if src == tgt:
                continue
            t = res.test_causality(tgt, [src], kind="f")
            tests.append({"source": src, "target": tgt, "F": rnd(t.test_statistic), "p_raw": rnd(t.pvalue, 6)})
    reject, p_adj, _, _ = multipletests([t["p_raw"] for t in tests], alpha=0.05, method="fdr_bh")
    for t, r, q in zip(tests, reject, p_adj):
        t["q_bh"] = rnd(q, 6)
        t["significant_fdr05"] = bool(r)

    irf = res.irf(8)
    irf_cum = {
        tgt: {src: rnd(irf.cum_effects[8, S_COLS.index(tgt), S_COLS.index(src)]) for src in S_COLS} for tgt in S_COLS
    }
    return {
        "n_weeks": int(len(series)),
        "window": [WINDOW_START, WINDOW_END],
        "transform": transform,
        "adf_log1p_levels": adf,
        "lag_order_aic": p,
        "lag_order_bic": int(order.bic),
        "gamma_sum_of_lag_coefficients": gamma,
        "granger_tests": tests,
        "orthogonalized_irf_cumulative_8w": irf_cum,
        "var_stable": bool(res.is_stable()),
        "durbin_watson": {c: rnd(v) for c, v in zip(S_COLS, sm.stats.durbin_watson(res.resid))},
    }, series, res


def granger_sensitivity(df: pd.DataFrame) -> dict:
    out = {}
    w = df[(df["begin"] >= WINDOW_START) & (df["begin"] <= WINDOW_END)]
    week = w["begin"].dt.to_period("W-SUN").dt.start_time
    total = w.groupby(week).size()
    variants = {
        "strict_p1": (S_COLS, 1),
        "loose_pAIC": ([f"{c}_loose" for c in S_COLS], None),
    }
    for name, (cols, p_fixed) in variants.items():
        conc = w[cols].groupby(week).sum().div(total, axis=0) * 1000
        conc.columns = S_COLS
        y = np.log1p(conc).diff().dropna()
        model = VAR(y)
        p = p_fixed or max(1, int(model.select_order(maxlags=VAR_MAXLAGS).aic))
        res = model.fit(p)
        tests = []
        for tgt in S_COLS:
            for src in S_COLS:
                if src != tgt:
                    t = res.test_causality(tgt, [src], kind="f")
                    tests.append({"source": src, "target": tgt, "p_raw": rnd(t.pvalue, 6)})
        reject, q, _, _ = multipletests([t["p_raw"] for t in tests], method="fdr_bh")
        for t, r, qq in zip(tests, reject, q):
            t["q_bh"] = rnd(qq, 6)
            t["significant_fdr05"] = bool(r)
        out[name] = {"lag": p, "n_significant_fdr05": int(sum(reject)),
                     "min_q": rnd(float(min(q)), 6),
                     "top3": sorted(tests, key=lambda x: x["p_raw"])[:3]}
    return out


def autocatalytic_sigmoid(t, K, k0, k_auto, t0):
    return K / (1.0 + ((K - k0) / (k0 + 1e-6)) * np.exp(-k_auto * K * (t - t0)))


def logistic_fits(df: pd.DataFrame) -> dict:
    w = df[(df["begin"] >= WINDOW_START) & (df["begin"] <= WINDOW_END)]
    days = pd.date_range(WINDOW_START, WINDOW_END, freq="D")
    out = {}
    curves = {}
    for col in S_COLS:
        daily = w.loc[w[col] == 1].groupby("begin").size().reindex(days, fill_value=0)
        cum = daily.cumsum().to_numpy(dtype=float)
        t = np.arange(len(cum), dtype=float)
        n = len(t)
        lin = np.polyfit(t, cum, 1)
        rss_lin = float(np.sum((cum - np.polyval(lin, t)) ** 2))
        aic_lin = n * np.log(rss_lin / n) + 2 * 2
        try:
            best = None
            for t0_guess in np.linspace(0, n, 9):
                for r_guess in (0.005, 0.02, 0.08):
                    K0 = cum[-1] * 1.05
                    try:
                        popt_i, _ = curve_fit(
                            autocatalytic_sigmoid, t, cum,
                            p0=[K0, max(cum[0], 1.0), r_guess / K0, t0_guess],
                            bounds=([cum[-1], 1e-3, 0, -n], [cum[-1] * 20, cum[-1], 1.0, 2 * n]),
                            maxfev=20000,
                        )
                    except RuntimeError:
                        continue
                    rss_i = float(np.sum((cum - autocatalytic_sigmoid(t, *popt_i)) ** 2))
                    if best is None or rss_i < best[1]:
                        best = (popt_i, rss_i)
            if best is None:
                raise RuntimeError("no convergence")
            popt = best[0]
            fitted = autocatalytic_sigmoid(t, *popt)
            rss_sig = float(np.sum((cum - fitted) ** 2))
            aic_sig = n * np.log(rss_sig / n) + 2 * 4
            r2 = 1 - rss_sig / float(np.sum((cum - cum.mean()) ** 2))
            peak_daily = int(daily.max())
            out[col] = {
                "K": rnd(popt[0], 1), "k0": rnd(popt[1], 2), "k_auto": float(f"{popt[2]:.3e}"), "t0": rnd(popt[3], 1),
                "rate_r=k_auto*K_per_day": rnd(popt[2] * popt[0], 5),
                "r2": rnd(r2), "aic_sigmoid": rnd(aic_sig, 1), "aic_linear": rnd(aic_lin, 1),
                "delta_aic_linear_minus_sigmoid": rnd(aic_lin - aic_sig, 1),
                "final_cumulative": int(cum[-1]), "peak_daily": peak_daily,
                "peak_date": str(daily.idxmax().date()),
            }
            curves[col] = (days, cum, fitted)
        except RuntimeError as exc:
            out[col] = {"error": str(exc)}
    return {"fits": out, "_curves": curves}


def yemen_episode_fit(df: pd.DataFrame) -> dict:
    start, end = "2018-05-01", "2018-09-30"
    days = pd.date_range(start, end, freq="D")
    s3 = df[(df["S3_Islam_Refugee"] == 1) & (df["begin"] >= start) & (df["begin"] <= end)]
    cum = s3.groupby("begin").size().reindex(days, fill_value=0).cumsum().to_numpy(dtype=float)
    t = np.arange(len(cum), dtype=float)
    K0 = cum[-1] * 1.02
    popt, _ = curve_fit(
        autocatalytic_sigmoid, t, cum, p0=[K0, max(cum[0], 1.0), 4.0 / (K0 * 40), 40.0],
        bounds=([cum[-1], 1e-3, 0, 0], [cum[-1] * 5, cum[-1], 1.0, len(t)]), maxfev=40000,
    )
    fitted = autocatalytic_sigmoid(t, *popt)
    rss = float(np.sum((cum - fitted) ** 2))
    lin = np.polyfit(t, cum, 1)
    rss_lin = float(np.sum((cum - np.polyval(lin, t)) ** 2))
    n = len(t)
    return {
        "window": [start, end],
        "K": rnd(popt[0], 1), "k0": rnd(popt[1], 2), "k_auto": float(f"{popt[2]:.3e}"),
        "t0_day": rnd(popt[3], 1), "t0_date": str((pd.Timestamp(start) + pd.Timedelta(days=float(popt[3]))).date()),
        "rate_r_per_day": rnd(popt[2] * popt[0], 4),
        "r2": rnd(1 - rss / float(np.sum((cum - cum.mean()) ** 2))),
        "delta_aic_linear_minus_sigmoid": rnd((n * np.log(rss_lin / n) + 4) - (n * np.log(rss / n) + 8), 1),
        "_curve": (days, cum, fitted),
    }


def nle_analysis(df: pd.DataFrame) -> dict:
    w = df[(df["begin"] >= WINDOW_START) & (df["begin"] <= WINDOW_END)].copy()
    w["log_agree"] = np.log1p(w["num_agree"])
    w["log_len"] = np.log(w["text_len"].clip(lower=1))
    w["ym"] = w["begin"].dt.to_period("M").astype(str)
    w["lig_cat"] = w["ligand_count"].clip(upper=3).astype(int)
    w["is_substrate"] = (w["substrate_count"] >= 1).astype(int)
    w["agree_1k"] = (w["num_agree"] >= 1000).astype(int)

    sub = w[w["is_substrate"] == 1].copy()

    descr = (
        sub.groupby("ligand_count")
        .agg(n=("num_agree", "size"), mean_agree=("num_agree", "mean"), median_agree=("num_agree", "median"),
             share_ge1k=("agree_1k", "mean"), share_ge200k=("num_agree", lambda x: float((x >= 200_000).mean())),
             clone_rate=("is_copy_paste_clone", "mean"), median_len=("text_len", "median"))
        .reset_index()
    )

    f_base = "log_agree ~ C(lig_cat) + log_len + is_copy_paste_clone + C(ym) + C(category) + " + " + ".join(S_COLS)
    m_raw = smf.ols("log_agree ~ C(lig_cat)", data=sub).fit(cov_type="HC3")
    m_ctl = smf.ols(f_base, data=sub).fit(cov_type="HC3")
    m_quad = smf.ols(
        "log_agree ~ ligand_count + I(ligand_count**2) + log_len + is_copy_paste_clone + C(ym) + C(category) + " + " + ".join(S_COLS),
        data=sub,
    ).fit(cov_type="HC3")
    m_logit = smf.logit(
        "agree_1k ~ C(lig_cat) + log_len + is_copy_paste_clone + C(ym) + " + " + ".join(S_COLS), data=sub
    ).fit(disp=0, cov_type="HC1", method="bfgs", maxiter=2000)

    m_inter = smf.ols(
        "log_agree ~ C(lig_cat) * is_substrate + log_len + is_copy_paste_clone + C(ym) + C(category)", data=w
    ).fit(cov_type="HC3")

    def coef_table(m, prefix: str) -> dict:
        ci = m.conf_int()
        return {
            k: {"coef": rnd(m.params[k]), "ci_low": rnd(ci.loc[k, 0]), "ci_high": rnd(ci.loc[k, 1]), "p": rnd(m.pvalues[k], 6)}
            for k in m.params.index if k.startswith(prefix)
        }

    increments = {}
    b = {k: m_ctl.params.get(f"C(lig_cat)[T.{k}]", 0.0) for k in (1, 2, 3)}
    b[0] = 0.0
    for k in (1, 2, 3):
        increments[f"{k-1}->{k}"] = rnd(b[k] - b[k - 1])
    convex_test = m_ctl.t_test("C(lig_cat)[T.3] - 2*C(lig_cat)[T.2] + C(lig_cat)[T.1] = 0")

    return {
        "sample": "strict 기질 청원(분석 창 내)",
        "n_substrate": int(len(sub)),
        "n_full_window": int(len(w)),
        "descriptive_by_ligand_count": descr.round(4).to_dict(orient="records"),
        "ols_raw_lig_cat": coef_table(m_raw, "C(lig_cat)"),
        "ols_controlled_lig_cat": coef_table(m_ctl, "C(lig_cat)"),
        "ols_controlled_r2": rnd(m_ctl.rsquared),
        "ols_controlled_log_len": coef_table(m_ctl, "log_len"),
        "marginal_increments_controlled": increments,
        "second_difference_test_(b3-2b2+b1)": {
            "estimate": rnd(float(np.asarray(convex_test.effect).ravel()[0])),
            "p": rnd(float(np.asarray(convex_test.pvalue).ravel()[0]), 6),
        },
        "ols_quadratic": coef_table(m_quad, "ligand_count") | coef_table(m_quad, "I(ligand_count"),
        "logit_agree_ge_1000_odds_ratios": {
            k: {"OR": rnd(np.exp(m_logit.params[k])), "p": rnd(m_logit.pvalues[k], 6)}
            for k in m_logit.params.index if k.startswith("C(lig_cat)")
        },
        "interaction_full_corpus": coef_table(m_inter, "C(lig_cat)"),
        "interaction_n": int(m_inter.nobs),
        "_models": (m_ctl,),
        "_descr": descr,
    }


def hub_shift(df: pd.DataFrame) -> dict:
    w = df[(df["begin"] >= WINDOW_START) & (df["begin"] <= WINDOW_END) & (df["substrate_count"] >= 1)].copy()
    w["hubA"] = ((w["L1_Morality_Family"] == 1) | (w["L2_Hygiene_Disease"] == 1)).astype(int)
    w["hubB"] = (w["L3_Meritocracy_Freeride"] == 1).astype(int)
    w["half"] = w["begin"].dt.year.astype(str) + "H" + np.where(w["begin"].dt.month <= 6, "1", "2")
    w["t_months"] = (w["begin"] - pd.Timestamp(WINDOW_START)).dt.days / 30.44

    def ee(g: pd.DataFrame) -> float:
        a, b = g["hubA"].sum(), g["hubB"].sum()
        return float((b - a) / (b + a)) if a + b else np.nan

    profile, by_half, trend = {}, {}, {}
    rng = np.random.default_rng(SEED)
    for col in S_COLS:
        g = w[w[col] == 1]
        boots = []
        for _ in range(2000):
            idx = rng.integers(0, len(g), len(g))
            boots.append(ee(g.iloc[idx]))
        lo, hi = np.nanpercentile(boots, [2.5, 97.5])
        profile[col] = {
            "n": int(len(g)),
            "hubA_rate": rnd(g["hubA"].mean()),
            "hubB_rate": rnd(g["hubB"].mean()),
            "hubC_rate_(A&B)": rnd(((g["hubA"] == 1) & (g["hubB"] == 1)).mean()),
            "security_rate_L4": rnd(g["L4_Security_Sovereignty"].mean()),
            "ligand_rates": {l: rnd(g[l].mean()) for l in L_COLS},
            "ee_B_minus_A": rnd(ee(g)),
            "ee_bootstrap95": [rnd(lo), rnd(hi)],
            "clone_rate": rnd(g["is_copy_paste_clone"].mean()),
        }
        by_half[col] = {h: {"n": int(len(x)), "ee": rnd(ee(x)), "hubA": int(x["hubA"].sum()), "hubB": int(x["hubB"].sum())}
                        for h, x in g.groupby("half")}
        ab = g[(g["hubA"] + g["hubB"]) == 1]
        if len(ab) >= 30 and ab["hubB"].nunique() == 2:
            m = smf.logit("hubB ~ t_months", data=ab).fit(disp=0)
            trend[col] = {"n_A_xor_B": int(len(ab)), "logit_slope_per_month": rnd(m.params["t_months"]),
                          "p": rnd(m.pvalues["t_months"], 6)}
        else:
            trend[col] = {"n_A_xor_B": int(len(ab)), "logit_slope_per_month": None, "p": None}

    all_hc = w.assign(hubC=((w["hubA"] == 1) & (w["hubB"] == 1)).astype(int))
    contingency = pd.DataFrame({c: [int(all_hc.loc[all_hc[c] == 1, "hubC"].sum()),
                                    int((all_hc.loc[all_hc[c] == 1, "hubC"] == 0).sum())] for c in S_COLS},
                               index=["hubC", "not_hubC"])
    chi2, p_chi, dof, _ = scipy.stats.chi2_contingency(contingency.to_numpy())

    s5 = w[w["S5_China"] == 1]
    rest = w[w["S5_China"] == 0]
    s5_c = int(((s5["hubA"] == 1) & (s5["hubB"] == 1)).sum())
    rest_c = int(((rest["hubA"] == 1) & (rest["hubB"] == 1)).sum())
    fisher_or, fisher_p = scipy.stats.fisher_exact([[s5_c, len(s5) - s5_c], [rest_c, len(rest) - rest_c]])

    co = w[S_COLS].astype("int64").T.dot(w[S_COLS].astype("int64"))
    return {
        "profile_by_substrate": profile,
        "ee_by_half_year": by_half,
        "logit_trend_hubB_vs_hubA": trend,
        "hubC_by_substrate_chi2": {"chi2": rnd(chi2), "dof": int(dof), "p": rnd(p_chi, 6), "table": contingency.to_dict()},
        "s5_hubC_fisher_vs_rest": {"s5_hubC": s5_c, "s5_n": int(len(s5)), "rest_hubC": rest_c, "rest_n": int(len(rest)),
                                   "odds_ratio": rnd(fisher_or), "p": rnd(fisher_p, 6)},
        "substrate_cooccurrence_strict": co.astype(int).to_dict(),
    }


def clone_analysis(df: pd.DataFrame) -> dict:
    w = df[(df["begin"] >= WINDOW_START) & (df["begin"] <= WINDOW_END)]
    base = float(w["is_copy_paste_clone"].mean())
    per = {}
    for col in S_COLS:
        g = w[w[col] == 1]
        clones = g[g["is_copy_paste_clone"] == 1]
        per[col] = {
            "n": int(len(g)), "clone_rate": rnd(g["is_copy_paste_clone"].mean()),
            "rate_ratio_vs_corpus": rnd(g["is_copy_paste_clone"].mean() / base),
            "n_clone_clusters": int(clones["full_hash"].nunique()),
            "largest_cluster": int(g["clone_cluster_size"].max()),
            "median_agree_clone": rnd(clones["num_agree"].median(), 1),
            "median_agree_nonclone": rnd(g.loc[g["is_copy_paste_clone"] == 0, "num_agree"].median(), 1),
        }
    non = w[w["substrate_count"] == 0]
    return {"corpus_clone_rate": rnd(base), "non_substrate_clone_rate": rnd(non["is_copy_paste_clone"].mean()),
            "by_substrate": per}


def plot_all(conc, fits, yemen, nle, hub, gr) -> list[str]:
    files = []
    colors = ["#3b6ea5", "#c0504d", "#4f8f5b", "#8064a2", "#d08b2c"]

    fig, ax = plt.subplots(figsize=(10, 4.6))
    for c, col in zip(S_COLS, colors):
        ax.plot(conc.index, conc[c], label=S_LABEL[c], color=col, lw=1.4)
    ax.set_yscale("symlog", linthresh=1)
    ax.set_ylabel("전체 청원 1,000건당 기질 청원 수 (symlog)")
    ax.set_title("그림 1. 주별 기질 농도 H_i(t) (2017-09 ~ 2019-03, strict 규칙)")
    ax.legend(ncol=5, fontsize=8, frameon=False, loc="upper left")
    fig.tight_layout()
    files.append("fig1_weekly_substrate_concentration.png")
    fig.savefig(OUT_DIR / files[-1])
    plt.close(fig)

    q = pd.DataFrame(index=S_COLS, columns=S_COLS, dtype=float)
    g = pd.DataFrame(gr["gamma_sum_of_lag_coefficients"]).T.loc[S_COLS, S_COLS]
    for t in gr["granger_tests"]:
        q.loc[t["target"], t["source"]] = t["q_bh"]
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    vmax = np.nanmax(np.abs(g.to_numpy()))
    im = ax.imshow(g.to_numpy(dtype=float), cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    for i in range(5):
        for j in range(5):
            mark = ""
            if i != j and q.iloc[i, j] < 0.05:
                mark = "**"
            elif i != j and q.iloc[i, j] < 0.10:
                mark = "*"
            ax.text(j, i, f"{g.iloc[i, j]:.2f}{mark}", ha="center", va="center", fontsize=8)
    ax.set_xticks(range(5), [S_LABEL[c] for c in S_COLS], rotation=35, ha="right", fontsize=8)
    ax.set_yticks(range(5), [S_LABEL[c] for c in S_COLS], fontsize=8)
    ax.set_xlabel("원인 기질 i (t-1…t-p)")
    ax.set_ylabel("결과 기질 j (t)")
    ax.set_title(f"그림 2. 교차 촉매 계수 γ_ij (VAR({gr['lag_order_aic']}), 시차계수 합)\n** q<.05, * q<.10 (Granger, BH-FDR)", fontsize=10)
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    files.append("fig2_cross_catalysis_gamma_heatmap.png")
    fig.savefig(OUT_DIR / files[-1])
    plt.close(fig)

    days, cum, fitted = yemen["_curve"]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(days, cum, color="#4f8f5b", lw=2, label="관측 누적 S3 청원")
    ax.plot(days, fitted, color="black", ls="--", lw=1.2, label=f"자가촉매 시그모이드 적합 (R²={yemen['r2']})")
    ax.axvline(pd.Timestamp(yemen["t0_date"]), color="grey", lw=0.8)
    ax.set_title("그림 3. 2018년 제주 예멘 난민 국면의 S3 누적 청원과 자가촉매 곡선")
    ax.set_ylabel("누적 청원 수")
    ax.legend(frameon=False)
    fig.tight_layout()
    files.append("fig3_yemen_autocatalytic_sigmoid.png")
    fig.savefig(OUT_DIR / files[-1])
    plt.close(fig)

    ctl = nle["ols_controlled_lig_cat"]
    ks = [0, 1, 2, 3]
    est = [0.0] + [ctl[f"C(lig_cat)[T.{k}]"]["coef"] for k in (1, 2, 3)]
    lo = [0.0] + [ctl[f"C(lig_cat)[T.{k}]"]["ci_low"] for k in (1, 2, 3)]
    hi = [0.0] + [ctl[f"C(lig_cat)[T.{k}]"]["ci_high"] for k in (1, 2, 3)]
    raw = nle["ols_raw_lig_cat"]
    est_raw = [0.0] + [raw[f"C(lig_cat)[T.{k}]"]["coef"] for k in (1, 2, 3)]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(ks, est_raw, "o--", color="#999999", label="통제 전")
    ax.errorbar(ks, est, yerr=[np.subtract(est, lo), np.subtract(hi, est)], fmt="o-", color="#c0504d", capsize=4,
                label="길이·월·분류·복제·기질 통제 (95% CI, HC3)")
    ax.set_xticks(ks, ["0", "1", "2", "3+"])
    ax.set_xlabel("결합 리간드 수")
    ax.set_ylabel("log(1+동의 수) 차이 (기준: 0개)")
    ax.set_title("그림 4. 리간드 결합 수에 따른 동의 수 증폭(+NLE 검정)")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    files.append("fig4_nle_ligand_count_effect.png")
    fig.savefig(OUT_DIR / files[-1])
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.2))
    halves = sorted({h for c in S_COLS for h in hub["ee_by_half_year"][c]})
    for c, col in zip(S_COLS, colors):
        ys = [hub["ee_by_half_year"][c].get(h, {}).get("ee") for h in halves]
        ns = [hub["ee_by_half_year"][c].get(h, {}).get("hubA", 0) + hub["ee_by_half_year"][c].get(h, {}).get("hubB", 0) for h in halves]
        ys = [y if (y is not None and n >= 10) else np.nan for y, n in zip(ys, ns)]
        ax.plot(halves, ys, "o-", color=col, label=S_LABEL[c])
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_ylim(-1.05, 1.05)
    ax.set_ylabel("ee = (B - A)/(B + A)")
    ax.set_title("그림 5. 중심축 우세도: Hub A(도덕·위생) ↔ Hub B(공정·무임승차)\n(반기별, A+B 적중 10건 미만 구간 생략)", fontsize=10)
    ax.legend(ncol=3, fontsize=8, frameon=False)
    fig.tight_layout()
    files.append("fig5_hub_ee_by_half_year.png")
    fig.savefig(OUT_DIR / files[-1])
    plt.close(fig)
    return files


def run_kinetic_analysis() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(KST)
    setup_font()
    df = load()

    print("[Stage 3] 주별 농도 및 VAR/Granger...")
    conc = weekly_concentration(df)
    conc.to_csv(OUT_DIR / "stage3_table_weekly_concentration.csv", encoding="utf-8")
    gr, _, _ = cross_catalysis(conc)
    gr["sensitivity"] = granger_sensitivity(df)
    pd.DataFrame(gr["granger_tests"]).to_csv(OUT_DIR / "stage3_table_granger_fdr.csv", index=False, encoding="utf-8")

    print("[Stage 3] 자가촉매 시그모이드...")
    lf = logistic_fits(df)
    yemen = yemen_episode_fit(df)

    print("[Stage 3] +NLE 회귀...")
    nle = nle_analysis(df)
    nle["_descr"].to_csv(OUT_DIR / "stage3_table_nle_descriptive.csv", index=False, encoding="utf-8")

    print("[Stage 3] 중심축 이동 및 복제...")
    hub = hub_shift(df)
    clone = clone_analysis(df)

    print("[Stage 3] 그림...")
    figs = plot_all(conc, lf, yemen, nle, hub, gr)

    summary = {
        "analysis_timestamp_kst": started.isoformat(timespec="seconds"),
        "input": str(IN_PATH.relative_to(ROOT)),
        "analysis_window": [WINDOW_START, WINDOW_END],
        "design_notes": [
            "농도 H_i(t) = 주별 strict 기질 청원 수 / 주별 전체 청원 수 × 1000",
            "γ_ij = VAR(p)에서 H_j(t) 방정식의 H_i 시차계수 합(p는 AIC 선택). 유의성은 Granger F검정 + BH-FDR(20개 검정).",
            "2019-04 이후는 원천 수집량 급감으로 제외",
            "+NLE: 청원 단위 OLS(log1p 동의수), HC3 표준오차, 길이·월·분류·복제·기질 통제",
            "ee = (Hub B 적중 수 - Hub A 적중 수)/(합), 기질별 부트스트랩 95% CI(2000회)",
            "모든 결과는 규칙 기반 태깅(lexicon v1.1)에 의존하며, 검증 정밀도·재현율은 stage2b_rule_validation.json 참조",
        ],
        "cross_catalytic_gamma": gr,
        "autocatalytic_sigmoid_full_window": lf["fits"],
        "yemen_episode_sigmoid": {k: v for k, v in yemen.items() if not k.startswith("_")},
        "kagan_nonlinear_effect": {k: v for k, v in nle.items() if not k.startswith("_")},
        "catalytic_hub_shift": hub,
        "copy_paste_replication": clone,
        "figures": figs,
        "environment": {
            "python": sys.version.split()[0], "pandas": pd.__version__, "numpy": np.__version__,
            "scipy": scipy.__version__, "statsmodels": statsmodels.__version__, "matplotlib": matplotlib.__version__,
        },
    }
    with (OUT_DIR / "stage3_kinetic_results_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
    print(f"[Stage 3 완료] {OUT_DIR / 'stage3_kinetic_results_summary.json'}")


if __name__ == "__main__":
    run_kinetic_analysis()
