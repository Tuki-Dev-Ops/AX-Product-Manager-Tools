# -*- coding: utf-8 -*-
"""점검 묶음. python tools/check_all.py 로 실행한다.

점검 도구를 차례로 돌리고 결과를 한 표로 보여준다.
지적이 있으면 종료 코드 1을 낸다.

  --v   지적 내용까지 함께 출력한다
"""
import sys, subprocess, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKS = [
    ("check_ids",     "식별자 규칙과 중복"),
    ("check_data",    "문서 목록·변경 이력·이슈"),
    ("check_links",   "조사 파일과 절 참조"),
    ("check_terms",   "용어와 표기"),
    ("check_docs",    "문서 사이 정합"),
    ("check_screens", "공통 화면 규칙"),
    ("check_flow_chart", "순서도 표기"),
    ("check_flows",   "Flow 연결"),
    ("check_missing", "빠진 항목"),
    ("check_wording", "문장 기준"),
]


def run(name):
    p = ROOT / "tools" / ("%s.py" % name)
    if not p.exists():
        return None, ""
    r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"총 지적 (\d+)건", out)
    if m:
        return int(m.group(1)), out
    m = re.search(r"모두 (\d+)건", out)
    if m:
        return int(m.group(1)), out
    if "점검 결과 이상 없음" in out:
        return 0, out
    return None, out


def main():
    verbose = "--v" in sys.argv
    rows, total, skipped = [], 0, 0
    for name, what in CHECKS:
        n, out = run(name)
        if n is None:
            rows.append((name, what, "건너뜀"))
            skipped += 1
        else:
            rows.append((name, what, "이상 없음" if n == 0 else "지적 %d건" % n))
            total += n
        if verbose and n:
            print(out)
    w = max(len(r[0]) for r in rows)
    print("| 점검 | 보는 것 | 결과 |")
    print("| --- | --- | --- |")
    for name, what, res in rows:
        print("| %-*s | %-22s | %s |" % (w, name, what, res))
    print()
    if skipped:
        print("건너뛴 점검 %d개" % skipped)
    print("총 지적 %d건" % total if total else "모든 점검 이상 없음")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
