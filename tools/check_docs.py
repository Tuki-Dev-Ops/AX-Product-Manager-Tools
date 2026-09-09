# -*- coding: utf-8 -*-
"""문서 · Wireframe · 뷰어 전수 대조. python tools/check_docs.py 로 실행한다."""
import re, pathlib, collections, yaml, os, sys
os.chdir(pathlib.Path(__file__).resolve().parent.parent)
SC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
rd = lambda p: pathlib.Path(p).read_text(encoding="utf-8")
D5, D6, D7, D4, D3 = (rd("docs/0%s_%s.md" % (n, t)) for n, t in
    [(5,"IA"),(6,"Wireframe"),(7,"기능명세"),(4,"Flow"),(3,"서비스구조")])
bad = collections.defaultdict(list)
def X(cat, msg): bad[cat].append(msg)

# ── 06 파싱: 화면 블록
blocks = []   # (sid, title, frame, lines)
cur = None
for ln in D6.split("\n"):
    m = re.match(r"^# ([A-Z]{3}-[A-Z]{3,4}-[A-Z0-9]{3,6})\s+(.*)$", ln)
    if m:
        cur = [m.group(1), m.group(2).strip(), None, []]; blocks.append(cur); continue
    if cur is not None:
        if ln.startswith("@ "): cur[2] = ln[2:].strip()
        elif ln.startswith("```"): cur = None
        else: cur[3].append(ln)
wf_ids = [b[0] for b in blocks]
base_title = {}
for sid, t, fr, L in blocks:
    if " · " not in t and sid not in base_title: base_title[sid] = t
for sid, t, fr, L in blocks:
    # 기본 상태 없이 변형만 있는 화면은 변형 이름의 앞부분을 이름으로 본다
    if sid not in base_title: base_title[sid] = t.split(" · ")[0]
uniq6 = list(dict.fromkeys(wf_ids))

# ── 05 화면 목록 표
ia = {}   # sid -> (name, type, states)
for ln in D5.split("\n"):
    if not ln.startswith("|"): continue
    c = [x.strip() for x in ln.strip("|").split("|")]
    for i, x in enumerate(c):
        if re.fullmatch(r"[A-Z]{3}-[A-Z]{3,4}-[A-Z0-9]{3,6}", x):
            if i + 2 < len(c) and c[i+2] in ("페이지","레이어팝업","전체화면","모달","팝업"):
                ia[x] = (c[i+1], c[i+2], c[i+4] if i+4 < len(c) else "")
            break

# ── 07 명세
spec = {}
for m in re.finditer(r"^#### ([A-Z]{3}-[A-Z]{3,4}-[A-Z0-9]{3,6}) (.+)$", D7, re.M):
    sid = m.group(1)
    if sid in spec: X("07 명세 중복", sid)
    j = D7.find("\n#### ", m.end())
    spec[sid] = (m.group(2).strip(), D7[m.end(): j if j > 0 else len(D7)])

tr = yaml.safe_load(rd("_data/trace.yaml"))
tr_scr = {s["id"]: s for s in tr["screens"]}
tr_spec = {s["screen"] for s in tr["specs"]}
tr_flow = {f["id"]: f for f in tr["flows"]}

# ── 1. 화면 집합 일치
for sid in uniq6:
    if sid not in ia:      X("06에 있으나 05 화면 목록에 없음", sid)
    if sid not in spec:    X("06에 있으나 07 명세 없음", sid)
    if sid not in tr_scr:  X("06에 있으나 trace 없음", sid)
for sid in ia:
    if sid not in uniq6:   X("05에 있으나 06 Wireframe 없음", sid)
    if sid not in spec:    X("05에 있으나 07 명세 없음", sid)
for sid in spec:
    if sid not in ia:      X("07에 있으나 05 없음", sid)
for sid in tr_scr:
    if sid not in ia:      X("trace에 있으나 05 없음", sid)
    if sid not in tr_spec: X("trace 화면에 명세 없음", sid)

