import { RiskSummaryCard } from "../components/RiskSummaryCard";
import { TransactionTable } from "../components/TransactionTable";
import { sampleTransactions } from "../services/api";

export function DashboardPage() {
  return (
    <main className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">SafePay Admin</p>
          <h1>온라인 쇼핑 사기 탐지 대시보드</h1>
          <p className="hero-copy">
            거래 수집, 위험 점수 계산, 사기 거래 차단 결과를 한 화면에서 확인하기 위한 기본 뼈대입니다.
          </p>
        </div>
      </header>

      <section className="summary-grid">
        <RiskSummaryCard title="실시간 거래" value="128건" tone="neutral" />
        <RiskSummaryCard title="의심 거래" value="12건" tone="warning" />
        <RiskSummaryCard title="차단 거래" value="4건" tone="danger" />
      </section>

      <TransactionTable items={sampleTransactions} />
    </main>
  );
}
