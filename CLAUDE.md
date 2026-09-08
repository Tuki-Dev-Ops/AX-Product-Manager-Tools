# 문서 작성 기준

이 파일은 이 폴더에서 작성하는 모든 사용자 대상 기획 문서(기획서, IA, Flow Chart, Wireframe, 기능 명세, 검토 결과)에 적용되는 작성 기준이다. 아래 기준을 그대로 따른다.

---

# DOCUMENT WRITING STANDARD

# IT Consulting / Senior Product Planning Style

This document defines the writing standards for all user-facing planning documents.

The objective is to produce documentation that reads as if it was prepared by an experienced IT consultant, senior product planner, or professional PM.

The document must not feel AI-generated.

---

# 1. WRITING PRINCIPLE

Write as a professional consultant would write for an actual client or internal project team.

The writing must be:

* Clear
* Concise
* Practical
* Specific
* Neutral
* Professional
* Decision-oriented

Avoid unnecessary explanation.

Avoid exaggerated language.

Avoid generic AI expressions.

Do not try to sound sophisticated.

Do not use unnecessarily technical terminology when a simpler professional term is clearer.

The goal is not to demonstrate intelligence.

The goal is to communicate the planning decision clearly.

---

# 2. HUMAN DOCUMENT VS INTERNAL DOCUMENT

Maintain two different writing layers.

## INTERNAL LAYER

Used between AI agents.

Optimize for:

* Parsing
* Traceability
* Validation
* Structured data
* Stable identifiers
* Machine-readable terminology

English identifiers and YAML/JSON are allowed.

Example:

```yaml
requirement_id: REQ-ORDER-003
actor: CUSTOMER
trigger: CANCEL_REQUEST
precondition: ORDER_STATUS=PAID
```

## USER-FACING LAYER

Used in:

* Planning documents
* Reports
* Presentations
* Client deliverables
* Specifications
* Wireframes
* IA
* Flow Charts

Write naturally in Korean unless another language is requested.

Do not expose internal IDs unless they are useful for traceability.

Do not expose internal agent terminology.

Do not expose internal reasoning.

---

# 3. WRITING STYLE

Use the style of an experienced IT consulting firm.

Preferred:

> 주문 상태가 '배송 준비' 이후인 경우에는 고객이 직접 주문을 취소할 수 없도록 제한한다.

Avoid:

> 사용자가 주문 취소를 요청하는 경우 시스템은 주문 상태를 확인하고 해당 상태에 따라 취소 가능 여부를 판단합니다.

The first sentence communicates the business rule directly.

---

# 4. SENTENCE STYLE

Prefer short declarative sentences.

Use:

* ~한다.
* ~할 수 있다.
* ~하도록 한다.
* ~으로 정의한다.
* ~을 적용한다.
* ~을 제공한다.
* ~을 제한한다.
* ~을 표시한다.
* ~을 관리한다.

Avoid excessive use of:

* ~해야 합니다.
* ~할 수 있도록 합니다.
* ~하는 것이 필요합니다.
* ~할 필요가 있습니다.
* ~하는 것을 권장합니다.

Use direct statements instead.

---

# 5. DO NOT USE AI-LIKE EXPRESSIONS

Avoid the following expressions unless they are genuinely necessary:

* 본질적으로
* 종합적으로
* 효과적으로
* 체계적으로
* 유기적으로
* seamless
* holistic
* robust
* scalable solution
* innovative
* cutting-edge
* 최적의
* 효율적인
* 사용자 중심의
* 직관적인
* 혁신적인
* 차별화된
* 고도화된
* 종합적인
* 다양한
* 풍부한
* 향상된
* 획기적인

These expressions are often vague.

Replace them with specific statements.

Bad:

> 사용자 중심의 직관적인 서비스를 제공한다.

Good:

> 주요 기능은 첫 화면에서 바로 접근할 수 있도록 구성한다.

Bad:

> 확장 가능한 아키텍처를 구성한다.

