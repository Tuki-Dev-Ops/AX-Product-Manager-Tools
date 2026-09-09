# -*- coding: utf-8 -*-
"""식별자 점검. python tools/check_ids.py 로 실행한다.

ISO/IEC/IEEE 29148 5.2.8.2를 따른다. 한 번 부여한 식별자는 바꾸지 않고,
삭제한 번호는 다시 쓰지 않는다.

  1 형식이 규칙에 맞는지
  2 같은 번호를 두 번 쓰지 않았는지
  3 문서가 가리키는 식별자가 실제로 정의되어 있는지
  4 정의만 하고 아무 데서도 안 쓰는 식별자가 있는지
  5 변경 이력과 이슈 번호가 연속인지
"""
import re, sys, pathlib, collections, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = sorted((ROOT / "docs").glob("*.md"))

# 식별자별 형식과 정의처
KIND = {
    "REQ": (r"REQ-\d{3}", "requirements"),
    "NFR": (r"NFR-\d{2}", None),
    "FN":  (r"FN-\d{3}",  "functions"),
    "FL":  (r"FL-\d{3}",  "flows"),
    "FS":  (r"FS-\d{3}",  "specs"),
    "UT":  (r"UT-\d{2}",  None),
    "DC":  (r"DC-\d{3}",  None),
    "SC":  (r"SC-\d{2}",  None),
    "CH":  (r"CH-\d{3}",  None),
    "IS":  (r"IS-\d{3}",  None),
}
SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z0-9]{3,6}"


def rd(p):
    return (ROOT / p).read_text(encoding="utf-8")


def main():
    text = {p.name: p.read_text(encoding="utf-8") for p in DOCS}
    alldoc = "\n".join(text.values())
    tr = yaml.safe_load(rd("_data/trace.yaml"))
    ch = yaml.safe_load(rd("_data/changes.yaml"))
    iss = yaml.safe_load(rd("_data/issues.yaml"))
    ch = ch if isinstance(ch, list) else ch.get("changes", [])
    iss = iss if isinstance(iss, list) else iss.get("issues", [])
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    # 1. 형식
    for pre, (pat, _) in KIND.items():
        for m in re.finditer(r"(?<![A-Za-z0-9])" + pre + r"-[0-9A-Za-z]+", alldoc):
            if not re.fullmatch(pat, m.group(0)):
                add("식별자 형식이 규칙과 다르다", m.group(0))

    # 2. 중복
    for key, items in (("추적표 요구사항", tr["requirements"]), ("추적표 기능", tr["functions"]),
                       ("추적표 Flow", tr["flows"]), ("추적표 화면", tr["screens"]),
                       ("변경 이력", ch), ("이슈", iss)):
        seen = collections.Counter(x.get("id") or x.get("screen") for x in items)
        for i, n in seen.items():
            if n > 1:
                add("%s에 같은 번호가 둘 이상" % key, "%s (%d회)" % (i, n))
    seen = collections.Counter(s["screen"] for s in tr["specs"])
    for i, n in seen.items():
        if n > 1:
            add("한 화면에 명세가 둘 이상", "%s (%d회)" % (i, n))

    # 3. 문서가 가리키는데 정의가 없는 식별자
    defined = {
        "REQ": {r["id"] for r in tr["requirements"]},
        "FN": {f["id"] for f in tr["functions"]},
        "FL": {f["id"] for f in tr["flows"]},
        "FS": {s["id"] for s in tr["specs"]},
        "CH": {c["id"] for c in ch},
        "IS": {i["id"] for i in iss},
    }
    for pre in ("UT", "SC", "NFR"):
        defined[pre] = set(re.findall(r"^\| (%s-\d+) \|" % pre, alldoc, re.M))
    # 의사결정 기록은 표가 아니라 절 제목으로 정의한다
    defined["DC"] = set(re.findall(r"^### (DC-\d{3})", alldoc, re.M))
    dup = [i for i in re.findall(r"^### (DC-\d{3})", alldoc, re.M)
           if re.findall(r"^### %s" % i, alldoc, re.M).__len__() > 1]
    for i in dict.fromkeys(dup):
        add("같은 의사결정 기록이 두 번 있다", i)
    for pre, (pat, _) in KIND.items():
        used = set(re.findall(pat, alldoc))
        for i in sorted(used - defined.get(pre, set())):
            add("문서가 가리키는데 정의가 없다", i)

    # 4. 정의만 하고 아무 데서도 안 쓰는 식별자. 추적표의 연결도 쓰임으로 본다
    linked = rd("_data/trace.yaml") + rd("_data/issues.yaml") + rd("_data/changes.yaml")
    for pre in ("REQ", "FN", "FL", "UT", "DC", "SC", "NFR"):
        for i in sorted(defined.get(pre, set())):
            if len(re.findall(i, alldoc)) + len(re.findall(i, linked)) <= 1:
                add("정의만 하고 아무 데서도 안 쓴다", i)

    # 화면ID: 문서와 추적표가 같은 집합인지
    scr_tr = {s["id"] for s in tr["screens"]}
    scr_doc = set(re.findall(r"^# (%s)" % SID, text["06_Wireframe.md"], re.M))
    for i in sorted(scr_doc - scr_tr):
        add("Wireframe에만 있는 화면ID", i)
    for i in sorted(scr_tr - scr_doc):
        add("추적표에만 있는 화면ID", i)
    for m in re.finditer(r"(?:ADM|STR|WEB|KSK)-[A-Za-z0-9-]+", alldoc):
        v = m.group(0)
        if not re.fullmatch(SID, v):
            add("화면ID 형식이 규칙과 다르다", v)

    # 5. 번호 연속성. 빠진 번호는 삭제한 것이므로 다시 쓰지 않았는지만 본다
    for key, items in (("변경 이력", ch), ("이슈", iss)):
        nums = sorted(int(x["id"].split("-")[1]) for x in items)
        gaps = [n for n in range(nums[0], nums[-1]) if n not in nums]
        if gaps:
            add("%s 번호가 비어 있다 (삭제분으로 본다)" % key,
                ", ".join("%03d" % g for g in gaps[:10]) + (" 외" if len(gaps) > 10 else ""))

    n = 0
    for k, v in bad.items():
        uniq = list(dict.fromkeys(v))
        print("\n### %s (%d)" % (k, len(uniq)))
        for x in uniq[:15]:
            print("   -", x)
        if len(uniq) > 15:
            print("   ... 외 %d" % (len(uniq) - 15))
        n += len(uniq)
    tot = sum(len(defined.get(p, ())) for p in KIND)
    print("\n식별자 %d개를 봤다." % tot)
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
