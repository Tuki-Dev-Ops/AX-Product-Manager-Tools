# -*- coding: utf-8 -*-
"""05 공통 화면 규칙을 06 Wireframe에 대해 점검한다."""
import pathlib, re, sys, collections

SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z]{3,6}"
FLD = ("f","fx","fe","fo","fd","fdx","fde","fdo","fs","fsx","fse","fso",
       "sel","selx","sele","selo","fq","box")
POPUP = ("popup","popup2","wpopup","mpopup","kpopup")


def load():
    L = pathlib.Path("docs/06_Wireframe.md").read_text(encoding="utf-8").split("\n")
    out, i, inf = [], 0, False
    while i < len(L):
        if L[i].startswith("```"):
            inf = not inf; i += 1; continue
        if inf and L[i].startswith("# "):
            j = i + 1
            while j < len(L) and not L[j].startswith("# ") and not L[j].startswith("```"):
                j += 1
            m = re.match(r"^# (%s) (.+)$" % SID, L[i])
            out.append({"id": m.group(1), "name": m.group(2), "line": i + 1,
                        "rows": [x for x in L[i+1:j] if x.strip()]})
            i = j; continue
        i += 1
    for s in out:
        s["frame"] = next((x[2:].strip() for x in s["rows"] if x.startswith("@ ")), "")
        s["kinds"] = set()
        for l in s["rows"]:
            for c in l.split("|"):
                s["kinds"].add(c.strip().split(" ")[0].split(":")[0])
        s["base"] = s["name"].split(" · ")[0]
        s["state"] = s["name"].split(" · ")[1] if " · " in s["name"] else ""
    return out


def cells(l):
    return [c.strip() for c in l.split("|")]


def head(c):
    m = re.match(r"^([a-z][a-z0-9]*)(\*?)(:[\d.]+)?\s*(.*)$", c)
    return m.groups() if m else None


