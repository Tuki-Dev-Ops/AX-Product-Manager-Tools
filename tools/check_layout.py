# -*- coding: utf-8 -*-
"""배치와 표기 점검. python tools/check_layout.py 로 실행한다.

화면마다 갈리기 쉬운 배치와 표기를 맞춘다.

  1 조회·초기화 버튼의 폭
  2 검색 칸의 폭
  3 날짜 표기
  4 목록의 첫 두 열
  5 한 열 안에서 금액 단위 혼용
  6 기간 버튼이 여러 줄로 쪼개진 곳
  7 한 화면에서 같은 라벨 버튼의 폭이 다른 곳
  8 요약 지표 개수
"""
import re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z0-9]{3,6}"
DESK = ("admin", "popup", "popup2", "wpopup", "wpopup2", "split", "center")
PRESET = re.compile(r"^b2(:[\d.]+)?\s+(오늘|어제|최근 \d+일|\d+일|이번 달|지난달|행사 전체 기간)$")


def screens():
    out, cur = [], None
    for ln in (ROOT / "docs" / "06_Wireframe.md").read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^# (%s)\s*(.*)$" % SID, ln)
        if m:
            cur = {"id": m.group(1), "name": m.group(2).strip(), "rows": [], "frame": ""}
            out.append(cur); continue
        if cur is None:
            continue
        if ln.startswith("@ "):
            cur["frame"] = ln[2:].strip().split(" ")[0]
        elif ln.startswith("```"):
            cur = None
        elif ln.strip():
            cur["rows"].append(ln.rstrip())
    return out


def cells(l):
    return [c.strip() for c in l.split("|")]


def tcells(l):
    out, dep, cur = [], 0, ""
    for k, ch in enumerate(l):
        if ch in "([":
            dep += 1
        elif ch in ")]":
            dep = max(0, dep - 1)
        if ch == "," and dep == 0 and (k + 1 >= len(l) or l[k + 1] == " "):
            out.append(cur.strip()); cur = ""; continue
        cur += ch
    out.append(cur.strip())
    return out


def main():
    S = screens()
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    for s in S:
        sid, st = s["id"], s["name"].split(" · ")[-1] if " · " in s["name"] else "기본"
        where = "%s %s" % (sid, st)
        desk = s["frame"] in DESK
        labels = collections.defaultdict(set)

        for l in s["rows"]:
            cs = cells(l)

            # 1. 조회·초기화 버튼 폭
            if desk:
                for c in cs:
                    m = re.match(r"^(b|b2)(:([\d.]+))?\s+(조회|초기화|조건 초기화)$", c)
                    if m and m.group(4) != "조건 초기화":
                        if m.group(3) != "0.5":
                            add("조회·초기화 버튼 폭이 0.5가 아니다", "%s : %s" % (where, c))

            # 2. 검색 칸 폭
            if desk:
                for c in cs:
                    m = re.match(r"^fq(:([\d.]+))?\s", c)
                    if m and m.group(2) != "2":
                        add("검색 칸 폭이 2가 아니다", "%s : %s" % (where, c.split("//")[0].strip()))

            # 3. 날짜 표기
            for m in re.finditer(r"\b\d{2}\.\d{2}\b", l):
                add("날짜를 마침표로 끊었다", "%s : %s" % (where, m.group(0)))

            # 4. 목록의 첫 두 열
            if l.startswith("t "):
                head = tcells(l[2:])
                if head[0] == "[]" and len(head) > 1 and head[1] not in ("#", "#v", "#^"):
                    add("목록 둘째 열이 순번이 아니다", "%s : %s" % (where, head[1]))

            # 6. 기간 버튼은 앞 조건 줄이나 세그먼트 줄의 오른쪽에 붙인다
            pres = [c for c in cs if PRESET.match(c)]
            if pres and all(PRESET.match(c) or c == "sp" for c in cs):
                add("기간 버튼만 있는 줄을 따로 두었다", "%s : %s" % (where, l[:50]))

            # 6-2. 조회와 초기화는 조건 줄의 오른쪽 끝에 둔다
            if desk and cs and re.match(r"^b2?(:[\d.]+)?\s+(조회|초기화)$", cs[0]):
                add("조회 버튼을 조건 줄과 떼어 놓았다", "%s : %s" % (where, l[:50]))

            # 6-3. 등록 버튼은 머리말 오른쪽에 둔다
            if desk and len(cs) > 1:
                for c in cs:
                    if re.match(r"^b(:[\d.]+)?\s+\+", c) and any(
                            re.match(r"^(fd|sel|fq|chk)", x) for x in cs):
                        add("등록 버튼을 조건 줄에 두었다", "%s : %s" % (where, c))

            # 7. 같은 라벨 버튼의 폭
            for c in cs:
                m = re.match(r"^(b|b2|bd)(:([\d.]+))?\s+(.+)$", c)
                if m:
                    labels[m.group(4)].add((m.group(1), m.group(3) or "1"))

            # 8. 요약 지표 개수
            n = len([c for c in cs if c.startswith("stat ")])
            if n and not 3 <= n <= 4:
                add("요약 지표가 3~4개가 아니다", "%s : %d개" % (where, n))

        for lab, kinds in labels.items():
            if len(kinds) > 1:
                add("한 화면에서 같은 버튼의 폭이 다르다", "%s : %s %s" % (where, lab, sorted(kinds)))

        # 5. 한 열에서 금액 단위 혼용
        head, rows = None, []
        for l in s["rows"] + ["#끝"]:
            if l.startswith("t "):
                head, rows = tcells(l[2:]), []
            elif l.startswith("td ") and head is not None:
                rows.append(tcells(l[3:]))
            elif head is not None:
                for k, name in enumerate(head):
                    u = set()
                    for r in rows:
                        if k < len(r):
                            m = re.search(r"[\d,]+(천원|원)\b", r[k])
                            if m:
                                u.add(m.group(1))
                    if len(u) > 1:
                        add("한 열에서 금액 단위를 섞었다", "%s : %s %s" % (where, name, sorted(u)))
                head, rows = None, []

    n = 0
    for k, v in bad.items():
        uniq = list(dict.fromkeys(v))
        print("\n### %s (%d)" % (k, len(uniq)))
        for x in uniq[:15]:
            print("   -", x)
        if len(uniq) > 15:
            print("   ... 외 %d" % (len(uniq) - 15))
        n += len(uniq)
    print("\n화면 %d개를 봤다." % len(S))
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
