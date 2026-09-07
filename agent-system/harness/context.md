# 공유 Context

모든 Agent가 같은 파일을 읽고 쓴다. Agent마다 다른 사실을 들고 있으면 문서가 갈라진다.

## 파일

| 파일 | 내용 | 주 작성자 |
| --- | --- | --- |
| `context/project.yaml` | 프로젝트 배경, 문제, 목표, 범위 | pm-consultant |
| `context/service.yaml` | 사용자, 메뉴, 기능, 권한, 상태 | service-planner |
| `context/system.yaml` | 시스템 구성, API, 데이터, 외부 연계 | system-planner |
| `context/flow.yaml` | 네 가지 Flow 목록과 연결 | flow-designer |
| `context/decisions.yaml` | 결정과 근거, 미결 항목 | 전원 |

## 기존 데이터와의 관계

이 프로젝트에는 이미 `_data/` 아래 추적 데이터가 있다. Context는 그것을 대체하지 않는다.

| 구분 | 역할 |
| --- | --- |
| `context/*.yaml` | 작업 중 Agent 간에 주고받는 중간 상태 |
| `_data/*.yaml` | 확정된 사실. 상황판과 문서의 근거 |

Context의 항목이 확정되면 `_data/`로 옮긴다. 옮긴 뒤에는 `_data/`가 원본이다.

| Context 항목 | 확정 후 위치 |
| --- | --- |
| 요구사항 | `_data/trace.yaml` requirements |
| 사용자 유형 | `_data/trace.yaml` users |
| 기능 | `_data/trace.yaml` functions |
| 화면 | `_data/trace.yaml` screens |
| Flow | `_data/trace.yaml` flows |
| 의사결정 | `_data/trace.yaml` decisions |
| 미결 항목 | `_data/issues.yaml` |
| 변경 | `_data/changes.yaml` |

## 식별자

한 번 부여한 식별자는 바꾸지 않는다. 항목이 삭제되어도 재사용하지 않는다.

| 접두 | 대상 | 정의 문서 |
| --- | --- | --- |
| REQ | 요구사항 | 01 프로젝트 개요 |
| DC | 의사결정 | 02 기획 검토 |
| UT | 사용자 유형 | 03 서비스 구조 |
| FN | 기능 | 03 서비스 구조 |
| FL | Flow | 04 Flow Chart |
| SC | 화면 | 05 IA |
| FS | 기능 명세 | 07 기능 명세 |
| IS | 미결 항목 | `_data/issues.yaml` |
| CH | 변경 | `_data/changes.yaml` |

하위 문서는 상위 문서에서 정의한 항목을 참조만 한다. 새 항목이 필요하면 그 항목을 정의하는 상위 문서에 먼저 추가한다.

## 값의 상태

Context의 모든 값은 세 상태 중 하나를 가진다.

| 상태 | 뜻 | 문서 표기 |
| --- | --- | --- |
| confirmed | 입력 자료에서 확인됨 | 그대로 서술 |
| assumed | 문맥상 판단, 근거 문장 없음 | 가정 |
| open | 의사결정 필요 | 확인 필요 |

`assumed`와 `open`은 문서에 표기하고 `_data/issues.yaml`에 등록한다. 등록되지 않은 값은 문서에 쓰지 않는다.

## 충돌 처리

기존 내용과 새 판단이 충돌하면 임의로 고치지 않는다. 아래 형식으로 남기고 의사결정으로 올린다.

```text
[기존 내용]
주문 취소는 조리 시작 전까지 가능하다.

[충돌 내용]
가맹 어드민 화면 정의에는 조리 완료 후에도 취소 버튼이 있다.

[검토 필요]
조리 완료 후 취소를 허용할지 결정한다. 허용하면 환불 처리 기준이 필요하다.
```

## 갱신 규칙

- 값을 바꾼 Agent는 그 자리에서 `context/decisions.yaml`에 이유를 적는다.
- 다른 Agent가 쓴 값을 지우지 않는다. 다르면 충돌로 올린다.
- 단계가 끝나면 Context와 `_data/`의 차이를 확인한다.
