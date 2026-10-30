# 혐오 담론의 교차 촉매와 중심축 이동: 청와대 국민청원 재현 가능 분석 저장소

청와대 국민청원(2017-08 ~ 2019-08, 436,660건)을 원천에서 수집해 보존하고, 5대 혐오 기질과 4대 정당화 리간드를 태깅한 뒤 비선형 동역학 지표를 계산해 논문 초안까지 만드는 전 과정을 단계별로 담았다. 각 단계는 입력·출력 SHA-256과 실행 환경을 담은 provenance 파일을 남기며, 『디지털인문학』(KADH) 논문투고규정 제15조~제21조의 연구데이터 제출 요건을 염두에 두고 구성했다.

## 핵심 결과 (자세한 수치는 `archive_03_analysis_outputs/stage3_kinetic_results_summary.json`)

| 질문 | 결과 |
|---|---|
| 예멘 난민 국면(2018-05~09) S3 누적이 자가촉매 곡선을 따르는가 | 따른다. R²=0.987, 변곡점 2018-06-01 무렵, 일별 정점 2018-06-27(185건) |
| 기질 간 교차 촉매(γ_ij, Granger)가 있는가 | 확인되지 않음. 20개 쌍 모두 FDR q≥0.206. 민감도 분석에서도 결론이 불안정함 |
| 리간드 결합 수에 따라 동의 수가 초선형적으로 늘어나는가(+NLE) | 통제 후에는 확인되지 않음(2계 차분 p=0.221). 다만 리간드 2개 이상의 효과는 비기질 청원보다 기질 청원에서 더 큼(상호작용 p<0.01) |
| 중심축(도덕·위생 A ↔ 공정·무임승차 B) 우세도 ee | S2 성소수자만 A 우세(−0.27). S3·S4·S5는 B 우세(0.34~0.53). S5 중국은 시간이 지나며 B 쪽으로 이동(p<0.001) |
| 규칙 태깅 타당도(검증 표본 60건, 엄격 규칙) | 정밀도 0.909 / 재현율 0.851 / F1 0.879 (AI 보조 주석이므로 인간 검수 필요) |

## 디렉터리

```
stage1_collect_and_archive_raw.py      원천 고정 커밋 수집, 파일별 SHA-256, 품질 점검, RO-Crate
stage2_preprocess_and_tag.py           규칙 태깅(strict/loose), 전 코퍼스 복제 탐지, 주·월 집계, 표본 추출
stage2b_validate_rules.py              검증 표본 P/R/F1, 적대 비율, (LLM 라벨이 있으면) Cohen's κ
stage3_kinetic_analysis.py             VAR/Granger+FDR, 자가촉매 시그모이드, NLE 회귀, ee, 그림 5종
stage4_academic_reproducibility_packager.py   파라데이터 매니페스트, RO-Crate, 재현 ZIP
stage5_export_manuscript_docx.py       논문 초안 md → docx

lexicon/lexicon.json                   기질·리간드 정규식 사전 v1.1 (변경 이력 포함)
annotation/
  validation_dev_sample_lexicon-v1.1.csv       사전 개정용 개발 표본 120건 + 주석
  validation_heldout_sample_lexicon-v1.1.csv   개정 후 독립 검증 표본 60건 + 주석
  wrksai_coder_prompt.md                       웍스AI 에이전트 정밀 주석 프롬프트(Stage 2c, 미실행)
archive_01_raw_petitions/              stage1_raw_provenance.json, ro-crate-metadata.json (원문은 미포함)
archive_02_preprocessed/               태그(원문 제외) parquet, 집계 CSV, 사전 진단, 검증 결과
archive_03_analysis_outputs/           결과 JSON, 표 CSV, 그림 PNG(300dpi)
archive_04_academic_preservation/      파라데이터 매니페스트, RO-Crate (ZIP은 GitHub Release 첨부)
paper/                                 논문 초안 md / docx
assets/fonts/                          그래프용 나눔고딕(SIL OFL)
```

