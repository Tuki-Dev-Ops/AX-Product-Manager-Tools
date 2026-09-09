# -*- coding: utf-8 -*-
"""참조 점검. python tools/check_links.py 로 실행한다.

문서가 가리키는 곳이 실제로 있는지 본다.

  1 조사 파일 참조가 실제 파일인지, 쓰이지 않는 조사 파일이 있는지
  2 문서 사이 파일 참조가 맞는지
  3 절 번호 참조가 실제 절인지
  4 조사 파일에 근거 URL이 있는지
  5 도구 참조가 실제 파일인지
"""
import re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = sorted((ROOT / "docs").glob("*.md"))
EXTRA = [ROOT / "README.md", ROOT / "CLAUDE.md"]


def main():
    files = [p for p in DOCS + EXTRA if p.exists()]
    text = {p.name: p.read_text(encoding="utf-8") for p in files}
    alltxt = "\n".join(text.values())
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    # 1. 조사 파일
    used = set()
    for name, s in text.items():
        for m in re.finditer(r"research/([^\s`)\]]+\.md)", s):
            f = m.group(1)
            used.add(f)
            if not (ROOT / "research" / f).exists():
                add("없는 조사 파일을 가리킨다", "%s → research/%s" % (name, f))
    have = {p.name for p in (ROOT / "research").glob("*.md")}
    for f in sorted(have - used):
        add("어느 문서도 가리키지 않는 조사 파일", f)

    # 2. 문서 사이 파일 참조
    for name, s in text.items():
        for m in re.finditer(r"docs/(\d{2}_[^\s`)\]]+\.md)", s):
            if not (ROOT / "docs" / m.group(1)).exists():
                add("없는 문서를 가리킨다", "%s → docs/%s" % (name, m.group(1)))

    # 3. 절 번호 참조. "2.10.4에", "8절에" 같은 표현을 본다
    heads = collections.defaultdict(set)
    for name, s in text.items():
        for m in re.finditer(r"^#{2,4} (\d+(?:\.\d+)*)[ .]", s, re.M):
            heads[name].add(m.group(1))
    allheads = set().union(*heads.values()) if heads else set()
    for name, s in text.items():
        for m in re.finditer(r"(?<![\d.])(\d+\.\d+(?:\.\d+)?)(?:에|은|는|을|를|의|에서|에는|과|와|,|\.| 참조| 항목)", s):
            v = m.group(1)
            if re.match(r"^\d+\.\d+$", v) and float(v.split(".")[0]) > 30:
                continue                       # 숫자 값은 건너뛴다
            if v not in allheads:
                continue                       # 절 번호로 보기 어려운 값은 건너뛴다
        for m in re.finditer(r"(\d+(?:\.\d+){1,2})(?:에 있다|에 둔다|에 적는다|를 참조|을 참조)", s):
            if m.group(1) not in allheads:
                add("없는 절을 가리킨다", "%s → %s" % (name, m.group(1)))
        for m in re.finditer(r"(\d+)절", s):
            if not any(h == m.group(1) or h.startswith(m.group(1) + ".") for h in allheads):
                add("없는 절을 가리킨다", "%s → %s절" % (name, m.group(1)))

    # 4. 조사 파일의 근거 URL
    for p in sorted((ROOT / "research").glob("*.md")):
        s = p.read_text(encoding="utf-8")
        if not re.search(r"https?://", s):
            add("근거 URL이 없는 조사 파일", p.name)

    # 5. 도구 참조
    for name, s in text.items():
        for m in re.finditer(r"tools/([A-Za-z_]+\.(?:py|html))", s):
            if not (ROOT / "tools" / m.group(1)).exists():
                add("없는 도구를 가리킨다", "%s → tools/%s" % (name, m.group(1)))

    n = 0
    for k, v in bad.items():
        uniq = list(dict.fromkeys(v))
        print("\n### %s (%d)" % (k, len(uniq)))
        for x in uniq[:15]:
            print("   -", x)
        if len(uniq) > 15:
            print("   ... 외 %d" % (len(uniq) - 15))
        n += len(uniq)
    print("\n문서 %d개, 조사 파일 %d개를 봤다." % (len(files), len(have)))
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
