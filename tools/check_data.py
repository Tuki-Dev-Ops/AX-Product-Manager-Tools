# -*- coding: utf-8 -*-
"""데이터 규칙 점검. python tools/check_data.py 로 실행한다.

_data 아래 파일이 규칙대로 쓰였는지, 문서와 어긋나지 않는지 본다.

  1 문서 목록의 파일, 상태, 진행률, 판번호, 갱신일
  2 변경 이력의 필수 항목과 영향 문서
  3 이슈의 필수 항목과 상태
  4 문서 본문의 확인 필요·가정·의사결정 필요 표기가 이슈에 등록되어 있는지
  5 상속 관계가 서로 맞는지
"""
import re, sys, pathlib, datetime, collections, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC_STATUS = ("작성 전", "작성 중", "검토 중", "확정")
CH_TYPE = ("추가", "수정", "삭제", "범위 변경", "확정")
CH_STATUS = ("대기", "진행 중", "완료")
IS_TYPE = ("확인 필요", "가정", "의사결정 필요", "연결되지 않은 항목", "정의 간 불일치")
IS_STATUS = ("해결", "미해결", "보류")
MARK = {"[확인 필요]": "확인 필요", "[가정]": "가정", "[의사결정 필요]": "의사결정 필요"}
# DOC-00은 특정 문서가 아니라 폴더 공통(작성 기준, 상황판, 점검 도구)을 가리킨다
COMMON_DOC = "DOC-00"


def rd(p):
    return (ROOT / p).read_text(encoding="utf-8")


def isdate(v):
    if isinstance(v, datetime.date):
        return True
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v or "")))


def main():
    docs = yaml.safe_load(rd("_data/documents.yaml"))
    ch = yaml.safe_load(rd("_data/changes.yaml"))
    iss = yaml.safe_load(rd("_data/issues.yaml"))
    ch = ch if isinstance(ch, list) else ch.get("changes", [])
    iss = iss if isinstance(iss, list) else iss.get("issues", [])
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    D = {d["id"]: d for d in docs["documents"]}

    # 1. 문서 목록
    for i, d in D.items():
        if not (ROOT / d["file"]).exists():
            add("문서 파일이 없다", "%s %s" % (i, d["file"]))
        if d["status"] not in DOC_STATUS:
            add("문서 상태값이 규칙에 없다", "%s %s" % (i, d["status"]))
        if not isinstance(d["progress"], int) or not 0 <= d["progress"] <= 100:
            add("진행률이 0에서 100 사이가 아니다", "%s %s" % (i, d["progress"]))
        if not re.fullmatch(r"\d+\.\d+", str(d["version"])):
            add("판번호 형식이 다르다", "%s %s" % (i, d["version"]))
        if not isdate(d["updated"]):
            add("갱신일 형식이 다르다", "%s %s" % (i, d["updated"]))
        if d["status"] == "확정" and d["progress"] != 100:
            add("확정인데 진행률이 100이 아니다", i)

    # 2. 변경 이력
    for c in ch:
        who = c.get("id", "?")
        for k in ("id", "date", "type", "document", "summary", "status"):
            if not c.get(k):
                add("변경 이력에 빠진 항목", "%s : %s" % (who, k))
        if c.get("type") not in CH_TYPE:
            add("변경 구분이 규칙에 없다", "%s %s" % (who, c.get("type")))
        if c.get("status") not in CH_STATUS:
            add("변경 상태가 규칙에 없다", "%s %s" % (who, c.get("status")))
        if not isdate(c.get("date")):
            add("변경 날짜 형식이 다르다", "%s %s" % (who, c.get("date")))
        for t in [c.get("document")] + list(c.get("affects") or []):
            if t and t != COMMON_DOC and t not in D:
                add("없는 문서를 가리킨다", "%s → %s" % (who, t))
        if c.get("document") in (c.get("affects") or []):
            add("바꾼 문서를 영향 문서에도 적었다", who)

    # 3. 이슈
    for it in iss:
        who = it.get("id", "?")
        for k in ("id", "type", "document", "title", "status"):
            if not it.get(k):
                add("이슈에 빠진 항목", "%s : %s" % (who, k))
        if it.get("type") not in IS_TYPE:
            add("이슈 구분이 규칙에 없다", "%s %s" % (who, it.get("type")))
        if it.get("status") not in IS_STATUS:
            add("이슈 상태가 규칙에 없다", "%s %s" % (who, it.get("status")))
        if it.get("document") and it["document"] != COMMON_DOC and it["document"] not in D:
            add("없는 문서를 가리킨다", "%s → %s" % (who, it["document"]))
    # 해결일은 나중에 생긴 항목이다. 이 항목을 쓰기 시작한 날 이후 것만 본다
    since = min([str(i["raised"]) for i in iss if i.get("resolved") and i.get("raised")] or ["9999-12-31"])
    for it in iss:
        if it.get("status") == "해결" and not it.get("resolved") and str(it.get("raised", "")) >= since:
            add("해결인데 해결일이 없다", it.get("id"))

    # 4. 문서 표기와 이슈 등록
    open_marks = []
    for p in sorted((ROOT / "docs").glob("*.md")):
        for n, l in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            for mark, kind in MARK.items():
                if mark in l:
                    open_marks.append((p.name, n, kind, l.strip()[:50]))
    unresolved = [i for i in iss if i.get("status") != "해결"]
    for name, n, kind, txt in open_marks:
        if not unresolved:
            add("문서에 표기했으나 미해결 이슈가 없다", "%s:%d [%s] %s" % (name, n, kind, txt))
    for it in unresolved:
        doc = D.get(it.get("document"), {}).get("file", "")
        body = rd(doc) if doc and (ROOT / doc).exists() else ""
        if not any(m in body for m in MARK):
            add("미해결 이슈인데 문서에 표기가 없다", "%s %s" % (it["id"], it.get("title", "")))

    # 5. 상속 관계
    for i, d in D.items():
        for up in d.get("inherits") or []:
            if up not in D:
                add("상위 문서가 없다", "%s → %s" % (i, up))
        for down in D.values():
            if i in (down.get("inherits") or []) and down["id"] == i:
                add("자기 자신을 상위로 두었다", i)

    n = 0
    for k, v in bad.items():
        print("\n### %s (%d)" % (k, len(v)))
        for x in v[:15]:
            print("   -", x)
        if len(v) > 15:
            print("   ... 외 %d" % (len(v) - 15))
        n += len(v)
    print("\n문서 %d건, 변경 %d건, 이슈 %d건을 봤다." % (len(D), len(ch), len(iss)))
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