## 재현 방법

```bash
pip install -r requirements.txt
python stage1_collect_and_archive_raw.py --collector "김바로 (한국학중앙연구원)" --compare-hf   # 약 720MB 다운로드
python stage2_preprocess_and_tag.py
python stage2b_validate_rules.py
python stage3_kinetic_analysis.py
python stage5_export_manuscript_docx.py
python stage4_academic_reproducibility_packager.py
```

Stage 1의 파일별 SHA-256이 `archive_01_raw_petitions/stage1_raw_provenance.json`의 `raw_files[].sha256`과 같으면 동일한 원천을 받은 것이다. Stage 2 이후 결과는 고정 시드(20261030)로 결정적으로 생성된다.

## 원 기획 대비 주요 수정

1. 자료 범위: 원천 두 곳 모두 2019-08까지만 수록하므로 "2017~2022"를 실제 범위로 바꾸었다. 2019-04 이후는 수집량이 급감해 시계열 분석에서 제외했다.
2. 원천 선택: Hugging Face 미러는 관리자 수정 고지문(4,633건)과 replies 필드가 삭제되어 있어, GitHub 원천을 사용했다.
3. 사전: 초안에서 깨져 있던 S2 사전을 복원했다. 기질과 리간드에 함께 들어 있던 '역차별'을 정리했고, 과포괄 일반어('범죄', '불법', '공정', '검열')를 제외하거나 한정했다.
4. 복제 탐지: '같은 달·같은 기질 내부' 기준을 전 코퍼스 기준으로 바꾸었다.
5. γ_ij: 월별 OLS(관측 19개)를 주별 VAR + Granger + BH-FDR로 바꾸고, 민감도 분석을 추가했다.
6. +NLE: 단순 평균 비교에 길이·시점·분류·복제를 통제한 회귀와 비기질 청원 대비 상호작용 검정을 추가했다.
7. LLM 주석 프롬프트: "유해발화 가드레일 우회" 목적의 문구를 삭제했다. 대신 연구 목적을 투명하게 고지하고, 출력 스키마를 엄격하게 정의했으며, relevant/hostile 축을 분리했다.
8. 파라데이터: 실행하지 않은 모델이나 단계를 기록하지 않는다. 미실행 단계는 `pending`으로 표기한다.

## 남은 작업 (투고 전)

- `annotation/validation_*.csv`의 `gold_relevant`·`gold_hostile`을 인간 코더가 검수하고, 2인 주석 후 κ를 보고한다.
- 웍스AI 에이전트로 `stage2_llm_batch_input_strat3000.csv`를 주석한다(`annotation/wrksai_coder_prompt.md`). 결과를 `annotation/llm_labels_*.csv`로 저장하고 Stage 2b → 4를 다시 실행한다.
- 국내 논문 저자명을 Crossref 로마자 표기에서 한글 표기로 교체하고, KCI/RISS URI를 보강한다.
- 협의회 공식 docx 양식으로 옮긴다.

## 권리

코드는 MIT 라이선스이다. 파생 데이터·그림·초안은 CC BY-NC-ND 4.0을 따른다(KADH 제21조 준용). 청원 원문은 원천 저장소에 라이선스가 없고 청원인의 권리가 있으므로 이 저장소와 재현 번들에 포함하지 않는다. 예외로, 검증 표본 180건(`annotation/validation_*.csv`)에는 주석 근거를 확인할 수 있도록 제목과 본문 앞 380자 이내의 발췌만 담았다.

## 생성형 AI 활용 고지

이 저장소의 코드, 사전 개정, 검증 표본 1차 주석, 논문 초안은 웍스AI Wrks Coding Agent(Claude Opus 5.5, 2026-10-30)를 활용해 작성했다. 상세 내역은 `archive_04_academic_preservation/KADH_Academic_Paradata_Manifest.json`에 있다. 최종 검증과 학술적 책임은 연구자에게 있다.
