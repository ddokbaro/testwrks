# 혐오 담론의 교차 촉매와 중심축 이동: 청와대 국민청원(2017~2019)의 비선형 동역학 분석

Cross-Catalysis and Core-Axis Shifting in Hate Discourse: A Non-linear Kinetic Analysis of the Cheong Wa Dae National Petitions, 2017–2019

김바로 (한국학중앙연구원)

> [초안 상태 표기] 국내 논문 저자명은 Crossref 메타데이터의 로마자 표기를 그대로 옮겼으며, 한글 성명 확인 후 교체가 필요하다. 이 원고는 Wrks Coding Agent(Claude Opus 5.5)가 저장소의 실행 결과(`archive_03_analysis_outputs/stage3_kinetic_results_summary.json`, `archive_02_preprocessed/stage2b_rule_validation.json`)만을 근거로 작성한 초안이다. 본문의 모든 수치는 해당 파일에서 옮긴 것이다. 투고 전 저자의 해석 검토, 검증 표본의 인간 주석 검수, 웍스AI 에이전트 주석(Stage 2c)의 실행과 반영이 필요하다. 원 기획의 '국회 국민동의청원' 자료와 2019년 9월 이후 청와대 청원은 이번 분석에 포함하지 못했으므로, 제목과 범위를 실제 자료에 맞추어 조정하였다.

## 목차

1. 머리말: 혐오의 대상은 왜 연쇄 이동하는가
2. 이론적 배경: 비대칭 자가촉매와 기질 다중성
 2.1. 소아이 반응과 카강의 비선형 효과의 인문정보학적 전유
 2.2. 교차 촉매 계수(γ_ij)의 정식화와 추정 전략
3. 연구 데이터 및 전처리·보존 파이프라인
 3.1. 청와대 국민청원 43만 6천여 건의 원본 보존과 무결성 검증
 3.2. 5대 기질과 4대 정당화 리간드의 규칙 기반 태깅 및 타당도 검증
4. 실증 분석 결과
 4.1. 기질 농도의 시계열과 교차 촉매 검정
 4.2. 자가촉매 누적 곡선과 조직적 복제
 4.3. 리간드 결합 수와 동의 수의 비선형 증폭 검정
 4.4. 중심축 우세도(ee)와 기질 간 분화
5. 맺음말: 비평형 혐오 생태계와 비판적 디지털 인문학의 과제

## 국문초록

이 연구는 혐오의 표적이 한 집단에서 다른 집단으로 옮겨 가는 현상을 화학 동역학의 은유로 형식화하고, 청와대 국민청원 게시판 원문을 통해 이를 계량적으로 검증하는 것을 목적으로 한다. 연구 범위는 2017년 8월 25일부터 2019년 8월 30일 사이에 청원이 종료된 436,660건이며, 실제 분석에는 수집량이 안정적인 2017년 9월부터 2019년 3월까지의 자료를 사용하였다. 방법으로는 게임·서브컬처, 성소수자, 이슬람·난민, 젠더·장애, 중국의 5대 혐오 '기질'과 도덕·가족, 질병·위생, 공정·무임승차, 안보·주권의 4대 정당화 '리간드'를 규칙 사전으로 태깅하였다. 규칙의 정밀도와 재현율은 독립 검증 표본으로 보고하였다. 이어 주별 기질 농도에 대한 벡터자기회귀(VAR)·Granger 검정, 자가촉매 시그모이드 적합, 청원 단위 회귀, 그리고 '거울상 과잉률(ee)'을 유비한 중심축 우세도 지표를 적용하였다. 분석 결과는 다음과 같다. 첫째, 2018년 제주 예멘 난민 국면의 이슬람·난민 청원 누적은 자가촉매 곡선에 잘 맞았다(R²=0.987). 둘째, 기질 간 교차 촉매는 다중검정 보정 뒤 일관되게 유의하지 않았다. 셋째, 리간드 결합 수와 동의 수 사이에는 단조 증가 관계가 있었으나, 길이와 시점을 통제하면 초선형적 증폭은 확인되지 않았다. 다만 둘 이상의 리간드가 결합한 경우의 효과는 비혐오 청원보다 혐오 기질 청원에서 유의하게 컸다. 넷째, 성소수자 담론만 도덕·위생 축이 우세했고, 이슬람·난민, 젠더, 중국 담론은 공정·무임승차 축이 우세하였다. 중국 담론은 시간이 지날수록 공정 축으로 이동하는 추세를 보였다. 이 결과는 혐오의 '연쇄 이동'이 표적 사이의 직접적 촉매보다는 공통된 정당화 문법의 재배치로 더 잘 설명될 수 있음을 시사한다.

주제어: 혐오 담론, 청와대 국민청원, 교차 촉매, 비선형 효과, 디지털 인문학

## Abstract

This study formalizes the migration of hate targets across social groups through the metaphor of chemical kinetics and tests it quantitatively on the full text of the Cheong Wa Dae (Blue House) national petition board. The corpus comprises 436,660 petitions closed between 25 August 2017 and 30 August 2019; analysis is restricted to September 2017–March 2019, when collection volume was stable. Five hate "substrates" (game/subculture, sexual minorities, Islam/refugees, gender/disability, China) and four justificatory "ligands" (morality/family, disease/hygiene, fairness/free-riding, security/sovereignty) were tagged with a versioned rule lexicon whose precision and recall are reported on an independent validation sample. We applied vector autoregression with Granger tests to weekly substrate concentrations, autocatalytic sigmoid fitting, petition-level regression, and an axis-dominance index analogous to enantiomeric excess (ee). The cumulative Islam/refugee petitions during the 2018 Jeju Yemeni refugee episode closely follow an autocatalytic curve (R² = 0.987), whereas cross-substrate catalysis is not robustly significant after false-discovery-rate correction. Agreement counts increase monotonically with the number of ligands, but no super-linear amplification remains once length and timing are controlled; nevertheless, the two-or-more-ligand effect is significantly larger for hate-substrate petitions than for other petitions. Only the sexual-minority discourse is dominated by the moral/hygiene axis; refugee, gender and China discourses are dominated by the fairness/free-riding axis, and the China discourse shifts further toward it over time. The findings suggest that the apparent migration of hate is better explained by the redeployment of a shared justificatory grammar than by direct catalysis between targets.