Good:

> 초기에는 단일 서비스 구조로 구성하고, 트래픽 증가 시 기능별 분리가 가능하도록 모듈 단위로 설계한다.

---

# 6. AVOID REDUNDANCY

Do not repeat the same information in:

* Summary
* Flow
* IA
* Wireframe
* Functional Specification

Each section has a specific purpose.

### Flow Chart

Answers:

"사용자가 어떤 순서로 서비스를 이용하는가?"

### IA

Answers:

"서비스의 화면과 기능은 어떻게 구성되는가?"

### Wireframe

Answers:

"각 화면은 어떻게 배치되고 동작하는가?"

### Functional Specification

Answers:

"각 기능은 어떤 조건과 규칙으로 동작하는가?"

### Architecture

Answers:

"서비스는 어떤 시스템으로 구성되고 서로 어떻게 연동되는가?"

---

# 7. REQUIREMENT WRITING

Requirements must describe an actual product behavior or business rule.

Bad:

> 회원 관리 기능을 제공하여 사용자 편의성을 향상한다.

Good:

> 관리자는 회원 목록에서 상태, 가입일, 검색어를 기준으로 회원을 조회할 수 있다.

Bad:

> 결제 시스템을 안정적으로 구축한다.

Good:

> 결제 요청 결과에 따라 주문 상태를 결제 완료, 결제 실패로 구분하여 관리한다.

---

# 8. FEATURE NAME

Use concise nouns or action-oriented names.

Preferred:

* 회원 목록
* 회원 상세
* 주문 조회
* 주문 취소
* 결제 수단 관리
* 알림 설정
* 파일 업로드
* 관리자 권한 관리

Avoid:

* 회원 관리 기능 제공
* 주문 정보를 효율적으로 조회할 수 있는 기능
* 사용자 편의성을 위한 알림 기능

---

# 9. PAGE NAME

Page names must be simple and recognizable.

Preferred:

* 대시보드
* 회원 목록
* 회원 상세
* 주문 목록
* 주문 상세
* 결제 내역
* 설정

Avoid:

* 회원 정보 관리 화면
* 주문 관련 정보 조회 화면
* 사용자 설정 및 관리 화면

---

# 10. FLOW CHART WRITING

Flow Chart should describe behavior, not explain the flow in paragraphs.

Preferred:

```text
로그인
 ↓
아이디/비밀번호 입력
 ↓
로그인 요청
 ↓
인증 결과 확인
 ├─ 성공 → 대시보드
 └─ 실패 → 오류 메시지 표시
```

Avoid:

> 사용자가 아이디와 비밀번호를 입력한 후 로그인 버튼을 클릭하면 시스템에서 인증을 수행하고 인증 결과에 따라 다음 화면으로 이동합니다.

---

# 11. IA WRITING

IA should be concise.

Example:

```text
1. 대시보드

2. 회원 관리
   2.1 회원 목록
   2.2 회원 상세

3. 주문 관리
   3.1 주문 목록
   3.2 주문 상세

4. 설정
   4.1 계정 설정
   4.2 알림 설정
```

Do not add unnecessary descriptions to every hierarchy item.

---

# 12. WIREFRAME WRITING

Describe the purpose and behavior of the screen.

Preferred:

### 회원 목록

**목적**
회원 정보를 조회하고 관리한다.

**구성**

* 검색 영역
* 상태 필터
* 회원 목록
* 페이지네이션

**주요 동작**

* 검색 조건 입력 후 조회
* 회원 선택 시 상세 화면 이동
* 상태 변경 시 확인 팝업 표시

**예외**

* 검색 결과가 없는 경우 "검색 결과가 없습니다." 표시
* 조회 실패 시 오류 메시지 표시

Avoid:

> 사용자가 편리하게 회원 정보를 확인할 수 있도록 직관적인 UI를 제공한다.

---

# 13. FUNCTIONAL SPECIFICATION WRITING

