# -*- coding: utf-8 -*-
"""요구사항 문장을 ISO/IEC/IEEE 29148 기준으로 점검한다.

5.2.4 의무는 평서형으로 적고 권장과 구분한다. 부정문과 수동태를 피한다.
5.2.7 최상급, 주관적 표현, 모호한 대명사, 개방형 표현, 빠져나갈 구멍, 전체성 함의를 쓰지 않는다.
"""
import collections
import pathlib
import re
import sys

BAN = [
    ("최상급", r"최적의|최고의|최상의|가장 (?:빠른|좋은|많은)|최대한"),
    ("주관적 표현", r"쉽게|편리하게|간편하게|직관적|사용자 친화|빠르게 처리|원활"),
    ("모호한 지시어", r"(?:^|\s)(?:그것|이것|해당 사항|위와 같이)(?:을|를|은|는|이|가|\s|$)"),
    ("개방형 표현", r"등등|기타 등|및 기타|등을 (?:포함|제공)|등의 기능"),
    ("빠져나갈 구멍", r"가능하면|필요시|필요한 경우 |적절히|적절한 |상황에 따라|가급적|되도록"),
    ("전체성 함의", r"항상 |모든 경우|언제나|무조건"),
    ("권장 표현", r"권장한다|바람직하다|하는 것이 좋다|고려한다$"),
    ("모호한 정도", r"충분히|신속히|즉시 처리|다양한|여러 가지"),
]
SOFT = re.compile(r"(?:할 수 있도록 한다|하도록 지원한다|되어야 한다|해야 한다)$")


def rows(path, pat):
    out = []
    for i, l in enumerate(pathlib.Path(path).read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(pat, l.strip())
        if m:
            out.append((i, m.group(1), m.group(2).strip()))
    return out


def main():
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    src = [
        ("docs/01_프로젝트개요.md", r"^\|\s*(REQ-\d+)\s*\|\s*([^|]+)\|"),
        ("docs/01_프로젝트개요.md", r"^\|\s*(NFR-\d+)\s*\|\s*([^|]+)\|"),
    ]
    n = 0
    for path, pat in src:
        for line, rid, text in rows(path, pat):
            n += 1
            for name, rx in BAN:
                m = re.search(rx, text)
                if m:
                    add(name, "%s %s … %s" % (rid, m.group(0).strip(), text[:44]))
            if SOFT.search(text):
                add("의무를 평서형으로 적지 않았다", "%s … %s" % (rid, text[-30:]))

    # 05 화면 목록의 정책 칸과 07 명세의 조건·예외도 같은 기준으로 본다
    SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z]{3,6}"
    for line in pathlib.Path("docs/05_IA.md").read_text(encoding="utf-8").splitlines():
        m = re.search(r"\| (%s) \|" % SID, line)
        if not m or not line.rstrip().endswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 10:
            continue
        text = cells[-1]
        n += 1
        for name, rx in BAN:
            g = re.search(rx, text)
            if g:
                add(name, "%s %s … %s" % (m.group(1), g.group(0).strip(), text[:44]))
    cur = ""
    for line in pathlib.Path("docs/07_기능명세.md").read_text(encoding="utf-8").splitlines():
        h = re.match(r"^#### (%s)" % SID, line)
        if h:
            cur = h.group(1)
            continue
        if not line.startswith("* ") or not cur:
            continue
        text = line[2:].strip()
        n += 1
        for name, rx in BAN:
            g = re.search(rx, text)
            if g:
                add(name, "%s %s … %s" % (cur, g.group(0).strip(), text[:44]))
    print("점검한 문장 %d개" % n)
    if not bad:
        print("점검 결과 이상 없음")
        return 0
    tot = 0
    for k, v in bad.items():
        print("[%s] %d건" % (k, len(v)))
        for x in v[:12]:
            print("   ", x)
        if len(v) > 12:
            print("    ... 외 %d건" % (len(v) - 12))
        tot += len(v)
    print("모두 %d건" % tot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