Keywords: hate discourse, Cheong Wa Dae petitions, cross-catalysis, nonlinear effect, digital humanities

## 1. 머리말: 혐오의 대상은 왜 연쇄 이동하는가

2017년 8월 문을 연 청와대 국민청원 게시판은 시민이 국가 최고 권력에 직접 말을 건넬 수 있는 통로로 설계되었다. 동시에 이 게시판은 특정 집단을 겨냥한 배제와 비하의 요구가 공적 언어의 형식을 빌려 축적되는 장소이기도 했다. 2018년 6월 제주 예멘 난민 수용 반대 청원이 단기간에 폭증한 사례는 그 가장 가시적인 사례이다. 같은 시기 게시판에서는 여성가족부 폐지, 동성애·퀴어문화축제 반대, 조선족과 외국인 건강보험 문제를 겨냥한 청원도 잇따랐다. 관찰자에게 이 흐름은 혐오가 하나의 표적에서 다음 표적으로 '번져 가는' 모습으로 보이기 쉽다.

이 연구는 그 인상을 검증 가능한 질문으로 바꾸고자 한다. 하나의 표적에 대한 혐오가 커지면 다른 표적에 대한 혐오가 뒤따라 커지는가. 혐오 청원이 동원하는 정당화 논리가 여러 겹으로 결합할수록 공감은 단순 합산을 넘어 비선형적으로 증폭되는가. 그리고 서로 다른 표적을 향한 혐오는 같은 정당화 논리를 공유하는가, 아니면 표적마다 고유한 논리 축을 가지는가. 이 질문들을 다루기 위해 연구는 비대칭 자가촉매와 비선형 효과라는 화학의 개념을 분석 틀로 빌려 온다. 이는 은유를 실체로 착각하기 위한 것이 아니다. 은유가 요구하는 검증 조건을 명시함으로써 은유의 설명력이 어디까지 유효한지를 판정하려는 것이다.

청와대 국민청원을 다룬 기존 연구는 주로 참여 동기와 정치적 효능감, 청원의 주제 구조와 정부 응답의 수사를 분석하였다.1) 2018년 예멘 난민 사태를 다룬 연구들은 신문 기사의 은유, 포털 댓글의 텍스트 마이닝, 혐오 표현의 정치화 문제를 각각 검토하였다.2) 한국어 혐오 표현을 자동 탐지하기 위한 말뭉치 구축 연구도 활발히 진행되었다.3) 그러나 서로 다른 혐오 표적 사이의 시간적 연동과 정당화 논리의 공유 구조를 하나의 코퍼스 안에서 함께 측정한 연구는 드물다. 이 연구는 청원 원문 43만여 건을 바이트 단위로 보존한 뒤 그 위에서 이 공백을 다룬다.

## 2. 이론적 배경: 비대칭 자가촉매와 기질 다중성

### 2.1. 소아이 반응과 카강의 비선형 효과의 인문정보학적 전유

Frank는 1953년 거울상 이성질체 가운데 하나가 자기 자신의 생성을 촉진하고 다른 하나의 생성을 억제하면, 처음의 미세한 비대칭이 자발적으로 증폭될 수 있다는 모형을 제시하였다.4) 이 이론적 가능성은 1995년 소아이(Soai) 연구진이 피리미딜 알칸올의 비대칭 자가촉매 반응에서 거울상 과잉률이 반응을 거듭할수록 증폭되는 현상을 실험으로 보이면서 실증되었다.5) 한편 카강(Kagan) 연구진은 1986년 키랄 보조 리간드의 광학 순도와 생성물의 광학 순도가 선형 관계를 벗어나는 '비선형 효과(nonlinear effect, NLE)'를 보고하였다. 이후 이 현상은 리간드들이 단량체가 아닌 응집체로 촉매에 참여하기 때문이라는 해석과 함께 체계화되었다.6)

이 연구가 이 개념들에서 빌려 오는 것은 세 가지 검증 가능한 명제이다. 첫째, 자가촉매 명제이다. 어떤 기질에 대한 청원의 누적 증가 속도가 이미 누적된 양에 비례해 빨라졌다가 포화된다면, 그 누적 곡선은 선형보다 로지스틱형 자가촉매 곡선에 더 잘 맞아야 한다. 둘째, 비선형 증폭 명제이다. 청원이 동원하는 정당화 논리(리간드)가 여러 겹으로 결합할 때 공감(동의 수)이 결합 수에 대해 초선형적으로 증가한다면, 결합 수에 따른 효과의 2계 차분은 양(+)이어야 한다. 셋째, 거울상 과잉률의 유비이다. 서로 경쟁하는 두 정당화 축 가운데 어느 쪽이 우세한지를 ee = (B − A)/(B + A)로 요약할 수 있다. 이 값의 기질별 차이와 시간에 따른 변화는 '중심축 이동'의 직접적인 지표가 된다.