Functional specifications must define actual behavior.

Use this structure:

### 기능명

**목적**
무엇을 처리하는 기능인지 정의한다.

**대상**
누가 사용하는지 정의한다.

**사전 조건**
기능 실행 전에 충족되어야 하는 조건.

**처리**

1. 사용자가 검색 조건을 입력한다.
2. 조회 버튼을 선택한다.
3. 시스템은 입력 조건에 따라 회원 정보를 조회한다.
4. 조회 결과를 목록에 표시한다.

**조건**

* 관리자 권한이 있는 경우에만 조회할 수 있다.
* 검색어는 최대 100자까지 입력할 수 있다.

**예외**

* 조회 결과가 없는 경우 빈 결과 화면을 표시한다.
* 서버 오류 발생 시 오류 메시지를 표시한다.

---

# 14. BUSINESS RULE WRITING

Business rules must be explicit.

Bad:

> 주문 취소는 적절한 경우에만 가능하다.

Good:

> 주문 상태가 '결제 완료'인 경우에만 고객이 직접 주문을 취소할 수 있다.

Bad:

> 관리자는 필요한 권한을 가져야 한다.

Good:

> 회원 정보 수정은 '회원 관리' 권한을 가진 관리자만 수행할 수 있다.

---

# 15. ERROR MESSAGE WRITING

Error messages must describe what happened and what the user can do.

Bad:

> 오류가 발생했습니다.

Better:

> 요청을 처리하지 못했습니다. 잠시 후 다시 시도해 주세요.

Specific error:

> 비밀번호가 일치하지 않습니다.

System error:

> 서버와 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.

Avoid technical error codes in user-facing messages unless required.

---

# 16. STATUS NAME

Use consistent business terminology.

Example:

```text
대기
처리 중
완료
실패
취소
삭제
```

Do not alternate between:

```text
완료
성공
처리완료
Complete
DONE
```

unless these represent genuinely different states.

---

# 17. TERMINOLOGY CONSISTENCY

Once a business term is defined, use the same term throughout the entire document.

For example, choose one:

* 회원
* 사용자
* 고객

Do not randomly alternate between all three.

If they represent different entities, explicitly define the difference.

Example:

```text
회원 = 서비스에 가입한 사용자
고객 = 실제 상품을 구매한 회원
관리자 = 운영 권한을 가진 사용자
```

---

# 18. TABLE WRITING

Use tables when information is easier to compare.

Example:

| 구분    | 설명          |
| ----- | ----------- |
| 대상    | 관리자         |
| 목적    | 회원 조회 및 관리  |
| 검색 조건 | 이름, 이메일, 상태 |
| 결과    | 회원 목록       |
| 권한    | 회원 관리 권한 필요 |

Avoid creating tables simply to make the document look structured.

---

# 19. RECOMMENDATION WRITING

Recommendations should include the decision and reason.

Bad:

> 사용성을 고려하여 검색 기능을 개선하는 것을 권장합니다.

Good:

> 검색 조건은 이름, 이메일, 상태로 제한한다. 초기 버전에서는 복잡한 필터를 제공하지 않고 주요 조회 조건만 제공하는 것이 적절하다.

---

# 20. RESEARCH RESULT WRITING

Research findings should be converted into planning implications.

Do not dump research results into the planning document.

Bad:

> A 서비스는 검색 기능을 제공하고 있으며 B 서비스도 필터 기능을 제공하고 있다.

Good:

> 유사 서비스는 기본 검색과 조건별 필터를 함께 제공한다. 본 서비스도 초기 버전에서 검색어와 주요 상태값을 기준으로 조회할 수 있도록 구성한다.

The purpose of research is to support a product decision.

---

# 21. COMPETITOR ANALYSIS

Do not simply list competitors.

Analyze:

* What they do
* Why they do it
* What works
* What does not
* What should be adopted
* What should not be adopted

Example:

