# -*- coding: utf-8 -*-
"""기획 용어 점검. python tools/check_terms.py 로 실행한다.

  기본        용어 사전(_data/terms.yaml)과 문서를 대조해 어긋난 표기를 찾는다
  --list      용어 사전을 표로 출력한다
  --scan      사전에 없는 띄어쓰기 흔들림을 찾아 후보로 보여준다
"""
import re, sys, pathlib, collections, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = sorted((ROOT / "docs").glob("*.md"))
GLOSSARY_DOC = ROOT / "docs" / "03_서비스구조.md"


def load():
    return yaml.safe_load((ROOT / "_data" / "terms.yaml").read_text(encoding="utf-8"))


def lines():
    """(문서명, 줄번호, 줄) 목록. 코드 블록도 함께 본다."""
    out = []
    for p in DOCS:
        for n, l in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            out.append((p.name, n, l))
    return out


def masked(line, pats, phrases=()):
    """면제 구간을 지운 줄. 파일 경로, 알림톡 변수, 면제 구문은 점검하지 않는다."""
    for pat in pats:
        line = re.sub(pat + r"[^\s`]*" if pat.endswith("/") else pat, " ", line)
    for ph in phrases:
        line = line.replace(ph, " ")
    # 백틱 안은 표기를 인용한 것이므로 점검하지 않는다
    line = re.sub(r"`[^`]*`", " ", line)
    return line


def hit(word, line):
    """낱말 경계를 본다. 앞뒤가 한글이면 다른 낱말의 일부로 본다."""
    for m in re.finditer(re.escape(word), line):
        a = line[m.start() - 1] if m.start() else " "
        b = line[m.end()] if m.end() < len(line) else " "
        if re.match(r"[가-힣]", a) or re.match(r"[가-힣]", b):
            continue
        return True
    return False


def glossary_terms():
    s = GLOSSARY_DOC.read_text(encoding="utf-8")
    i = s.find("## 10. 용어 정의")
    if i < 0:
        return {}
    j = s.find("\n## ", i + 5)
    body = s[i: j if j > 0 else len(s)]
    return {m.group(1).strip(): m.group(2).strip()
            for m in re.finditer(r"^\| ([^|]+?) \| ([^|]+?) \|$", body, re.M)
            if m.group(1).strip() not in ("용어", "---")}


def main():
    cfg = load()
    pats = cfg.get("exempt_patterns", [])
    phrases = cfg.get("exempt_phrases", [])
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    if "--list" in sys.argv:
        print("| 용어 | 정의 | 쓰지 않는 표기 |")
        print("| --- | --- | --- |")
        for t in cfg["terms"]:
            print("| %s | %s | %s |" % (t["term"], t["definition"], ", ".join(t.get("avoid") or []) or "-"))
        return 0

    L = lines()

    if "--scan" in sys.argv:
        txt = "\n".join(masked(l, pats, phrases) for _, _, l in L)
        words = collections.Counter(re.findall(r"[가-힣]{2,10}", txt))
        known = {s["avoid"] for s in cfg["spacing"]} | {s["write"] for s in cfg["spacing"]}
        found = []
        for w, c in collections.Counter(re.findall(r"[가-힣]{1,6} [가-힣]{1,6}", txt)).items():
            j = w.replace(" ", "")
            if w in known or j in known:
                continue
            if words.get(j, 0):
                found.append((c + words[j], w, c, j, words[j]))
        found.sort(reverse=True)
        print("사전에 없는 띄어쓰기 흔들림 후보 %d건" % len(found))
        for _, w, c, j, jc in found[:30]:
            print("  %-18s %4d   %-16s %4d" % (w, c, j, jc))
        return 0

    # 1. 쓰지 않기로 한 용어
    for t in cfg["terms"]:
        for a in t.get("avoid") or []:
            for name, n, l in L:
                if hit(a, masked(l, pats, phrases)):
                    add("쓰지 않는 용어 '%s' (→ %s)" % (a, t["term"]), "%s:%d  %s" % (name, n, l.strip()[:60]))

    # 2. 띄어쓰기
    for s in cfg["spacing"]:
        for name, n, l in L:
            if hit(s["avoid"], masked(l, pats, phrases)):
                add("표기 '%s' (→ %s)" % (s["avoid"], s["write"]), "%s:%d  %s" % (name, n, l.strip()[:60]))

    # 3. 용어 사전과 03 문서의 정의 절이 어긋나는지
    g = glossary_terms()
    for t in cfg["terms"]:
        if t["term"] not in g:
            add("03 용어 정의 절에 없다", t["term"])
        elif g[t["term"]] != t["definition"]:
            add("정의가 다르다", "%s\n      사전 %s\n      03   %s" % (t["term"], t["definition"], g[t["term"]]))
    for k in g:
        if k not in {t["term"] for t in cfg["terms"]}:
            add("용어 사전에 없다", k)

    n = 0
    for k, v in bad.items():
        print("\n### %s (%d)" % (k, len(v)))
        for x in v[:12]:
            print("   -", x)
        if len(v) > 12:
            print("   ... 외 %d" % (len(v) - 12))
        n += len(v)
    print("\n용어 %d개, 띄어쓰기 규칙 %d개로 점검했다." % (len(cfg["terms"]), len(cfg["spacing"])))
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