### 2.2. 교차 촉매 계수(γ_ij)의 정식화와 추정 전략

효소 연구에서 기질 다중성(substrate promiscuity)은 하나의 효소가 본래 기질 외의 다른 기질에도 촉매 활성을 보이는 현상을 가리킨다.7) 이 연구는 혐오를 생성하는 사회적 '촉매'가 특정 표적에 고정되지 않고 다른 표적으로 활성을 옮길 수 있다는 가설을 이 개념에 기대어 정식화한다. 기질 j의 농도를 H_j(t)라 하면, 원 설계의 다중 파동 연립 미분방정식은 dH_j/dt = k_j H_j (1 − H_j/K_j) + Σ_{i≠j} γ_ij H_i H_j 형태로 쓸 수 있다. 여기서 γ_ij는 기질 i가 기질 j의 성장을 촉진(+)하거나 억제(−)하는 교차 촉매 계수이다.

관측 자료로 이 계수를 식별하기 위해 연구는 이산 시간 근사를 택한다. 주별 농도의 로그 변환 계열에 벡터자기회귀모형 VAR(p)를 적합하고, j 방정식에서 i의 시차계수 합을 γ_ij의 추정치로 삼는다.8) 교차 촉매의 존재 여부는 Granger 인과 검정으로 판정한다.9) 기질 쌍 20개를 동시에 검정하므로 Benjamini–Hochberg 방법으로 거짓발견률(FDR)을 통제한다.10) 원 설계의 월별 최소제곱 회귀는 관측치 19개로 6개 계수를 추정해야 하는 자유도 문제가 있었다. 그래서 주별 자료와 다중검정 보정으로 설계를 바꾸었다.

## 3. 연구 데이터 및 전처리·보존 파이프라인

### 3.1. 청와대 국민청원 43만 6천여 건의 원본 보존과 무결성 검증

자료는 lovit(Kim, Hyunjoong)이 청와대 국민청원 게시판에서 청원 종료 건을 월별로 수집해 공개한 저장소를 원천으로 삼았다.11) 재현성을 위해 저장소의 특정 커밋(03dc3f3d)에 고정해 월별 JSONL 25개 파일을 바이트 그대로 보존하였고, 파일마다 SHA-256 해시를 기록하였다. 수집된 청원은 436,660건이며 청원 번호 중복과 필수 필드 결측은 없었다. 다만 수록 범위는 청원 시작일 기준 2017년 8월 25일부터 2019년 8월 30일까지로, 게시판 운영 종료 시점(2022년 5월)까지를 포괄하지 않는다. 또 2019년 4월 이후에는 월 수집량이 수백 건으로 급감하므로, 시계열 분석의 창은 2017년 9월 4일부터 2019년 3월 31일까지로 제한하였다.

같은 자료의 Hugging Face 재배포본(heegyu/korean-petitions)과 레코드 단위로 전수 대조한 결과, 청원 집합은 같았다. 그러나 재배포본에서는 4,633건의 본문에 붙어 있던 "[본 게시물의 일부 내용이 국민 청원 요건에 위배되어 관리자에 의해 수정되었습니다]"라는 관리자 고지문이 삭제되어 있었고, 원천에 있던 replies 필드도 제거되어 있었다. 관리자 개입의 흔적은 혐오 청원 연구에서 그 자체로 의미 있는 정보이므로, 이 연구는 원천 저장소만을 사용하고 대조 결과를 원본 보존 증명서에 함께 기록하였다. 보존 메타데이터는 RO-Crate 1.1 규격으로 작성하였다.12)

### 3.2. 5대 기질과 4대 정당화 리간드의 규칙 기반 태깅 및 타당도 검증

기질과 리간드는 버전 관리되는 정규식 사전(lexicon v1.1)으로 태깅하였다. 사전 설계에서는 두 가지 원칙을 지켰다. 첫째, 기질 사전과 리간드 사전에 같은 어휘를 두지 않았다. 예를 들어 원 설계에서 '역차별'은 젠더 기질과 공정 리간드 양쪽에 들어 있었는데, 이렇게 두면 기질과 리간드의 결합이 정의상 생겨 버리는 순환이 발생하므로 리간드 쪽에만 남겼다. 둘째, 코퍼스 전체에서 비특이적으로 대량 적중하는 일반어는 제외하거나 한정형으로 좁혔다. '범죄'(32,404건), '불법'(22,044건), 단독형 '공정'(14,109건), 단독형 '검열'(862건) 등이 이에 해당한다. 장문 청원에서 지나가듯 한 번 언급된 경우를 거르기 위해, 제목에서 적중하거나 본문에서 2회 이상 적중한 경우만 기질 양성으로 판정하는 엄격 규칙을 주 분석에 사용하였다. 1회 적중 기준(느슨 규칙)은 민감도 분석에 사용하였다.

엄격 규칙에 따른 기질 청원은 16,298건이었다. 기질별로는 S1 게임·서브컬처 656건, S2 성소수자 1,126건, S3 이슬람·난민 6,781건, S4 젠더·장애 7,249건, S5 중국 1,537건이었다. 장애인 이동권 시위 관련 어휘('전장연', '지하철 시위')는 2021년 이후의 사건이어서 이 코퍼스에서 거의 적중하지 않았다. 따라서 S4는 사실상 젠더 기질로 해석해야 한다.

