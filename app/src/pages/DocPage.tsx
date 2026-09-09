import { Placeholder } from '@/components/Placeholder'

export function DocPage() {
  return (
    <Placeholder
      title="문서 보기"
      detail="문서 본문을 구역과 Flow 탭으로 나눠 둔다. 주소에 문서 번호, 구역, Flow를 담는다."
      source="docs/*.md"
    />
  )
}