| 항목 | A 서비스 | B 서비스 | 제안                |
| -- | ----- | ----- | ----------------- |
| 검색 | 기본 검색 | 상세 필터 | 초기에는 기본 검색 적용     |
| 목록 | 테이블   | 카드    | 데이터 중심 화면은 테이블 적용 |
| 상세 | 별도 화면 | 모달    | 정보량에 따라 별도 화면 적용  |

---

# 22. PRODUCT FEEDBACK

Do not label the section as an AI-style "Feedback".

Use professional terms such as:

* 검토 의견
* 주요 검토 사항
* 개선 제안
* 기획 검토 결과
* 주요 이슈
* 의사결정 사항

Preferred:

## 주요 검토 사항

| 항목   | 검토 결과          | 제안                  |
| ---- | -------------- | ------------------- |
| 회원가입 | 입력 항목이 많음      | 초기 가입 단계는 최소 정보로 구성 |
| 검색   | 조건이 지나치게 많음    | 핵심 조건 중심으로 단순화      |
| 관리자  | 운영 기능이 정의되지 않음 | 관리자 메뉴 별도 구성        |

---

# 23. UNKNOWN / ASSUMPTION / DECISION

Do not expose these terms directly to users unless necessary.

Use:

UNKNOWN → 확인 필요

ASSUMPTION → 가정

DECISION_REQUIRED → 의사결정 필요

ORPHAN → 연결되지 않은 항목

CONFLICT → 정의 간 불일치

Example:

Bad:

> DECISION_REQUIRED: Authentication

Good:

> **의사결정 필요**
>
> 로그인 방식이 정의되지 않았다.
>
> * 이메일/비밀번호
> * 소셜 로그인
> * SSO
>
> B2B 서비스라면 SSO를 고려할 수 있으며, 일반 사용자 서비스라면 이메일/비밀번호를 기본 방식으로 적용하는 것이 적절하다.

---

# 24. CRITIC RESULT

Do not expose "Critic Agent" terminology.

Use:

## 기획 검토 결과

### 주요 수정 사항

1. 주문 취소 화면은 IA에 정의되어 있으나 사용자 Flow에 포함되지 않았다.
2. 관리자 권한에 대한 기준이 화면별로 다르게 정의되어 있다.
3. 결제 실패 시 처리 기준이 기능 명세에 누락되어 있다.

### 조치

* 주문 취소 Flow 추가
* 관리자 권한 기준 통일
* 결제 실패 상태 및 재시도 정책 정의

---

# 25. FINAL DOCUMENT TONE

The final document should feel like:

"실무 경험이 많은 IT 컨설턴트가 프로젝트 착수 전에 정리한 기획 문서"

It should NOT feel like:

"AI가 요구사항을 분석해서 생성한 보고서"

Therefore:

* Avoid excessive headings.
* Avoid unnecessary English.
* Avoid repetitive summaries.
* Avoid generic explanations.
* Avoid exaggerated conclusions.
* Avoid artificial certainty.
* Avoid filler sentences.
* Avoid phrases that merely restate the heading.

---

# 26. DOCUMENT STRUCTURE

Use the following final structure unless the project requires otherwise.

# 1. 프로젝트 개요

* 추진 배경
* 목적
* 대상 사용자
* 주요 범위

# 2. 기획 검토

* 시장 및 유사 서비스 조사
* 주요 시사점
* 기획 검토 사항
* 개선 제안
* 의사결정 필요 사항

# 3. 서비스 구조

* 서비스 구성
* 사용자 유형
* 주요 기능
* 서비스 아키텍처
* 시스템 연계 구조

# 4. Flow Chart

* 주요 사용자 Flow
* 예외 Flow

# 5. IA

* 메뉴 구조
* 화면 목록
* 화면별 역할 및 접근 권한

# 6. Wireframe

* 화면 구성
* 주요 컴포넌트
* 인터랙션
* 상태별 화면

# 7. 기능 명세

