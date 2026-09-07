# 실행 규칙

Agent는 스스로 순서를 정하지 않는다. 이 문서의 순서로만 진행한다.

## 단계

| 단계 | 이름 | 담당 | 산출물 |
| --- | --- | --- | --- |
| 00 | 입력 확인 | 진행자 | 입력 목록 |
| 01 | 자료 분석 | pm-consultant | `context/*.yaml` 초안 |
| 02 | 프로젝트 개요 | pm-consultant | `output/project-overview.md` |
| 03 | 기획 검토 | pm-consultant | `output/planning-review.md` |
| 04 | 서비스 구조 | service-planner | `output/service-structure.md` |
| 05 | 기능 정의 | service-planner | 기능 상세 (04에 포함) |
| 06 | Flow 설계 | flow-designer | `output/flow-chart.md` |
| 07 | 시스템 구조 | system-planner | `output/system-structure.md` |
| 08 | 추적성 검증 | traceability-validator | 검증 결과 |
| 09 | 누락 분석 | traceability-validator | 누락 목록 |
| 10 | 최종 검토 | senior-reviewer | `output/final-review.md` |
| 11 | 수정 | 각 담당 | 수정된 산출물 |
| 12 | 최종 문서 | 진행자 | `docs/` 반영 |

## 단계 이동 조건

앞 단계의 통과 기준을 만족해야 다음 단계로 간다. 만족하지 못하면 그 자리에서 보완한다.

| 단계 | 통과 기준 |
| --- | --- |
| 01 | 입력 자료를 모두 읽었고 `context/project.yaml`에 프로젝트명, 배경, 문제, 목표가 채워졌다 |
| 02 | 목표마다 요구사항이 하나 이상 연결되고 제외 범위가 적혀 있다 |
| 03 | 누락, 중복, 모순 항목이 각각 목록으로 나왔다 |
| 04 | 사용자 유형, 메뉴, 기능, 화면이 정의되고 서로 연결되었다 |
| 05 | 기능마다 13개 항목이 모두 채워졌다 |
| 06 | 네 가지 Flow가 각각 작성되고 기능 목록과 일치한다 |
| 07 | 기능마다 시스템 매핑이 있고 기술 결정 필요 항목이 분리되었다 |
| 08 | 요구사항과 기능 전체에 판정이 있다 |
| 09 | 누락 항목이 `_data/issues.yaml`에 등록되었다 |
| 10 | 검토 질문 18개에 모두 답했다 |
| 11 | CRITICAL과 MAJOR가 0건이다 |

## 되돌아가기

11단계에서 CRITICAL이나 MAJOR가 남으면 그 항목의 담당 단계로 돌아간다.

```text
10 최종 검토
 ↓
CRITICAL 또는 MAJOR 있음?
 ├─ 예 → 해당 단계로 복귀 → 수정 → 08 추적성 검증부터 다시
 └─ 아니오 → 12 최종 문서
```

되돌아간 횟수를 `context/decisions.yaml`에 기록한다. 같은 항목으로 세 번 되돌아가면 그 항목은 의사결정 필요로 올리고 진행을 멈춘다. 같은 문제를 계속 고치는 것은 판단이 없기 때문이다.

## 병렬 실행

다음 조합만 동시에 진행할 수 있다.

| 조합 | 조건 |
| --- | --- |
| 06 Flow 설계 + 07 시스템 구조 | 05 기능 정의가 끝난 뒤 |

그 밖에는 순차로 진행한다. 앞 단계의 결과가 다음 단계의 입력이기 때문이다.

## 매 단계 종료 처리

1. 변경한 문서를 `_data/changes.yaml`에 기록한다. 영향받는 하위 문서를 `affects`에 적는다.
2. 상위 문서가 바뀌었으면 하위 문서 상태를 검토 중으로 되돌린다.
3. 새로 만든 식별자를 `_data/trace.yaml`에 반영한다.
4. `_data/documents.yaml`의 상태, 버전, 갱신일을 수정한다.
5. `python tools/build_dashboard.py`를 실행한다. 연결되지 않은 항목이 나오면 보고한다.

## 진행자의 판단

Agent가 확인 필요로 올린 항목은 진행자가 사용자에게 묻는다. Agent가 임의로 정하지 않는다. 다만 다음은 묻지 않고 진행한다.

- 문서 형식과 표기
- 식별자 부여
- 이미 확정된 기준의 적용
