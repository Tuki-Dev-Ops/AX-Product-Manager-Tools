# -*- coding: utf-8 -*-
"""데이터 사전 점검. python tools/check_fields.py 로 실행한다.

화면에 보이는 이름과 저장할 데이터가 어긋나지 않는지 본다.

  1 사전의 항목이 가리키는 화면이 실제로 있는지
  2 사전이 가리킨 화면에 그 이름이 있는지
  3 화면의 입력 칸이 사전에 있는지
  4 코드 집합의 값이 화면 상태값·문서와 같은지
  5 물리명이 규칙에 맞고 겹치지 않는지
"""
import re, sys, pathlib, collections, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SID = r"(?:ADM|STR|WEB|KSK)-[A-Z]{3,4}-[A-Z0-9]{3,6}"
FLD = ("f", "fx", "fe", "fo", "fd", "fdx", "fde", "fdo", "fs", "fsx", "fse", "fso",
       "sel", "selx", "sele", "selo", "fq", "box")
# 조회 조건이나 화면 표시에만 쓰는 이름. 저장하는 값이 아니다
SKIP = {"시작일", "종료일", "검색어", "표시", "열", "기준", "소속 기준", "비교 기준", "심사",
        "조회 조건", "기간", "인증번호", "다시 입력", "새 비밀번호", "비밀번호 재확인",
        "바꿀 시작 시각", "바꿀 종료 시각", "바꿀 연락처", "바꿀 준비 시간", "바꿀 판매가",
        "현재 영업시간", "현재 연락처", "현재 준비 시간", "현재 정산계좌", "현재 판매가",
        "도로명·건물명·지번", "상세주소", "매장명·사업자번호", "주문번호·휴대폰 뒤 4자리",
        "대상·내용", "이메일·이름", "대상 계정", "연동처", "담당자", "접근 키", "비밀 키",
        "매장 식사", "포장", "허용 범위", "정산 상태", "대사 단계", "배치 종류", "구분",
        "확인 여부", "수행업무", "변경 항목", "채널", "상태", "역할", "행사", "상권", "브랜드",
        "매장", "카테고리", "종류", "은행", "사유", "처리", "소속 행사", "참여 행사",
        "카드", "간편결제", "국내산", "한우", "글자 크게", "화면 낮추기", "음성 속도",
        "진행 표시", "카페", "매장 식사", "포장",
        "접수 대기 → 접수 완료 → 조리 중 → 조리 완료", "단말 상태 확인",
        "메뉴 갱신", "판매 메뉴 설정", "품절 설정"}


def rd(p):
    return (ROOT / p).read_text(encoding="utf-8")