* 기능별 동작
* 입력/출력
* 조건
* 권한
* 예외 처리
* 연계 API

# 8. 검토 결과

* 주요 이슈
* 수정 사항
* 추가 확인 사항

---

# 27. FINAL QUALITY CHECK

Before presenting the final document, ask:

1. Would an experienced IT consultant actually write this sentence?
2. Is the sentence saying something useful?
3. Can the sentence be shorter?
4. Is the terminology consistent?
5. Is the requirement specific enough for a developer?
6. Is the behavior specific enough for QA?
7. Is the structure clear enough for a designer?
8. Is the business rule clear enough for a PM?
9. Is the architecture consistent with the Flow?
10. Is the Wireframe consistent with the IA?
11. Is the Functional Specification consistent with the Wireframe?
12. Does anything sound like generic AI-generated text?

If a sentence does not provide meaningful information, remove it.

If a sentence can be expressed more clearly, rewrite it.

The final document must prioritize clarity over completeness, and practical decisions over verbose explanation.

---

# 운영 규칙 (이 폴더 전용)

폴더 구조, 문서 상속 관계, 식별자 체계는 `README.md`에 정의되어 있다. 아래 규칙을 함께 적용한다.

## 문서 작성

* 사용자 대상 문서는 `docs/` 아래 8개 파일에만 작성한다. 새 문서를 임의로 추가하지 않는다.
* 각 문서 상단의 문서 정보 표(문서 ID, 상태, 버전, 상위·하위 문서, 정의·참조 항목)를 유지한다.
* 하위 문서는 상위 문서에서 정의한 항목(REQ, DC, UT, FN, FL, SC)을 참조만 한다. 새 항목이 필요하면 해당 항목을 정의하는 상위 문서에 먼저 추가한다.
* 문서 본문에 `[확인 필요]`, `[가정]`, `[의사결정 필요]`를 표기한 항목은 `_data/issues.yaml`에도 등록한다.

## 변경 처리

* 문서를 수정하면 같은 작업 안에서 `_data/changes.yaml`에 변경 항목을 추가한다. 영향받는 하위 문서를 `affects`에 적는다.
* 상위 문서가 바뀌면 영향받는 하위 문서의 상태를 `검토 중`으로 되돌린다.
* 새로 정의하거나 바뀐 식별자는 `_data/trace.yaml`에 반영한다.
* `_data/documents.yaml`의 상태, 버전, 갱신일을 함께 수정한다.
* 작업 마지막에 `python tools/build_dashboard.py`를 실행해 `dashboard/index.html`을 다시 생성한다. 생성 결과에 '연결되지 않은 항목'이 있으면 사용자에게 보고한다.

## 변경 후 점검 (모든 작업에 적용)

무엇을 바꾸든 그 작업 안에서 아래를 끝낸다. 다음 요청을 기다리지 않는다.

1. **하위 문서 최신화**  바꾼 항목을 참조하는 하위 문서를 모두 찾아 함께 고친다. 화면을 지우면 04 Flow, 05 IA, 07 기능 명세, `_data/trace.yaml`에서 그 화면을 가리키는 곳을 남기지 않는다.
2. **상위 문서 확인**  기능이나 화면이 늘거나 줄면 01 요구사항과 03 기능 목록이 여전히 맞는지 확인한다. 근거가 사라진 요구사항은 같이 정리한다.
3. **누락 점검**  같은 유형의 화면에 있어야 할 상태가 빠졌는지 본다. 목록은 결과 없음, 등록·수정은 검증 오류, 처리 동작은 확인 팝업과 결과 안내를 갖춘다.
4. **표기 일치**  같은 항목이 문서마다 다른 이름이나 다른 규칙으로 적혀 있지 않은지 본다. 화면 수, 건수, 상태명, 용어를 맞춘다.
5. **식별자 점검**  중복과 재사용이 없는지 본다. 삭제한 번호는 다시 쓰지 않는다.
6. **08 검토 결과 갱신**  수치를 다시 세고, 조치가 끝난 항목은 지우고, 새로 생긴 검토 사항을 올린다.
7. **판단이 필요한 것은 보고**  범위가 바뀌거나 정책을 새로 정해야 하거나 근거가 없는 항목은 임의로 정하지 않는다. 선택지와 판단 근거를 함께 보고한다. 그 자리에서 정할 수 없으면 `_data/issues.yaml`에 등록하고 문서에 `[확인 필요]`로 표기한다.

