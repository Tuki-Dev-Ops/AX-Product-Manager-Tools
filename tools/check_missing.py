# -*- coding: utf-8 -*-
"""누락 점검. python tools/check_missing.py 로 실행한다.

빠지기 쉬운 것만 본다.

  1 정의한 상태값이 화면에 한 번도 안 나오는 경우
  2 되돌릴 수 없는 동작에 확인 팝업이 없는 경우
  3 처리 동작이 있는데 결과 안내가 없는 경우
  4 목록 명세에 목록 구성 표가, 입력 명세에 입력 항목 표가 없는 경우
  5 화면이 Flow 본문에 한 번도 안 나오는 경우
  6 요구사항·기능·Flow·화면·명세를 잇는 고리가 한쪽에서 끊긴 경우
  7 법으로 표시해야 하는 항목이 화면에서 빠진 경우
  8 보내기로 한 알림이 Flow에 없는 경우
"""
import re, sys, pathlib, collections, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z0-9]{3,6}"

# 되돌릴 수 없거나 값을 바꾸는 동작. 확인 팝업을 요구한다
CONFIRM = ("삭제", "폐점", "확정", "초기화", "중지", "해제", "실행", "파기", "재설정")
# 전자상거래법 제13조 제1항에 따라 판매자 정보 화면이 갖춰야 하는 항목
SELLER = ("상호", "대표자", "사업자등록번호", "통신판매업", "주소", "연락처")


def rd(p):
    return (ROOT / p).read_text(encoding="utf-8")


def screens():
    """06 Wireframe의 화면 블록"""
    out, cur = [], None
    for ln in rd("docs/06_Wireframe.md").split("\n"):
        m = re.match(r"^# (%s)\s*(.*)$" % SID, ln)
        if m:
            cur = {"id": m.group(1), "name": m.group(2).strip(), "rows": [], "frame": ""}
            cur["state"] = cur["name"].split(" · ")[1] if " · " in cur["name"] else ""
            out.append(cur); continue
        if cur is None:
            continue
        if ln.startswith("@ "):
            cur["frame"] = ln[2:].strip()
        elif ln.startswith("```"):
            cur = None
        else:
            cur["rows"].append(ln)
    return out


def specs():
    s = rd("docs/07_기능명세.md")
    out = {}
    for m in re.finditer(r"^#### (%s) (.+)$" % SID, s, re.M):
        j = s.find("\n#### ", m.end())
        out[m.group(1)] = s[m.end(): j if j > 0 else len(s)]
    return out