규칙의 타당도는 사전 개정에 사용한 개발 표본 120건과, 개정 뒤 별도 시드로 추출한 검증 표본 60건으로 평가하였다. 두 표본에는 각 기질 양성, 느슨 규칙에서만 양성, 음성 청원이 층화되어 포함되었다. 각 청원에 대해 해당 집단이 청원의 실질 주제인지(relevant)와 해당 집단에 대한 배제·비하·권리 제한 요구가 있는지(hostile)를 따로 주석하였다. 검증 표본에서 엄격 규칙의 미시 평균 정밀도는 0.909, 재현율은 0.851, F1은 0.879였다. 기질별 F1은 S1 0.941, S2 0.941, S3 0.762, S4 0.778, S5 1.000이었다. 개발 표본의 결과(정밀도 0.909, 재현율 0.825)와도 큰 차이가 없었다. 한편 규칙 양성 청원 가운데 적대적 청원의 비율은 기질마다 크게 달랐다. 검증 표본 기준으로 S1은 0.0, S2는 0.625, S3는 0.800, S4는 0.667, S5는 0.889였다. 즉 S1 청원의 대부분은 게임 규제(셧다운제)에 반대하는 청원이지 게이머나 서브컬처 향유자를 겨냥한 혐오가 아니었다. 이후의 모든 결과는 '혐오 청원'이 아니라 '혐오 표적이 되는 집단을 주제로 한 청원'에 대한 것으로 읽어야 한다. 현재 주석은 연구 보조에 사용한 생성형 AI가 1차로 부여한 것이며, 인간 코더의 검수를 거쳐 확정해야 한다는 한계가 있다.13)

조직적 자기복제는 본문에서 한글·영문·숫자 이외의 문자를 제거한 정규형을 기준으로 측정하였다. 정규형 전체가 같거나 앞 100자가 같은 청원이 전 코퍼스에서 3건 이상이면 복제 청원으로 판정하였다. 원 설계는 '같은 달·같은 기질' 안에서만 복제를 찾았는데, 이 방식은 월 경계를 넘거나 다른 주제로 분류된 복제를 놓치므로 전 코퍼스 기준으로 바꾸었다.

## 4. 실증 분석 결과

### 4.1. 기질 농도의 시계열과 교차 촉매 검정

주별 기질 농도(전체 청원 1,000건당 기질 청원 수)는 81주 동안 측정되었다(그림 1). 성소수자와 이슬람·난민 농도는 단위근 검정에서 정상성을 기각하지 못했으므로, 다섯 계열 모두에 로그 차분을 적용하였다. AIC로 선택한 시차는 4주였고 추정된 VAR 모형은 안정적이었다. 시차계수 합으로 계산한 γ_ij 가운데 가장 큰 양의 값은 S3→S2(0.774), S2→S3(1.253), S2→S1(1.344)이었다. 그러나 Granger 검정 20개에 FDR 보정을 적용한 뒤에는 어떤 쌍도 유의하지 않았다(최소 q=0.206). 보정 전 p값이 가장 작았던 것은 S3→S2(p=0.012), S3→S4(p=0.021), S5→S3(p=0.032)였다(그림 2).

민감도 분석은 이 결론이 모형 설정에 따라 흔들린다는 점을 보여준다. 시차를 1주로 고정하면 S1→S4 한 쌍만 FDR 기준을 통과하였고(q=0.042), 느슨 규칙으로 농도를 다시 계산하면 유의한 쌍이 하나도 없었다. 따라서 이 자료에서 '한 표적에 대한 청원의 증가가 다른 표적에 대한 청원의 증가를 체계적으로 선행한다'는 의미의 교차 촉매는 확인되지 않는다고 보는 것이 신중하다. 이는 표적 간 연동이 없다는 뜻이 아니다. 아래 4.4절에서 보듯 표적 사이의 연결은 시간적 선후보다 단일 청원 안의 공동 출현과 정당화 논리의 공유로 드러난다.

### 4.2. 자가촉매 누적 곡선과 조직적 복제

전체 분석 창의 일별 누적 청원 수에 자가촉매 시그모이드를 적합하였다. S1, S2, S3, S5에서는 선형 모형보다 AIC가 크게 낮았고(ΔAIC 713~1,614), S4는 선형 모형이 오히려 약간 나았다(ΔAIC −26.9). 젠더 기질 청원은 2년 가까운 기간 동안 비교적 일정한 속도로 누적된 반면, 다른 기질은 특정 국면에 집중적으로 늘었다가 포화되는 양상을 보인 것이다.

자가촉매 명제에 가장 잘 들어맞는 사례는 2018년 제주 예멘 난민 국면이었다. 2018년 5월부터 9월까지 S3 청원의 일별 누적에 같은 곡선을 적합하면 결정계수는 0.987이었고, 변곡점은 2018년 6월 1일 무렵으로 추정되었다(그림 3). 일별 S3 청원은 2018년 6월 27일 185건으로 정점에 이르렀다. 다만 누적 곡선이 로지스틱 형태를 띤다는 사실만으로 '이미 올라온 청원이 다음 청원을 부른다'는 자가촉매 기제가 입증되지는 않는다. 언론 보도와 같은 외부 충격이 한 번 주어지고 관심이 감쇠하는 과정도 같은 형태의 곡선을 만들 수 있기 때문이다.

조직적 복제의 비율은 표적마다 달랐다. 분석 창 전체의 복제율은 6.13%였고 비기질 청원의 복제율도 6.11%로 거의 같았다. 기질별로 보면 젠더(11.2%, 전체 대비 1.83배), 성소수자(8.65%, 1.41배), 중국(7.57%, 1.23배)은 평균보다 높았다. 반면 이슬람·난민(2.65%, 0.43배)과 게임(5.26%)은 평균보다 낮았다. 예멘 난민 국면의 폭증이 같은 문안의 반복이 아니라 서로 다른 문안의 동시다발적 작성으로 이루어졌다는 점은, 이 국면을 소수의 조직적 동원만으로 설명하기 어렵다는 것을 보여준다.

