import { Transaction } from "../types/transaction";

type TransactionTableProps = {
  items: Transaction[];
  onRefresh?: () => void;
  loading?: boolean;
};

const riskLevelLabel: Record<string, string> = {
  normal: "정상",
  suspicious: "의심",
  danger: "위험",
};

export function TransactionTable({ items, onRefresh, loading }: TransactionTableProps) {
  return (
    <section className="table-card">
      <div className="table-header">
        <h2>의심 거래 목록</h2>
        {onRefresh && (
          <button
            type="button"
            className="refresh-button"
            onClick={onRefresh}
            disabled={loading}
          >
            {loading ? "불러오는 중..." : "새로고침"}
          </button>
        )}
      </div>
      <table>
        <thead>
          <tr>
            <th>거래 ID</th>
            <th>사용자</th>
            <th>금액</th>
            <th>결제 수단</th>
            <th>위험 점수</th>
            <th>위험 등급</th>
            <th>상태</th>
            <th>구매 시각</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr>
              <td colSpan={8} style={{ textAlign: "center", color: "#888" }}>
                거래 데이터가 없습니다.
              </td>
            </tr>
          ) : (
            items.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.userId}</td>
                <td>{item.amount.toLocaleString()}원</td>
                <td>{item.paymentMethod}</td>
                <td>{item.riskScore}</td>
                <td>
                  <span className={`badge risk-${item.riskLevel}`}>
                    {riskLevelLabel[item.riskLevel] ?? item.riskLevel}
                  </span>
                </td>
                <td>{item.status}</td>
                <td>{new Date(item.purchasedAt).toLocaleString("ko-KR")}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}
