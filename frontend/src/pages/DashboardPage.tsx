import { useCallback, useEffect, useState } from "react";
import { RiskSummaryCard } from "../components/RiskSummaryCard";
import { TransactionTable } from "../components/TransactionTable";
import { fetchTransactions } from "../services/api";
import { Transaction } from "../types/transaction";

export function DashboardPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTransactions = useCallback(() => {
    setLoading(true);
    setError(null);
    fetchTransactions()
      .then(setTransactions)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadTransactions();
  }, [loadTransactions]);

  const total = transactions.length;
  const held = transactions.filter((t) => t.status === "held").length;
  const blocked = transactions.filter((t) => t.status === "blocked").length;

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
        <RiskSummaryCard title="실시간 거래" value={loading ? "..." : `${total}건`} tone="neutral" />
        <RiskSummaryCard title="의심 거래" value={loading ? "..." : `${held}건`} tone="warning" />
        <RiskSummaryCard title="차단 거래" value={loading ? "..." : `${blocked}건`} tone="danger" />
      </section>

      {error && <p className="error-message">{error}</p>}

      <TransactionTable items={transactions} onRefresh={loadTransactions} loading={loading} />
    </main>
  );
}