### 4.3. 리간드 결합 수와 동의 수의 비선형 증폭 검정

분석 창 안의 엄격 기질 청원 16,208건에서 리간드 결합 수에 따른 평균 동의 수는 0개 263건, 1개 232건, 2개 368건, 3개 1,113건, 4개 2,241건으로 가파르게 증가하였다. 그러나 결합 수가 많은 청원은 본문 중앙값이 0개 292자, 2개 1,538자, 4개 13,844자로 훨씬 길었다. 긴 글일수록 여러 리간드 어휘가 우연히 적중할 가능성도 커진다. 따라서 이 증가를 그대로 비선형 증폭으로 읽을 수는 없다.

동의 수에 1을 더해 로그를 취한 값을 종속변수로 하고 본문 길이(로그), 복제 여부, 월·청원 분류 고정효과, 기질 지시변수를 통제한 회귀에서, 리간드 0개 대비 효과는 1개 0.138, 2개 0.355, 3개 이상 0.325였다(HC3 강건 표준오차, 3개 이상은 p=0.064). 증분은 0→1에서 0.138, 1→2에서 0.217로 커졌다가 2→3에서 −0.030으로 사라졌다. 2계 차분 검정(b₃ − 2b₂ + b₁)은 −0.246으로 유의하지 않았고(p=0.221), 2차항 모형의 제곱항도 0.007로 유의하지 않았다(p=0.780). 동의 1,000건 이상 여부를 종속변수로 한 로지스틱 회귀에서도 리간드 결합 수의 오즈비는 모두 유의하지 않았다(그림 4). 요컨대 통제 후에도 리간드 결합과 공감 사이에는 완만한 단조 관계가 있지만, 카강의 비선형 효과에 대응하는 초선형적 증폭은 확인되지 않는다.

그런데 같은 모형을 분석 창 전체 432,313건에 적합하고 리간드 결합 수와 기질 여부의 상호작용을 넣으면 다른 그림이 나타난다. 리간드 1개의 효과는 기질 청원과 비기질 청원에서 차이가 없었다(상호작용 0.011, p=0.649). 그러나 2개의 효과는 기질 청원에서 0.205만큼 더 컸고(p<0.001), 3개 이상에서는 0.660만큼 더 컸다(p=0.001). 비기질 청원에서는 리간드가 3개 이상 결합하면 오히려 동의 수가 줄었는데(−0.393), 혐오 기질 청원에서는 그렇지 않았다. 정당화 논리를 여러 겹 쌓는 수사가 일반 청원에서는 공감을 얻지 못하지만, 혐오 표적을 다루는 청원에서는 상대적으로 공감을 잃지 않는다는 뜻이다. 이를 비선형 증폭의 약한 형태로 해석할 여지가 있으나, 인과적 해석에는 추가 검증이 필요하다.

### 4.4. 중심축 우세도(ee)와 기질 간 분화

도덕·가족 또는 질병·위생 리간드를 Hub A로, 공정·무임승차 리간드를 Hub B로 두고 기질별 ee = (B − A)/(B + A)를 계산하였다(부트스트랩 95% 신뢰구간). 성소수자 기질만이 음의 값, 곧 도덕·위생 축 우세를 보였다(ee=−0.275, [−0.347, −0.205]). 성소수자 청원의 Hub A 적중률은 29.0%로 다른 기질(2.9~7.1%)보다 훨씬 높았다. 특히 질병·위생 리간드가 20.6%로 두드러졌다. 반대로 이슬람·난민(ee=0.528, [0.472, 0.584]), 중국(0.371, [0.272, 0.464]), 젠더(0.337, [0.290, 0.382])는 모두 공정·무임승차 축이 우세하였다. 게임은 0.156([0.000, 0.306])으로 경계에 있었다. 안보·주권 리간드는 거의 모든 기질에서 가장 흔한 리간드였다(20.7~27.1%, 게임 14.1%). 이는 '안보' 논리가 어느 한 축에 귀속되기보다 표적을 가리지 않는 범용 정당화로 기능함을 시사한다.

시간에 따른 이동은 기질마다 방향이 달랐다(그림 5). Hub A와 Hub B 중 하나만 적중한 청원에서 Hub B일 확률을 월 단위 시간에 회귀한 결과, 중국 기질은 월 0.111씩 공정 축 쪽으로 이동하였다(p<0.001). ee는 2017년 하반기 −0.234에서 2018년 하반기 0.559로 부호가 바뀌었다. 반대로 성소수자(−0.070, p=0.004)와 젠더(−0.026, p=0.035)는 도덕·위생 축 쪽으로 이동하였다. 이슬람·난민은 처음부터 공정 축이 우세했고 유의한 추세가 없었다(p=0.494). 따라서 원 가설이 상정한 '보수 개신교 윤리 축에서 청년 능력주의 축으로의 일방향 중심축 이동'은 이 자료에서 전체 담론 수준의 경향으로는 확인되지 않는다. 그 대신 표적에 따라 축이 분화하는 양상이 나타났으며, 중국 담론에서만 그 방향의 이동이 뚜렷했다.

