# -*- coding: utf-8 -*-
"""_data/*.yaml 과 docs/*.md 를 읽어 dashboard/index.html 을 생성한다.

사용법:  python tools/build_dashboard.py

상황판 탭은 두 개다. '문서별 작업'은 진행률과 문서 열람, '변경 이력'은 변경 항목 조회를 담당한다.
문서 본문은 생성 시점에 HTML 안에 함께 넣는다. 상황판 파일 하나만 열면 문서까지 볼 수 있다.
문서 간 연결 누락과 미결 항목은 화면에 넣지 않고, 실행할 때 콘솔에 점검 결과로 출력한다.
점검 규칙은 README.md '누락 점검 규칙' 표와 같다.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
TEMPLATE = ROOT / "tools" / "dashboard_template.html"
OUT = ROOT / "dashboard" / "index.html"

DONE_STATUS = "확정"
ACTIVE_STATUS = ("작성 중", "검토 중")


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def s(v):
    """날짜 등 비문자열 값을 문자열로 통일한다."""
    if v is None:
        return ""
    if hasattr(v, "isoformat"):
        return v.isoformat()
    return str(v)


def check_links(trace, doc_titles):
    """문서 간 연결 누락과 정의 간 불일치를 점검한다. 화면에는 넣지 않고 콘솔로만 보고한다."""
    reqs = trace.get("requirements", []) or []
    decisions = trace.get("decisions", []) or []
    users = trace.get("users", []) or []
    fns = trace.get("functions", []) or []
    flows = trace.get("flows", []) or []
    screens = trace.get("screens", []) or []
    specs = trace.get("specs", []) or []

    known = {}
    for group in (reqs, decisions, users, fns, flows, screens, specs):
        for item in group:
            known[item["id"]] = item.get("title", "")

    found = []

    def add(kind, item_id, message, doc):
        found.append({"kind": kind, "id": item_id, "title": known.get(item_id, ""),
                      "message": message, "document": doc_titles.get(doc, doc)})

    def check_refs(item, field, owner_doc):
        for ref in item.get(field, []) or []:
            if ref not in known:
                add("정의 간 불일치", item["id"],
                    f"{ref} 는 trace.yaml 에 정의되지 않은 ID다", owner_doc)

    for d in decisions:
        check_refs(d, "requirements", "DOC-02")
    for f in fns:
        check_refs(f, "requirements", "DOC-03")
        check_refs(f, "users", "DOC-03")
    for fl in flows:
        check_refs(fl, "functions", "DOC-04")
        check_refs(fl, "screens", "DOC-04")
        check_refs(fl, "users", "DOC-04")
    for sc in screens:
        check_refs(sc, "functions", "DOC-05")
        check_refs(sc, "users", "DOC-05")
    for fs in specs:
        check_refs(fs, "functions", "DOC-07")
        check_refs(fs, "screens", "DOC-07")
        check_refs(fs, "decisions", "DOC-07")
        if fs.get("screen") and fs["screen"] not in known:
            add("정의 간 불일치", fs["id"],
                f"{fs['screen']} 는 trace.yaml 에 정의되지 않은 ID다", "DOC-07")

    fn_by_req, fl_by_fn, sc_by_fn, fs_by_fn, fl_by_sc = {}, {}, {}, {}, {}
    for f in fns:
        for r in f.get("requirements", []) or []:
            fn_by_req.setdefault(r, []).append(f["id"])
    for fl in flows:
        for f in fl.get("functions", []) or []:
            fl_by_fn.setdefault(f, []).append(fl["id"])
        for sc in fl.get("screens", []) or []:
            fl_by_sc.setdefault(sc, []).append(fl["id"])
    for sc in screens:
        for f in sc.get("functions", []) or []:
            sc_by_fn.setdefault(f, []).append(sc["id"])
    fs_by_sc = {}
    for fs in specs:
        for f in fs.get("functions", []) or []:
            fs_by_fn.setdefault(f, []).append(fs["id"])
        if fs.get("screen"):
            fs_by_sc.setdefault(fs["screen"], []).append(fs["id"])
    # 명세는 화면 단위로 쓴다. 기능은 그 기능의 화면에 명세가 있으면 갖춘 것으로 본다
    for sc in screens:
        for fid in fs_by_sc.get(sc["id"], []):
            for f in sc.get("functions", []) or []:
                fs_by_fn.setdefault(f, []).append(fid)

    for r in reqs:
        if not fn_by_req.get(r["id"]):
            add("연결되지 않은 항목", r["id"], "요구사항이 어떤 기능(FN)에도 연결되지 않음", "DOC-03")
    for f in fns:
        if not fl_by_fn.get(f["id"]):
            add("연결되지 않은 항목", f["id"], "기능이 어떤 Flow(FL)에도 포함되지 않음", "DOC-04")
        if not sc_by_fn.get(f["id"]):
            add("연결되지 않은 항목", f["id"], "기능에 연결된 화면(SC)이 없음", "DOC-05")
        if not fs_by_fn.get(f["id"]):
            add("연결되지 않은 항목", f["id"], "기능 명세(FS)가 없음", "DOC-07")
    for sc in screens:
        if not fl_by_sc.get(sc["id"]):
            add("연결되지 않은 항목", sc["id"], "화면이 어떤 Flow(FL)에도 나타나지 않음", "DOC-04")
        if not fs_by_sc.get(sc["id"]):
            add("연결되지 않은 항목", sc["id"], "화면에 기능 명세(FS)가 없음", "DOC-07")
        if sc.get("wireframe", "미착수") == "미착수":
            add("연결되지 않은 항목", sc["id"], "Wireframe 미착수", "DOC-06")
    return found


def build():
    documents = load("documents.yaml")
    trace = load("trace.yaml")
    changes = load("changes.yaml").get("changes", []) or []
    issues = load("issues.yaml").get("issues", []) or []

    docs = documents.get("documents", []) or []
    project = {k: s(v) for k, v in (documents.get("project", {}) or {}).items()}
    doc_titles = {d["id"]: d["title"] for d in docs}
    doc_titles.setdefault("DOC-00", "구조·기준")

    rows, etas, missing = [], [], []
    for n, d in enumerate(docs, start=1):
        status = d.get("status", "미착수")
        progress = 100 if status == DONE_STATUS else int(d.get("progress") or 0)
        eta = s(d.get("eta"))
        if status != DONE_STATUS and eta:
            etas.append(eta)

        rel = d.get("file", "")
        path = ROOT / rel
        if path.is_file():
            content = path.read_text(encoding="utf-8")
        else:
            content, _ = "", missing.append(rel)

        rows.append({
            "no": n, "id": d["id"], "title": d["title"], "file": rel,
            "category": d.get("category", ""), "status": status,
            "progress": progress, "eta": eta,
            "version": s(d.get("version")), "updated": s(d.get("updated")),
            "inherits_titles": [doc_titles.get(x, x) for x in d.get("inherits", []) or []],
            "content": content,
        })

    total = len(rows) or 1
    summary = {
        "progress": round(sum(r["progress"] for r in rows) / total),
        "total": len(rows),
        "done": sum(1 for r in rows if r["status"] == DONE_STATUS),
        "active": sum(1 for r in rows if r["status"] in ACTIVE_STATUS),
        "waiting": sum(1 for r in rows if r["status"] == "미착수"),
        "eta": max(etas) if etas else "",
    }

    for c in changes:
        c["date"] = s(c.get("date"))
        c["document_title"] = doc_titles.get(c.get("document"), c.get("document"))
        c["affects_titles"] = [doc_titles.get(x, x) for x in c.get("affects", []) or []]

    data = {
        "built": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "project": project,
        "summary": summary,
        "documents": rows,
        "changes": sorted(changes, key=lambda c: (c.get("date", ""), c.get("id", "")), reverse=True),
    }

    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    orphans = check_links(trace, doc_titles)
    open_issues = [i for i in issues if i.get("status", "미결") != "해결"]
    size_kb = round(len(html.encode("utf-8")) / 1024)
    print(f"생성: {OUT.relative_to(ROOT)} ({size_kb}KB, 문서 본문 포함)")
    print(f"전체 진행률 {summary['progress']}% · 진행 중 {summary['active']}건 · "
          f"대기 {summary['waiting']}건 · 완료 {summary['done']}건")
    for m in missing:
        print(f"  ! 문서 파일 없음: {m}")
    print(f"점검: 미결 항목 {len(open_issues)}건, 연결되지 않은 항목 {len(orphans)}건")
    for i in open_issues:
        print(f"  - [{i.get('type')}] {i['id']} {i.get('title','')} -> "
              f"{doc_titles.get(i.get('document'), i.get('document'))}")
    by_doc = {}
    for o in orphans:
        by_doc.setdefault((o["kind"], o["message"], o["document"]), []).append(o["id"])
    started = {d["id"] for d in docs if d.get("status") != "미착수"}
    doc_of = {v: k for k, v in doc_titles.items()}
    for (kind, message, doc), items in sorted(by_doc.items()):
        pending = doc_of.get(doc) not in started
        mark = "  (해당 문서 미착수)" if pending else ""
        head = f"  - [{kind}] {message} -> {doc} {len(items)}건{mark}"
        print(head)
        if not pending:
            print(f"      {', '.join(items)}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