def main():
    S = screens()
    by = collections.defaultdict(list)
    for s in S:
        by[s["id"]].append(s)
    SP = specs()
    d5 = rd("docs/05_IA.md")
    d4 = rd("docs/04_Flow.md")
    d2 = rd("docs/02_기획검토.md")
    tr = yaml.safe_load(rd("_data/trace.yaml"))
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    # 1. 정의만 하고 화면에 없는 상태값
    for sid, group in by.items():
        body = SP.get(sid, "")
        m = re.search(r"\| 상태값 \| (.+?) \|", body)
        if not m:
            continue
        badges = set()
        for s in group:
            for l in s["rows"]:
                badges |= set(re.findall(r"\{([^}]+)\}", l))
        for st in [x.strip() for x in re.split(r"[,·]", m.group(1)) if x.strip()]:
            seen = st in badges or any(st in l for s in group for l in s["rows"])                 or any(st in s["name"] for s in group)
            if not seen:
                add("정의한 상태값이 화면에 없다", "%s  %s" % (sid, st))

    # 2·3. 되돌릴 수 없는 동작의 확인 팝업과 결과 안내
    sec8 = d5[d5.index("### 8.2"):] if "### 8.2" in d5 else ""
    for ln in sec8.split("\n"):
        c = [x.strip() for x in ln.strip("|").split("|")]
        if len(c) < 6 or not re.fullmatch(SID, c[0]):
            continue
        sid, act, res = c[0], c[4], c[5]
        if act and act != "-":
            names = [a.strip() for a in re.split(r"[,·]", act) if a.strip()]
            needs = [a for a in names if any(w in a for w in CONFIRM)]
            has = any("확인" in s["state"] for s in by.get(sid, [])) \
                or "확인 팝업" in act or "ADM-COMN-CONF" in ln or "확인 팝업" in res
            if needs and not has:
                add("되돌릴 수 없는 동작에 확인 팝업이 없다", "%s  %s" % (sid, ", ".join(needs)))
            if res in ("", "-"):
                add("동작은 있는데 결과 안내가 없다", "%s  %s" % (sid, act))

    # 4. 명세의 구성 표
    for sid, group in by.items():
        body = SP.get(sid, "")
        base = group[0]
        rows = base["rows"]
        has_table = any(l.startswith("t ") for l in rows)
        has_field = any(re.match(r"^(f|fo|fs|fd|sel|box)[x*eo]?(:[\d.]+)?\s", l) for l in rows)
        saves = any(re.search(r"b(:[\d.]+)? (저장|등록|발급|변경)", l) for l in rows)
        if has_table and sid.endswith(("LIST", "COMP")) and "**목록 구성**" not in body:
            add("목록 명세에 목록 구성 표가 없다", sid)
        if has_field and saves and "**입력 항목**" not in body:
            add("입력 명세에 입력 항목 표가 없다", sid)

    # 5. Flow 본문에 나오지 않는 화면
    names = {}
    for m in re.finditer(r"^\| [^|]*\| (%s) \| ([^|]+) \|" % SID, d5, re.M):
        names[m.group(1)] = m.group(2).strip()
    for sid in by:
        if sid in d4:
            continue
        nm = names.get(sid, "")
        if nm and re.search(r"(^|\W)%s(\W|$)" % re.escape(nm), d4):
            continue
        add("Flow 본문에 나오지 않는 화면", "%s %s" % (sid, nm))

    # 6. 추적 고리
    req = {r["id"]: r for r in tr["requirements"]}
    fn = {f["id"]: f for f in tr["functions"]}
    fl = {f["id"]: f for f in tr["flows"]}
    scr = {s["id"]: s for s in tr["screens"]}
    spec_of = {s["screen"] for s in tr["specs"]}
    for i, r in req.items():
        if not r.get("functions"):
            add("요구사항에 기능이 없다", i)
        for f in r.get("functions") or []:
            if f not in fn:
                add("없는 기능을 가리킨다", "%s → %s" % (i, f))
    for i, f in fn.items():
        if not f.get("requirements"):
            add("기능에 요구사항이 없다", i)
        if not any(i in (x.get("functions") or []) for x in fl.values()) \
           and not any(i in (x.get("functions") or []) for x in scr.values()):
            add("기능이 Flow와 화면 어디에도 없다", i)
    # 서비스 전체 흐름(FL-00x)과 화면 조작 공통 Flow(FL-6xx)는 특정 화면에 매이지 않는다
    NO_SCREEN_OK = re.compile(r"^FL-(00\d|6\d\d)$")
    for i, f in fl.items():
        if not f.get("screens") and not NO_SCREEN_OK.match(i):
            add("Flow에 화면이 없다", i)
    for i, s in scr.items():
        if i not in spec_of:
            add("화면에 명세가 없다", i)
        if not any(i in (x.get("screens") or []) for x in fl.values()):
            add("화면이 어느 Flow에도 없다", i)

    # 7. 법정 표시 항목
    for sid in ("WEB-INFO-SELL", "KSK-INFO-SELL"):
        txt = "\n".join(l for s in by.get(sid, []) for l in s["rows"])
        for item in SELLER:
            if item not in txt:
                add("판매자 정보에 법정 항목이 없다", "%s  %s" % (sid, item))

    # 8. 보내기로 한 알림
    if "#### 알림톡 템플릿" in d2:
        blk = d2[d2.index("#### 알림톡 템플릿"):]
        blk = blk[:blk.index("\n#### ")] if "\n#### " in blk else blk
        for m in re.finditer(r"^\| ([^|]+?) \| #\{매장명\}", blk, re.M):
            when = m.group(1).strip()
            if when in ("보낼 때", "---"):
                continue
            key = {"접수": "접수", "거절": "거절", "준비 완료": "준비 완료", "미수령 마감": "미수령"}.get(when, when)
            if key not in d4:
                add("보내기로 한 알림이 Flow에 없다", when)

    n = 0
    for k, v in bad.items():
        print("\n### %s (%d)" % (k, len(v)))
        for x in v[:15]:
            print("   -", x)
        if len(v) > 15:
            print("   ... 외 %d" % (len(v) - 15))
        n += len(v)
    print("\n화면 %d개, 명세 %d건, Flow %d건을 봤다." % (len(by), len(SP), len(fl)))
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
