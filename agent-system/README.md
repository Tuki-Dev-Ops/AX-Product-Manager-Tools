# 기획 문서 Agent System

기존 기획 자료를 읽고 프로젝트 개요, 기획 검토, 서비스 구조, 기능 정의, Flow, 시스템 구조를 보강한다.

문서를 새로 창작하지 않는다. 기존 내용에 누락된 것을 더하고 구조를 잡고 논리를 맞춘다.

## 구성

```text
agent-system/
├─ agents/     역할 정의. .claude/agents/ 에 복사해 쓴다
├─ harness/    실행 순서와 검사 기준
├─ skills/     각 역할의 작업 절차
├─ context/    Agent 간에 주고받는 중간 상태
└─ output/     산출물 서식
```

## 사용

### 1. Agent 등록

```bash
mkdir -p .claude/agents
cp agent-system/agents/*.md .claude/agents/
```

각 파일 머리말의 `name`으로 호출된다.

### 2. Skill 등록

```bash
mkdir -p .claude/skills
cp -r agent-system/skills/* .claude/skills/
```

### 3. 실행

`agent-system/harness/workflow.md`의 순서대로 진행한다. 00 입력 확인부터 12 최종 문서까지다.

각 단계가 끝나면 `agent-system/harness/validation.md`의 여덟 가지 검사를 수행한다. 통과하지 못하면 다음 단계로 가지 않는다.

## 기존 프로젝트와의 관계

이 프로젝트에는 이미 문서 체계가 있다. Agent System은 그것을 대체하지 않는다.

| 구분 | 역할 |
| --- | --- |
| `docs/` | 확정된 사용자 대상 문서 |
| `_data/` | 확정된 추적 데이터. 상황판의 근거 |
| `agent-system/context/` | 작업 중 중간 상태 |
| `agent-system/output/` | 작업 중 산출물 |

Context의 항목이 확정되면 `_data/`와 `docs/`로 옮긴다. 옮긴 뒤에는 그쪽이 원본이다.

문서 작성 기준은 `CLAUDE.md`를 따른다. Agent System이 별도 기준을 두지 않는다.

## 원칙

1. 문서를 새로 창작하지 않는다. 기존 자료를 먼저 읽는다.
2. 자료에 없는 내용을 확정하지 않는다. 가정과 확인 필요로 구분한다.
3. 기술 스택을 근거 없이 정하지 않는다.
4. 요구사항에 없는 기능을 추가하지 않는다.
5. 기존 내용과 충돌하면 임의로 고치지 않고 검토 필요로 올린다.
6. 식별자는 한 번 부여하면 바꾸지 않는다.
7. 개발자가 만들 수 있고 QA가 검증할 수 있는 수준으로 쓴다.

## 산출

| 영역 | 위치 |
| --- | --- |
| 최종 문서 | `docs/` |
| 검토 결과 | `agent-system/output/final-review.md` |
| 미결 항목 | `_data/issues.yaml` |
