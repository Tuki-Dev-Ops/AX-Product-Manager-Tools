import { Placeholder } from '@/components/Placeholder'

export function HomePage() {
  return (
    <Placeholder
      title="문서별 작업"
      detail="문서 8종의 상태, 진행률, 상위·하위 관계를 표로 둔다."
      source="_data/documents.yaml"
    />
  )
}