두 축이 한 청원 안에서 함께 쓰이는 '혼성 연합(Hub C)'의 비율은 성소수자(5.2%)와 게임(2.9%)에서 높고 이슬람·난민(0.7%)에서 가장 낮았다. 기질 간 차이는 유의하였다(χ²=144.9, 자유도 4, p<0.001). 원 가설은 중국 담론을 두 축의 합류점으로 보았다. 그러나 중국 기질의 Hub C 비율(1.45%)은 나머지 기질 전체에 비해 오즈비 1.44로 높았을 뿐 유의하지 않았다(Fisher 정확검정 p=0.112). 반면 기질 간 공동 출현에서는 중국과 이슬람·난민의 결합이 423건으로 가장 많았다. 다음으로는 성소수자와 이슬람·난민(191건), 게임과 젠더(174건)의 결합이 많았다. 혐오 표적 사이의 연결은 시간적 선후(4.1절)보다 한 청원 안에서 '외국인'이라는 상위 범주로 묶이는 방식(중국–난민)과, 여성가족부라는 공통의 제도적 표적을 매개로 묶이는 방식(게임–젠더)으로 더 분명히 나타난다.

## 5. 맺음말: 비평형 혐오 생태계와 비판적 디지털 인문학의 과제

이 연구는 혐오 표적의 연쇄 이동이라는 인상을 화학 동역학의 은유로 형식화하고, 은유가 요구하는 검증 조건을 청원 원문 43만여 건에 적용하였다. 결과는 은유의 설명력이 부분적임을 보여준다. 예멘 난민 국면의 누적 곡선은 자가촉매 곡선과 잘 맞았다. 그러나 표적 사이의 교차 촉매는 다중검정 보정과 민감도 분석을 통과하지 못하였다. 정당화 논리의 결합은 공감과 단조적으로 연관되었지만 초선형적 증폭은 확인되지 않았고, 혐오 표적 청원과 일반 청원 사이의 상호작용에서만 약한 증폭의 흔적이 남았다. 가장 분명한 결과는 표적에 따라 정당화 축이 분화한다는 점이다. 성소수자 담론은 도덕·위생 축에, 난민·중국·젠더 담론은 공정·무임승차 축에 기대었다. 중국 담론은 관찰 기간 동안 공정 축 쪽으로 이동하였다.

이 결과는 혐오가 '옮겨 간다'고 말할 때 실제로 옮겨 가는 것이 무엇인지를 다시 묻게 한다. 이 자료에서 옮겨 다니는 것은 표적 자체라기보다 '세금', '특혜', '역차별', '안보'와 같이 어떤 표적에든 결합할 수 있는 정당화의 문법이다. 그렇다면 혐오에 대한 대응 역시 표적별 대응을 넘어, 표적을 가리지 않고 재사용되는 정당화 문법을 분석하고 비판하는 방향으로 확장되어야 한다.

이 연구에는 분명한 한계가 있다. 자료는 게시판 운영 기간의 앞쪽 2년에 그치고, 2019년 4월 이후는 수집이 불완전하다. 국회 국민동의청원 자료는 다루지 못했다. 태깅은 규칙 사전에 의존하며, 그 타당도 평가에 사용한 주석은 생성형 AI가 1차로 부여한 것이어서 인간 코더의 검수가 필요하다. 동의 수는 청원 내용뿐 아니라 언론 노출, 커뮤니티 공유, 게시판의 노출 알고리즘에 좌우되지만, 이 연구는 이를 관측하지 못하였다. 마지막으로 화학의 개념을 사회 현상에 옮기는 일은 그 자체로 위험을 수반한다. 이 연구의 은유는 검증 가능한 가설을 생성하는 장치로만 사용되었으며, 혐오를 자연법칙처럼 필연적인 과정으로 묘사하려는 것이 아니다.

## 연구데이터 및 생성형 AI 활용 고지

이 논문의 연구데이터는 GitHub 저장소 ddokbaro/testwrks에 단계별 스크립트, 규칙 사전, 검증 주석, 분석 결과, 재현성 보존 패키지와 함께 공개되어 있다(KADH 논문투고규정 제16조~제19조). 청원 원문은 원천 저장소에 라이선스가 명시되어 있지 않고 청원인의 저작권과 개인정보 문제가 있으므로 재배포하지 않는다. 대신 원천 저장소의 커밋과 파일별 SHA-256 해시로 동일 자료를 재수집해 검증할 수 있도록 하였다.

연구 과정에서 한국학중앙연구원 웍스AI의 코딩 에이전트(Wrks Coding Agent, 기반 모델 Claude Opus 5.5)를 보조적으로 활용하였다. 활용 범위는 파이프라인 코드의 작성·수정·실행, 규칙 사전의 개정 제안, 검증 표본 180건의 1차 주석, 통계 결과의 요약, 초고 문장의 작성이다. 웍스AI '나만의 에이전트'를 이용한 층화 표본 3,000건의 정밀 주석은 설계와 프롬프트만 마련된 상태이며 이 초안의 결과에는 반영되지 않았다. 모든 원천 데이터의 대조, 분석 설계와 해석의 타당성 검증, 그리고 최종 학술적 책임은 저자에게 있다. 사용한 모델과 일시, 역할 분담은 재현성 보존 패키지의 파라데이터 매니페스트(KADH_Academic_Paradata_Manifest.json)에 기록하였다.

## 미주

1) Song, Junmo; Park, Youngdeuk (2019). "청와대 국민청원에서는 무엇이 일어나는가? : 자연어 처리를 활용한 청와대 국민청원 분석". <한국정치학회보>. https://doi.org/10.18854/kpsr.2019.53.5.003 ; Lee, Seungwon; Lim, Hansaem; Lee, Hyeon Woo (2018). "청와대 국민청원 참여요인 분석". <OUGHTOPIA>. https://doi.org/10.32355/oughtopia.2018.11.33.3.111 ; Yang, Hyejin; Ahn, Jungmin; Lee, Taehun (2021). "텍스트 빅데이터 분석을 통한 한국인의 불공정 경험 분석: 국민청원 게시판 데이터 분석 결과를 중심으로". <조사연구>. https://doi.org/10.20997/sr.22.1.2

