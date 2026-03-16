type RiskSummaryCardProps = {
  title: string;
  value: string;
  tone: "neutral" | "warning" | "danger";
};

export function RiskSummaryCard({ title, value, tone }: RiskSummaryCardProps) {
  return (
    <article className={`card tone-${tone}`}>
      <p className="card-title">{title}</p>
      <strong className="card-value">{value}</strong>
    </article>
  );
}