# ── 2. 화면명 일치
for sid in uniq6:
    n6 = base_title.get(sid, "")
    if sid in ia and ia[sid][0] != n6:   X("화면명 05≠06", "%s  05=%s  06=%s" % (sid, ia[sid][0], n6))
    if sid in spec and spec[sid][0] != n6: X("화면명 07≠06", "%s  07=%s  06=%s" % (sid, spec[sid][0], n6))
    if sid in tr_scr and tr_scr[sid].get("title") != n6: X("화면명 trace≠06", "%s  trace=%s  06=%s" % (sid, tr_scr[sid].get("title"), n6))

# ── 3. 유형 일치 (05 vs 07 표)
FR2TYPE = {"admin":"페이지","wpopup":"레이어팝업","wpopup2":"레이어팝업","popup":"레이어팝업",
           "popup2":"레이어팝업","mobile":"페이지","kiosk":"전체화면","split":"페이지","toast":"페이지"}
for sid, t, fr, L in blocks:
    if " · " in t: continue
    body = spec.get(sid, ("", ""))[1]
    m = re.search(r"\| 유형 \| (.+?) \|", body)
    if m and sid in ia and m.group(1).strip() != ia[sid][1]:
        X("유형 05≠07", "%s  05=%s  07=%s" % (sid, ia[sid][1], m.group(1).strip()))

# ── 4. 상태값 일치 (05 표 vs 07 상태값 행 vs 06 배지)
for sid in uniq6:
    s5 = set(x.strip() for x in re.split(r"[,·]", ia.get(sid, ("","",""))[2]) if x.strip() and x.strip() != "-")
    body7 = spec.get(sid, ("",""))[1]
    m = re.search(r"\| 상태값 \| (.+?) \|", body7)
    s7 = set(x.strip() for x in re.split(r"[,·]", m.group(1)) if x.strip()) if m else set()
    s7b = set(s7)
    for mm in re.finditer(r"\| [^|]*상태 \| (.+?) \|", body7):
        s7b |= set(x.strip() for x in re.split(r"[,·]", mm.group(1)) if x.strip())
    if s5 and s7 and s5 != s7:
        X("상태값 05≠07", "%s  05만=%s  07만=%s" % (sid, sorted(s5-s7), sorted(s7-s5)))
    badges = set()
    for _sid, _t, _fr, L in blocks:
        if _sid != sid: continue
        for ln in L: badges |= set(re.findall(r"\{([^}]+)\}", ln))
    unknown = {b for b in badges if s5 and b not in s5 and b not in s7b}
    if unknown and (s5 or s7):
        X("06 배지가 상태값에 없음", "%s  %s  (정의=%s)" % (sid, sorted(unknown), sorted(s5 or s7)))

# ── 5. 연결 Flow 존재
flow_ids = set(re.findall(r"^### (FL-\d{3})", D4, re.M))
for sid, (nm, body) in spec.items():
    m = re.search(r"\| 연결 Flow \| (.+?) \|", body)
    if not m: X("연결 Flow 행 없음", sid); continue
    for f in re.findall(r"FL-\d{3}", m.group(1)):
        if f not in flow_ids: X("없는 Flow 참조", "%s → %s" % (sid, f))

# ── 6. 명세 필수 절
for sid, (nm, body) in spec.items():
    for sec in ("**처리**", "**조건**", "**예외**"):
        if sec not in body: X("명세 절 누락", "%s  %s" % (sid, sec))

# ── 7. 뷰어/캔버스 지원 kind
page = rd(str(SC / "wf_page.html")) if SC and (SC / "wf_page.html").exists() else rd("dashboard/wireframe.html")
tpl = rd("tools/dashboard_template.html")
FIELDLIKE = {"f","f*","fo","fe","fx","fs","fd","fq","sel","selx","sele","selo",
             "fsx","fse","fso","fdx","fde","fdo","top","fe*","fo*","fs*"}
WIDTH = re.compile(r"^([a-z][a-z0-9]*\*?):[\d.]+$")
kinds = collections.Counter(); frames = collections.Counter()
for sid, t, fr, L in blocks:
    frames[fr] += 1
    for ln in L:
        s = ln.strip()
        if not s or s.startswith("!"): continue
        for cell in s.split(" | "):
            k = cell.strip().split(" ")[0]
            m2 = WIDTH.match(k)
            if m2: k = m2.group(1)
            if k: kinds[k] += 1