def main():
    S = load()
    by = collections.defaultdict(list)
    for s in S:
        by[s["id"]].append(s)
    bad = collections.OrderedDict()

    def add(key, item):
        bad.setdefault(key, []).append(item)

    for sid, group in by.items():
        base = group[0]
        states = {s["state"] for s in group}
        haspage = "p" in base["kinds"]
        isl = haspage and base["frame"] in ("admin", "")
        ismod = base["frame"] in POPUP
        hasfld = any(k in FLD for k in base["kinds"])

        # 목록 화면은 결과 없음 상태를 갖춘다
        if isl and sid.endswith("LIST") and not any("결과 없음" in x for x in states):
            add("목록에 결과 없음 상태가 없다", sid)
        # 목록 화면은 조회 건수를 표시한다
        if isl and "cnt" not in base["kinds"]:
            add("목록에 조회 건수가 없다", sid)
        # 목록은 체크박스와 순번 두 열로 시작한다
        if isl:
            # 한 화면에 요약표와 목록이 함께 있으면 목록 쪽만 본다
            ths = [l for l in base["rows"] if l.startswith("t ")]
            if ths and not any(l.startswith("t [], ") for l in ths):
                add("목록에 선택 체크박스가 없다", "%s : %s" % (sid, ths[-1][2:38]))
        # 목록 화면은 기본 정렬 열을 표시한다
        if isl:
            ths = [l for l in base["rows"] if l.startswith("t ")]
            if ths and not any(re.search(r"[\^v]\s*(,|$)", t) for t in ths):
                add("목록에 정렬 방향 표시가 없다", sid)
        # 입력이 있는 모달은 검증 오류 상태를 갖춘다
        editable = any(re.match(r"^(f|fd|fs|sel|box)(:[\d.]+)?\s", l) for l in base["rows"])
        saves = any(re.search(r"b(:[\d.]+)? (저장|적용|다음|변경|발급)", l) for l in base["rows"])
        if ismod and editable and saves and not any("오류" in x or "미입력" in x for x in states):
            add("입력 모달에 검증 오류 상태가 없다", sid)

        for s in group:
            R = s["rows"]
            # 화면 머리말
            h = next((l for l in R if l.startswith("h ")), None)
            card = s["frame"] in ("split", "center", "mobile", "kiosk")
            if h is None and not card and "top" not in s["kinds"]:
                add("머리말이 없다", "%s %s" % (sid, s["state"] or "기본"))
            else:
                if s["frame"] == "admin" and "//" not in h:
                    add("화면 머리말에 용도 설명이 없다", "%s %s" % (sid, s["state"] or "기본"))
                if ismod and " ~ " in h:
                    add("모달 머리말에 동작 버튼이 있다", "%s %s" % (sid, s["state"] or "기본"))
            # 화면에 문서체 설명문을 두지 않는다. 약관 전문은 뺀다
            if sid != "WEB-INFO-POLI":
                for l in R:
                    if l.startswith("tx ") and re.search(r"(?<!니)다\.\s*$", l):
                        add("화면에 문서체 설명문이 있다", "%s %s : %s" %
                            (sid, s["state"] or "기본", l[3:40]))
            # 강조 버튼은 하나
            nb = sum(1 for l in R for c in cells(l) if re.match(r"^b(:[\d.]+)?(\s|$)", c))
            if nb > 1:
                add("강조 버튼이 둘 이상이다", "%s %s" % (sid, s["state"] or "기본"))
            # 필수와 선택 표기 혼용
            txt = "\n".join(R)
            if re.search(r"^(?:%s)\*" % "|".join(FLD), txt, re.M) and "(선택)" in txt:
                add("필수와 선택 표기를 섞었다", "%s %s" % (sid, s["state"] or "기본"))
            # 입력 칸에 라벨 (등록·수정과 인증 화면. 조회 조건 줄은 뺀다)
            tpos = next((k for k, l in enumerate(R) if l.startswith("t ")), len(R))
            for k2, l in enumerate(R):
                if k2 < tpos and any(x.startswith("t ") for x in R):
                    continue
                if re.search(r"b2?(:[\d.]+)? 조회", l):
                    continue
                # 조회 조건 줄: 기간, 상태, 검색어, 버튼, 건수로만 이루어진다
                ks = [head(c)[0] for c in cells(l) if head(c)]
                if ks and all(k in ("fd", "fdx", "fde", "fdo", "sel", "selx", "sele", "selo",
                                    "fq", "b", "b2", "bd", "sp", "cnt") for k in ks)                        and not any("//" in c and head(c) and head(c)[0] in ("f", "fs") for c in cells(l)):
                    continue
                for c in cells(l):
                    g = head(c)
                    if not g or g[0] not in FLD or g[0] in ("fq", "box"):
                        continue
                    if "//" not in c and not re.match(r"^f(:[\d.]+)? \d+$", c):
                        add("입력 칸에 라벨이 없다", "%s %s : %s" % (sid, s["state"] or "기본", c[:28]))
            # 오류 문구
            for l in R:
                if l.startswith("err ") and re.search(r"필수 항목|오류 문구|오류가 발생", l):
                    add("오류 문구가 무엇을 할지 알려주지 않는다", "%s %s" % (sid, s["state"] or "기본"))
            # 표 칸 수
            th = None
            for l in R:
                if l.startswith("t "):
                    th = split_cells(l[2:])
                elif l.startswith("td ") and th is not None:
                    if len(split_cells(l[3:])) != len(th):
                        add("표의 머리글과 본문 칸 수가 다르다", "%s %s" % (sid, s["state"] or "기본"))
            # 모달의 마지막 줄은 버튼
            if ismod and R:
                last = R[-1]
                ok = all(re.match(r"^(b|b2|bd)(:[\d.]+)?\s", c) or c == "sp" for c in cells(last))
                if not ok and "toast" not in last and not last.startswith("note"):
                    add("모달 끝에 버튼 줄이 없다", "%s %s" % (sid, s["state"] or "기본"))
            # 겹쳐 뜨는 판은 펼친 칸 뒤에 온다
            for k, l in enumerate(R):
                if l.startswith("menu ") or l.startswith("cal "):
                    prev = [c for x in R[:k] for c in x.split("|")
                            if re.match(r"^(fx|selx|fsx|fdx)\b", c.strip())]
                    if not prev:
                        add("펼친 칸 없이 목록이나 달력만 있다", "%s %s" % (sid, s["state"] or "기본"))
    return bad


def split_cells(s):
    out, d, cur = [], 0, ""
    for k, c in enumerate(s):
        if c in "([": d += 1
        elif c in ")]": d = max(0, d - 1)
        if c == "," and d == 0 and (k + 1 >= len(s) or s[k + 1] == " "):
            out.append(cur.strip()); cur = ""; continue
        cur += c
    out.append(cur.strip())
    return out


if __name__ == "__main__":
    bad = main()
    if not bad:
        print("점검 결과 이상 없음")
        sys.exit(0)
    n = 0
    for k, v in bad.items():
        print("[%s] %d건" % (k, len(v)))
        for x in v[:12]:
            print("   ", x)
        if len(v) > 12:
            print("    ... 외 %d건" % (len(v) - 12))
        n += len(v)
    print("모두 %d건" % n)
