import './Placeholder.css'

type Props = {
  title: string
  detail: string
  source?: string
}

/** 화면을 옮기기 전까지 자리를 표시한다. 무엇이 들어올지와 원천을 함께 적는다. */
export function Placeholder({ title, detail, source }: Props) {
  return (
    <section className="ph">
      <h2>{title}</h2>
      <p>{detail}</p>
      {source ? <p className="ph-src">원천 {source}</p> : null}
    </section>
  )
}