vf = (set(re.findall(r'k *===? *"([a-z0-9*]+)"', page))
      | set(re.findall(r'kind *===? *"([a-z0-9*]+)"', page)) | FIELDLIKE)
cf = (set(re.findall(r'k *===? *"([a-z0-9*]+)"', tpl))
      | set(re.findall(r'kind *===? *"([a-z0-9*]+)"', tpl)) | FIELDLIKE)
for k, n in kinds.items():
    if k not in vf: X("뷰어 미지원 kind", "%s (%d회)" % (k, n))
    if k not in cf: X("캔버스 미지원 kind", "%s (%d회)" % (k, n))
FRAME = set(re.findall(r"^\s*(\w+)\s*:\s*\[", page[page.index("const FRAME"):page.index("const FRAME")+900], re.M))
for f, n in frames.items():
    if f and f not in FRAME: X("뷰어 FRAME 없음", "%s (%d회)" % (f, n))
    if not f: X("@ frame 지정 없음", "%d개 블록" % n)

# ── 8. 05 화면 수 표 대조
CH = {"ADM":"내부 어드민","STR":"가맹 어드민","WEB":"하이브리드 웹앱","KSK":"키오스크"}
cnt = collections.Counter()
for sid in uniq6:
    tp = ia.get(sid, ("","",""))[1]
    cnt[(CH.get(sid[:3], sid[:3]), tp)] += 1
print("== 실제 화면 수 ==")
tot = collections.Counter()
for ch in ("내부 어드민","가맹 어드민","하이브리드 웹앱","키오스크"):
    p = cnt[(ch,"페이지")]; l = cnt[(ch,"레이어팝업")]; f = cnt[(ch,"전체화면")]
    tot["페이지"] += p; tot["레이어팝업"] += l; tot["전체화면"] += f
    print("  %-10s 페이지 %2d  레이어팝업 %2d  전체화면 %2d  = %d" % (ch, p, l, f, p+l+f))
print("  %-10s 페이지 %2d  레이어팝업 %2d  전체화면 %2d  = %d" %
      ("합계", tot["페이지"], tot["레이어팝업"], tot["전체화면"], sum(tot.values())))
print("  Wireframe 블록 %d / 화면 %d / 05표 %d / 07명세 %d / trace %d" %
      (len(blocks), len(uniq6), len(ia), len(spec), len(tr_scr)))

# ── 9. 매장 상태 파급
print("\n== '개설 준비' 언급 ==")
for f in ("docs/02_기획검토.md","docs/03_서비스구조.md","docs/04_Flow.md","docs/05_IA.md","docs/06_Wireframe.md","docs/07_기능명세.md","docs/08_검토결과.md"):
    print("  %-24s %d" % (f, rd(f).count("개설 준비")))

print("\n" + "=" * 60)
n = 0
for cat in sorted(bad):
    print("\n### %s (%d)" % (cat, len(bad[cat])))
    for m in bad[cat][:25]: print("   -", m)
    if len(bad[cat]) > 25: print("   ... 외 %d" % (len(bad[cat]) - 25))
    n += len(bad[cat])
print("\n총 지적 %d건" % n)

# ── 10. 8절 겹침 요소 표 수록 여부
sec8 = D5[D5.index("### 8.2"):]
listed = set(re.findall(r"^\| ([A-Z]{3}-[A-Z]{3,4}-[A-Z0-9]{3,6}) \|", sec8, re.M))
for sid in ia:
    if sid not in listed: X("05 8절 겹침 요소 표에 없음", sid)
for sid in listed:
    if sid not in ia: X("8절에만 있는 화면", sid)
n2 = sum(len(v) for v in bad.values())
if n2 != n:
    print("\n### 8절 점검")
    for cat in ("05 8절 겹침 요소 표에 없음", "8절에만 있는 화면"):
        if bad[cat]:
            print("  %s (%d): %s" % (cat, len(bad[cat]), ", ".join(bad[cat][:20])))
    print("  총 %d건" % (n2 - n))