2) Jeong, Da-Som; Kwon, Soon-Hee (2019). "신문기사에 나타난 '난민' 관련 은유 표현 연구: 제주도 이주 예멘 난민 기사를 중심으로". <한국어 의미학>. https://doi.org/10.19033/sks.2019.3.63.1 ; Kang, Jingu; Lee, Ki-seong (2019). "텍스트마이닝(Text Minning)을 통해 본 제주 예멘 난민: 네이버 뉴스 댓글을 중심으로". <다문화콘텐츠연구>. https://doi.org/10.15400/mccs.2019.04.30.103 ; Youn, Eun-Joo (2022). "정치화된 혐오 표현에 대한 비판: 제주 예멘 난민 사건을 중심으로". <한국여성철학>. https://doi.org/10.17316/kfp.2022.5.37.1

3) Moon, Jihyung; Cho, Won Ik; Lee, Junbum (2020). "BEEP! Korean Corpus of Online News Comments for Toxic Speech Detection." Proceedings of the Eighth International Workshop on Natural Language Processing for Social Media. https://doi.org/10.18653/v1/2020.socialnlp-1.4 ; Jeong, Younghoon; Oh, Juhyun; Lee, Jongwon; Ahn, Jaimeen; Moon, Jihyung; Park, Sungjoon; Oh, Alice (2022). "KOLD: Korean Offensive Language Dataset." Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing. https://doi.org/10.18653/v1/2022.emnlp-main.744 ; Lee, Jean; Lim, Taejun; Lee, Heejun; Jo, Bogeun; Kim, Yangsok; Yoon, Heegeun; Han, Soyeon Caren (2022). "K-MHaS: A Multi-label Hate Speech Detection Dataset in Korean Online News Comment." Proceedings of the 29th International Conference on Computational Linguistics. https://aclanthology.org/2022.coling-1.311/

4) Frank, F. C. (1953). "On Spontaneous Asymmetric Synthesis." Biochimica et Biophysica Acta. https://doi.org/10.1016/0006-3002(53)90082-1

5) Soai, Kenso; Shibata, Takanori; Morioka, Hiroshi; Choji, Kaori (1995). "Asymmetric Autocatalysis and Amplification of Enantiomeric Excess of a Chiral Molecule." Nature. https://doi.org/10.1038/378767a0

6) Puchot, C.; Samuel, O.; Duñach, E.; Zhao, S.; Agami, C.; Kagan, H. B. (1986). "Nonlinear Effects in Asymmetric Synthesis. Examples in Asymmetric Oxidations and Aldolization Reactions." Journal of the American Chemical Society. https://doi.org/10.1021/ja00269a036 ; Girard, Christian; Kagan, Henri B. (1998). "Nonlinear Effects in Asymmetric Synthesis and Stereoselective Reactions: Ten Years of Investigation." Angewandte Chemie International Edition. https://doi.org/10.1002/(SICI)1521-3773(19981116)37:21<2922::AID-ANIE2922>3.0.CO;2-1

7) Khersonsky, Olga; Tawfik, Dan S. (2010). "Enzyme Promiscuity: A Mechanistic and Evolutionary Perspective." Annual Review of Biochemistry. https://doi.org/10.1146/annurev-biochem-030409-143718

8) Sims, Christopher A. (1980). "Macroeconomics and Reality." Econometrica. https://doi.org/10.2307/1912017

9) Granger, C. W. J. (1969). "Investigating Causal Relations by Econometric Models and Cross-spectral Methods." Econometrica. https://doi.org/10.2307/1912791

10) Benjamini, Yoav; Hochberg, Yosef (1995). "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing." Journal of the Royal Statistical Society Series B. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

11) lovit (Kim, Hyunjoong). "청와대 국민청원 데이터 아카이브". https://github.com/lovit/petitions_archive

12) Soiland-Reyes, Stian; Sefton, Peter; Crosas, Mercè; Castro, Leyla Jael; Coppens, Frederik; Fernández, José M.; Garijo, Daniel; Grüning, Björn; La Rosa, Marco; Leo, Simone; Ó Carragáin, Eoghan; Portier, Marc; Trisovic, Ana; RO-Crate Community; Groth, Paul; Goble, Carole (2022). "Packaging Research Artefacts with RO-Crate." Data Science. https://doi.org/10.3233/DS-210053 ; Wilkinson, Mark D. et al. (2016). "The FAIR Guiding Principles for Scientific Data Management and Stewardship." Scientific Data. https://doi.org/10.1038/sdata.2016.18

13) Gilardi, Fabrizio; Alizadeh, Meysam; Kubli, Maël (2023). "ChatGPT Outperforms Crowd Workers for Text-annotation Tasks." Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.2305016120 ; Cohen, Jacob (1960). "A Coefficient of Agreement for Nominal Scales." Educational and Psychological Measurement. https://doi.org/10.1177/001316446002000104

## 참고문헌

Kang, Jingu; Lee, Ki-seong (2019). "텍스트마이닝(Text Minning)을 통해 본 제주 예멘 난민: 네이버 뉴스 댓글을 중심으로". <다문화콘텐츠연구>. https://doi.org/10.15400/mccs.2019.04.30.103

lovit (Kim, Hyunjoong). "청와대 국민청원 데이터 아카이브". https://github.com/lovit/petitions_archive