점검 결과는 작업 보고에 함께 적는다. 고친 것과 보고할 것을 나눠서 적는다.

## 상황판

* `dashboard/index.html`은 생성물이다. 직접 수정하지 않는다. 화면을 바꿀 때는 `tools/dashboard_template.html`을 수정한다.
* 상황판에 표시되는 문구는 사용자 대상 문서와 같은 기준(한글, 업무 용어, 상태명 통일)을 따른다.

## 아키텍처 설계

* 시스템 구성과 인프라는 인터넷 조사를 먼저 하고, 근거를 확인한 뒤 설계한다. 조사 없이 통상적인 구성을 그대로 적지 않는다.
* 구성 요소를 선택할 때는 선택지와 실제 채택 사례, 선택 조건, 근거를 함께 남긴다. 결론만 적지 않는다.
* 솔루션 간 연결 방식(결제, 단말, 외부 시스템 연동)은 각 솔루션의 공식 문서를 근거로 정리한다.
* 근거로 확정하지 못한 항목은 '확인 필요'로 표기하고 `_data/issues.yaml`에 등록한다.
* 조사 결과는 그대로 옮기지 않는다. 본 서비스에 적용할 판단으로 바꿔서 문서에 적는다.

## 문서 표준

문서 형식과 표기는 아래 표준을 따른다. 조사 근거는 `research/문서표준_조사.md`에 있다.

| 영역 | 준거 | 적용 |
| --- | --- | --- |
| 순서도 기호 | ISO 5807 | 단자, 처리, 판단, 데이터, 정의된 처리, 결합자, 주석 기호만 쓴다 |
| 흐름 방향 | ISO 5807 10.2.1 | 위에서 아래, 왼쪽에서 오른쪽을 표준 방향으로 한다. 표준 방향이 아니면 화살촉을 붙인다 |
| 분기 표기 | ISO 5807 10.3.1.2 | 판단의 각 출구에 조건 값을 적는다 |
| 요구사항 문장 | ISO/IEC/IEEE 29148 5.2.4 | 의무는 평서형으로 적고 권장과 구분한다. 부정문과 수동태를 피한다 |
| 요구사항 금지 표현 | ISO/IEC/IEEE 29148 5.2.7 | 최상급, 주관적 표현, 모호한 대명사, 개방형 표현, 빠져나갈 구멍, 전체성 함의를 쓰지 않는다 |
| 식별자 | ISO/IEC/IEEE 29148 5.2.8.2 | 한 번 부여한 식별자는 바꾸지 않는다. 항목이 삭제되어도 재사용하지 않는다 |
| 추적성 | ISO/IEC/IEEE 29148 6.4.3.5 | 요구사항은 상위 요구사항, 아키텍처, 구현 요소, 검증 항목으로 추적할 수 있어야 한다 |
| 문서 공통 항목 | ISO/IEC/IEEE 15289 7 | 발행일과 상태, 범위, 대상 독자, 참조 문서, 용어 정의, 변경 이력을 갖춘다 |
| 아키텍처 기술 | ISO/IEC/IEEE 42010 | 관점과 뷰를 구분하고, 결정에는 근거와 검토한 대안을 함께 남긴다 |

문서 공통 항목은 다음 위치에서 충족한다. 발행일과 상태는 상황판 문서 머리말, 변경 이력은 `_data/changes.yaml`, 용어 정의는 각 문서의 정의 절, 참조 문서는 `research/` 아래 조사 원본이다.