def screens():
    """06 Wireframe에서 화면별 입력 칸 이름과 표 열을 모은다"""
    out, cur = {}, None
    for ln in rd("docs/06_Wireframe.md").split("\n"):
        m = re.match(r"^# (%s)" % SID, ln)
        if m:
            cur = m.group(1)
            out.setdefault(cur, {"labels": set(), "cols": set(), "badges": set(), "words": set()})
            continue
        if cur is None:
            continue
        if ln.startswith("t "):
            head = [h.rstrip("^v").strip() for h in tcells(ln[2:])]
            out[cur]["lasthead"] = head
            for h in head:
                if h and h not in ("[]", "#"):
                    out[cur]["cols"].add(h)
            continue
        if ln.startswith("td "):
            out[cur]["badges"] |= set(re.findall(r"\{([^}]+)\}", ln))
            head = out[cur].get("lasthead") or []
            if head[:1] in (["항목"], ["구분"], ["채널"], ["결제수단"]) and len(head) == 2:
                first = tcells(ln[3:])[0].strip()
                if first:
                    out[cur]["cols"].add(first)
            continue
        out[cur]["words"].add(re.sub(r"^[a-z0-9*:]+\s+", "", ln.strip()))
        for c in [x.strip() for x in ln.split(" | ")]:
            k = c.split(" ")[0].split(":")[0].rstrip("*")
            if k in FLD:
                body = c[len(c.split(" ")[0]):].strip()
                lab = body.split("//")[0].split("~")[0].strip()
                lab = re.sub(r"^\d+\s+", "", lab)
                lab = re.sub(r"\s*\(선택\)$", "", lab).strip()
                if lab and not lab.startswith("("):
                    out[cur]["labels"].add(lab)
    return out


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
    cfg = yaml.safe_load(rd("_data/fields.yaml"))
    S = screens()
    bad = collections.OrderedDict()

    def add(k, v):
        bad.setdefault(k, []).append(v)

    dict_labels = set()
    cols = collections.Counter()
    nf = 0
    for ent in cfg["entities"]:
        for f in ent["fields"]:
            nf += 1
            dict_labels.add(f["label"])
            for alt in f.get("also") or []:
                dict_labels.add(alt)
            cols[(ent["table"], f["column"])] += 1

            # 5. 물리명 규칙
            if not re.fullmatch(r"[a-z][a-z0-9_]*", f["column"]):
                add("물리명이 규칙과 다르다", "%s.%s" % (ent["table"], f["column"]))
            if f.get("need") not in ("필수", "선택", "자동"):
                add("필수 구분이 규칙에 없다", "%s %s : %s" % (ent["name"], f["label"], f.get("need")))
            if f.get("code") and f["code"] not in cfg["codes"]:
                add("없는 코드 집합을 가리킨다", "%s %s → %s" % (ent["name"], f["label"], f["code"]))

            # 1·2. 화면 참조
            for sid in f.get("screens") or []:
                if sid not in S:
                    add("사전이 없는 화면을 가리킨다", "%s %s → %s" % (ent["name"], f["label"], sid))
                    continue
                sc = S[sid]
                names = sc["labels"] | sc["cols"] | sc["words"]
                cand = [f["label"]] + list(f.get("also") or [])
                lab = f["label"]
                hit = any(x in names for x in cand) or any(
                    (y in x or x in y) and min(len(y), len(x)) >= 2
                    for y in cand for x in names)
                if not hit:
                    add("화면에 그 이름이 없다", "%s %s → %s" % (ent["name"], lab, sid))

    for (t, c), n in cols.items():
        if n > 1:
            add("한 표에 같은 물리명이 둘 이상", "%s.%s" % (t, c))

    # 3. 화면 입력 칸이 사전에 있는지
    for sid, sc in S.items():
        for lab in sc["labels"]:
            if lab in SKIP or lab in dict_labels:
                continue
            if re.fullmatch(r"[\d,·\s가-힣A-Za-z]*\d[\d,]*(원|건|개|분|%)?", lab):
                continue          # 값이 그대로 라벨로 들어간 예시
            if re.search(r"(그래프|이미지|미리보기|막대|그림)", lab):
                continue          # 자리만 잡아 둔 영역
            if "  " in lab or lab.endswith(")"):
                continue          # 값이나 보기를 그대로 적은 자리
            add("화면 입력 칸이 사전에 없다", "%s : %s" % (sid, lab))

    # 4. 코드 값이 화면 배지와 맞는지
    allcodes = set()
    for vals in cfg["codes"].values():
        allcodes |= {v for v in vals}
    for sid, sc in S.items():
        for b in sc["badges"]:
            if b not in allcodes:
                add("화면 배지가 코드 집합에 없다", "%s : %s" % (sid, b))

    n = 0
    for k, v in bad.items():
        uniq = list(dict.fromkeys(v))
        print("\n### %s (%d)" % (k, len(uniq)))
        for x in uniq[:15]:
            print("   -", x)
        if len(uniq) > 15:
            print("   ... 외 %d" % (len(uniq) - 15))
        n += len(uniq)
    print("\n개체 %d개, 항목 %d개, 코드 집합 %d개를 봤다."
          % (len(cfg["entities"]), nf, len(cfg["codes"])))
    print("총 지적 %d건" % n if n else "점검 결과 이상 없음")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