Song, Junmo; Park, Youngdeuk (2019). "청와대 국민청원에서는 무엇이 일어나는가? : 자연어 처리를 활용한 청와대 국민청원 분석". <한국정치학회보>. https://doi.org/10.18854/kpsr.2019.53.5.003

Yang, Hyejin; Ahn, Jungmin; Lee, Taehun (2021). "텍스트 빅데이터 분석을 통한 한국인의 불공정 경험 분석: 국민청원 게시판 데이터 분석 결과를 중심으로". <조사연구>. https://doi.org/10.20997/sr.22.1.2

Youn, Eun-Joo (2022). "정치화된 혐오 표현에 대한 비판: 제주 예멘 난민 사건을 중심으로". <한국여성철학>. https://doi.org/10.17316/kfp.2022.5.37.1

Lee, Seungwon; Lim, Hansaem; Lee, Hyeon Woo (2018). "청와대 국민청원 참여요인 분석". <OUGHTOPIA>. https://doi.org/10.32355/oughtopia.2018.11.33.3.111

Jeong, Da-Som; Kwon, Soon-Hee (2019). "신문기사에 나타난 '난민' 관련 은유 표현 연구: 제주도 이주 예멘 난민 기사를 중심으로". <한국어 의미학>. https://doi.org/10.19033/sks.2019.3.63.1

Benjamini, Yoav; Hochberg, Yosef (1995). "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing." Journal of the Royal Statistical Society Series B. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

Cohen, Jacob (1960). "A Coefficient of Agreement for Nominal Scales." Educational and Psychological Measurement. https://doi.org/10.1177/001316446002000104

Frank, F. C. (1953). "On Spontaneous Asymmetric Synthesis." Biochimica et Biophysica Acta. https://doi.org/10.1016/0006-3002(53)90082-1

Gilardi, Fabrizio; Alizadeh, Meysam; Kubli, Maël (2023). "ChatGPT Outperforms Crowd Workers for Text-annotation Tasks." Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.2305016120

Girard, Christian; Kagan, Henri B. (1998). "Nonlinear Effects in Asymmetric Synthesis and Stereoselective Reactions: Ten Years of Investigation." Angewandte Chemie International Edition. https://doi.org/10.1002/(SICI)1521-3773(19981116)37:21<2922::AID-ANIE2922>3.0.CO;2-1

Granger, C. W. J. (1969). "Investigating Causal Relations by Econometric Models and Cross-spectral Methods." Econometrica. https://doi.org/10.2307/1912791

Jeong, Younghoon; Oh, Juhyun; Lee, Jongwon; Ahn, Jaimeen; Moon, Jihyung; Park, Sungjoon; Oh, Alice (2022). "KOLD: Korean Offensive Language Dataset." Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing. https://doi.org/10.18653/v1/2022.emnlp-main.744

Khersonsky, Olga; Tawfik, Dan S. (2010). "Enzyme Promiscuity: A Mechanistic and Evolutionary Perspective." Annual Review of Biochemistry. https://doi.org/10.1146/annurev-biochem-030409-143718

Lee, Jean; Lim, Taejun; Lee, Heejun; Jo, Bogeun; Kim, Yangsok; Yoon, Heegeun; Han, Soyeon Caren (2022). "K-MHaS: A Multi-label Hate Speech Detection Dataset in Korean Online News Comment." Proceedings of the 29th International Conference on Computational Linguistics. https://aclanthology.org/2022.coling-1.311/

Moon, Jihyung; Cho, Won Ik; Lee, Junbum (2020). "BEEP! Korean Corpus of Online News Comments for Toxic Speech Detection." Proceedings of the Eighth International Workshop on Natural Language Processing for Social Media. https://doi.org/10.18653/v1/2020.socialnlp-1.4

Puchot, C.; Samuel, O.; Duñach, E.; Zhao, S.; Agami, C.; Kagan, H. B. (1986). "Nonlinear Effects in Asymmetric Synthesis. Examples in Asymmetric Oxidations and Aldolization Reactions." Journal of the American Chemical Society. https://doi.org/10.1021/ja00269a036

Sims, Christopher A. (1980). "Macroeconomics and Reality." Econometrica. https://doi.org/10.2307/1912017

Soai, Kenso; Shibata, Takanori; Morioka, Hiroshi; Choji, Kaori (1995). "Asymmetric Autocatalysis and Amplification of Enantiomeric Excess of a Chiral Molecule." Nature. https://doi.org/10.1038/378767a0

Soiland-Reyes, Stian; Sefton, Peter; Crosas, Mercè; Castro, Leyla Jael; Coppens, Frederik; Fernández, José M.; Garijo, Daniel; Grüning, Björn; La Rosa, Marco; Leo, Simone; Ó Carragáin, Eoghan; Portier, Marc; Trisovic, Ana; RO-Crate Community; Groth, Paul; Goble, Carole (2022). "Packaging Research Artefacts with RO-Crate." Data Science. https://doi.org/10.3233/DS-210053

Wilkinson, Mark D. et al. (2016). "The FAIR Guiding Principles for Scientific Data Management and Stewardship." Scientific Data. https://doi.org/10.1038/sdata.2016.18

## 그림

그림 1. archive_03_analysis_outputs/fig1_weekly_substrate_concentration.png
그림 2. archive_03_analysis_outputs/fig2_cross_catalysis_gamma_heatmap.png
그림 3. archive_03_analysis_outputs/fig3_yemen_autocatalytic_sigmoid.png
그림 4. archive_03_analysis_outputs/fig4_nle_ligand_count_effect.png
그림 5. archive_03_analysis_outputs/fig5_hub_ee_by_half_year.png
