# -*- coding: utf-8 -*-
"""순서도 표기 점검. python tools/check_flow_chart.py 로 실행한다.

ISO 5807을 따른다. 흐름은 위에서 아래로 두고, 판단의 각 출구에 조건 값을 적는다.

  1 절 제목이 'FL-번호 이름 (화면ID)' 형태인지
  2 판단(?로 끝나는 줄) 뒤에 분기가 있는지
  3 분기(├─ └─)의 각 출구에 조건 값이 있는지
  4 판단 없이 분기만 있는 곳이 없는지
  5 흐름 기호(↓)로 이어지는지
  6 한 Flow가 다른 Flow로 넘어갈 때 있는 번호를 가리키는지
"""
import re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z0-9]{3,6}"


def main():
    s = (ROOT / "docs" / "04_Flow.md").read_text(encoding="utf-8")
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    flows = list(re.finditer(r"^### (FL-\d{3}) (.+)$", s, re.M))
    ids = {m.group(1) for m in flows}
    n_blocks = 0

    for k, m in enumerate(flows):
        fid, title = m.group(1), m.group(2)
        end = flows[k + 1].start() if k + 1 < len(flows) else len(s)
        body = s[m.end():end]

        # 1. 제목 형태
        if "(" in title:
            inside = title[title.index("(") + 1: title.rindex(")")] if ")" in title else ""
            for part in [x.strip() for x in inside.split("/")]:
                # 배치처럼 화면이 아닌 표기는 그대로 둔다
                if not re.match(r"^[A-Z]", part):
                    continue
                if part and not re.fullmatch(SID, part):
                    add("제목의 화면ID 형식이 다르다", "%s : %s" % (fid, part))

        for blk in re.findall(r"```text\n(.*?)```", body, re.S):
            n_blocks += 1
            lines = [l.rstrip() for l in blk.split("\n") if l.strip()]
            for i, l in enumerate(lines):
                t = l.strip()

                # 2. 판단 뒤에는 분기가 온다
                if t.endswith("?"):
                    nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    if not nxt.startswith(("├─", "└─", "│")):
                        add("판단 뒤에 분기가 없다", "%s : %s" % (fid, t[:40]))

                # 3. 분기에는 조건 값을 적는다
                if t.startswith(("├─", "└─")):
                    v = t[2:].strip()
                    if not v:
                        add("분기에 조건 값이 없다", "%s : %s" % (fid, l[:40]))
                    # 판단 출구인데 화살표만 있는 경우
                    elif v.startswith("→"):
                        add("분기에 조건 값이 없다", "%s : %s" % (fid, l[:40]))

                # 5. 이어지는 기호
                if t == "↓" and i + 1 >= len(lines):
                    add("흐름 기호로 끝난다", "%s" % fid)

            # 4. 판단 없는 분기 묶음
            for i, l in enumerate(lines):
                if l.strip().startswith("├─"):
                    prev = lines[i - 1].strip() if i else ""
                    if prev.startswith(("├─", "└─")):
                        continue
                    # 판단이거나 목록을 펼치는 줄이면 넘어간다
                    if prev.endswith("?") or prev.endswith((":", "…")) or prev:
                        continue
                    add("판단 없이 분기만 있다", "%s : %s" % (fid, l[:40]))

            # 6. 다른 Flow 참조
            for f in re.findall(r"FL-\d{3}", blk):
                if f not in ids:
                    add("없는 Flow로 넘어간다", "%s → %s" % (fid, f))

    n = 0
    for k, v in bad.items():
        uniq = list(dict.fromkeys(v))
        print("\n### %s (%d)" % (k, len(uniq)))
        for x in uniq[:15]:
            print("   -", x)
        if len(uniq) > 15:
            print("   ... 외 %d" % (len(uniq) - 15))
        n += len(uniq)
    print("\nFlow %d건, 순서도 %d개를 봤다." % (len(flows), n_blocks))
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
