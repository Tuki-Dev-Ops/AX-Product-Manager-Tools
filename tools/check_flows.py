# -*- coding: utf-8 -*-
"""Flow가 서로 이어지는지 점검한다.

- 다른 Flow를 가리키는 참조가 실제로 있는 Flow인지
- 화면 참조가 실제로 있는 화면인지
- 어디에서도 가리키지 않는 Flow가 있는지
- 화면별 Flow가 그 화면에서 갈 수 있는 곳을 모두 그렸는지 (07 명세와 대조)
- 주문 상태 이름이 12절 정의와 같은지
"""
import collections
import pathlib
import re
import sys

SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z]{3,6}"


def flows():
    doc = pathlib.Path("docs/04_Flow.md").read_text(encoding="utf-8")
    out = collections.OrderedDict()
    parts = re.split(r"(?=^### FL-\d{3})", doc, flags=re.M)
    for b in parts:
        m = re.match(r"^### (FL-\d{3})\s*(.*)", b)
        if not m:
            continue
        head = m.group(2)
        out[m.group(1)] = {
            "title": head.split("(")[0].strip(),
            "screens": re.findall(SID, head),
            "body": b,
            "refs": [x for x in re.findall(r"FL-\d{3}", b) if x != m.group(1)],
            "used": re.findall(SID, b),
        }
    return out


def specs():
    doc = pathlib.Path("docs/07_기능명세.md").read_text(encoding="utf-8")
    out = {}
    for b in re.split(r"(?=^#### )", doc, flags=re.M):
        m = re.match(r"^#### (%s)" % SID, b)
        if not m:
            continue
        proc = re.search(r"\*\*처리\*\*\n\n(.*?)(?=\n\*\*|\n####|\Z)", b, re.S)
        fl = re.search(r"\| 연결 Flow \| (.+?) \|", b)
        out[m.group(1)] = {
            "goes": re.findall(SID, proc.group(1)) if proc else [],
            "flows": re.findall(r"FL-\d{3}", fl.group(1)) if fl else [],
        }
    return out


def main():
    F = flows()
    S = specs()
    wf = set(
        re.findall(
            r"^# (%s)" % SID,
            pathlib.Path("docs/06_Wireframe.md").read_text(encoding="utf-8"),
            re.M,
        )
    )
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    # 1. 없는 Flow를 가리킨다
    for fid, f in F.items():
        for r in set(f["refs"]):
            if r not in F:
                add("없는 Flow를 가리킨다", "%s → %s" % (fid, r))

    # 2. 없는 화면을 가리킨다
    for fid, f in F.items():
        for sc in set(f["used"]):
            if sc not in wf:
                add("없는 화면을 가리킨다", "%s → %s" % (fid, sc))

    # 3. 어디에서도 가리키지 않는 Flow. 05 IA와 07 명세에서 가리켜도 이어진 것으로 본다
    ref_to = set()
    for f in F.values():
        ref_to |= set(f["refs"])
    for f in ("docs/05_IA.md", "docs/07_기능명세.md"):
        ref_to |= set(re.findall(r"FL-\d{3}", pathlib.Path(f).read_text(encoding="utf-8")))
    ENTRY = {"FL-001", "FL-002", "FL-003", "FL-004", "FL-005"}
    for fid in F:
        if fid in ENTRY or fid in ref_to:
            continue
        # 화면별 Flow는 그 화면의 명세에서 가리키면 된다
        named = set(F[fid]["screens"])
        if any(fid in S.get(sc, {}).get("flows", []) for sc in named):
            continue
        add("어디에서도 가리키지 않는다", "%s %s" % (fid, F[fid]["title"]))

    # 4. 명세의 이동 대상이 그 화면 Flow에 없다.
    #    Flow 본문은 화면ID 대신 화면 이름으로 적으므로 둘 다 찾는다
    name = {}
    for line in pathlib.Path("docs/05_IA.md").read_text(encoding="utf-8").splitlines():
        m = re.search(r"\| (%s) \| ([^|]+) \|" % SID, line)
        if m:
            name[m.group(1)] = m.group(2).strip()
    for sc, sp in S.items():
        fids = [f for f in sp["flows"] if f in F]
        if not fids:
            continue
        body = " ".join(F[f]["body"] for f in fids)
        for g in set(sp["goes"]):
            if g == sc:
                continue
            if g in body:
                continue
            nm = name.get(g, "")
            if nm and (nm in body or nm.replace("·", "") in body.replace("·", "")):
                continue
            if any(f in body for f in S.get(g, {}).get("flows", [])):
                continue
            add("명세의 이동 대상이 Flow에 없다", "%s → %s %s (%s)" % (sc, g, nm, ", ".join(fids)))

    # 5. 화면 Flow가 명세에 연결되어 있지 않다
    for fid, f in F.items():
        for sc in f["screens"]:
            if sc in S and fid not in S[sc]["flows"]:
                add("화면 Flow가 명세의 연결 Flow에 없다", "%s ← %s" % (sc, fid))

    # 6. 주문 상태 이름. 12절 표에 정의한 값만 Flow와 화면에 쓴다
    doc = pathlib.Path("docs/04_Flow.md").read_text(encoding="utf-8")
    st = doc[doc.index("## 12. 주문 상태"):]
    known = set(re.findall(r"^\| ([가-힣 ]+?) \| ", st, re.M)) - {"상태"}
    wfdoc = pathlib.Path("docs/06_Wireframe.md").read_text(encoding="utf-8")
    ORDER = re.compile(r"\{([가-힣 ]+)\}")
    used = set()
    cur = ""
    for line in wfdoc.splitlines():
        m = re.match(r"^# (%s)" % SID, line)
        if m:
            cur = m.group(1)
        if line.startswith("td ") and "ORDR" in cur:
            used |= set(ORDER.findall(line))
    for u in sorted(used):
        if u not in known and u not in ("성공", "실패", "대체 발송"):
            add("12절에 없는 주문 상태를 화면에서 쓴다", u)

    print("Flow %d건, 화면 %d개, 명세 %d건" % (len(F), len(wf), len(S)))
    if not bad:
        print("점검 결과 이상 없음")
        return 0
    n = 0
    for k, v in bad.items():
        print("[%s] %d건" % (k, len(v)))
        for x in v[:15]:
            print("   ", x)
        if len(v) > 15:
            print("    ... 외 %d건" % (len(v) - 15))
        n += len(v)
    print("모두 %d건" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
