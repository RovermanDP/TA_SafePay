import { Transaction } from "../types/transaction";

export type RiskFilter = "all" | "normal" | "suspicious" | "danger";
export type SortBy = "recent" | "risk";

type TransactionTableProps = {
  items: Transaction[];
  totalCount?: number;
  onRefresh?: () => void;
  loading?: boolean;
  riskFilter?: RiskFilter;
  onRiskFilterChange?: (value: RiskFilter) => void;
  sortBy?: SortBy;
  onSortByChange?: (value: SortBy) => void;
};

const riskLevelLabel: Record<string, string> = {
  normal: "정상",
  suspicious: "의심",
  danger: "위험",
};

const statusLabel: Record<string, string> = {
  approved: "승인",
  held: "보류",
  blocked: "차단",
};

export function TransactionTable({
  items,
  totalCount,
  onRefresh,
  loading,
  riskFilter,
  onRiskFilterChange,
  sortBy,
  onSortByChange,
}: TransactionTableProps) {
  const isFiltered = riskFilter && riskFilter !== "all";
  const total = totalCount ?? items.length;

  return (
    <section className="table-card">
      <div className="table-header">
        <div className="table-title">
          <h2>의심 거래 목록</h2>
          <span className="table-count">
            {isFiltered ? `전체 ${total}건 중 ${items.length}건` : `총 ${total}건`}
          </span>
        </div>
        <div className="table-actions">
          {onRiskFilterChange && (
            <select
              className="filter-select"
              value={riskFilter ?? "all"}
              onChange={(e) => onRiskFilterChange(e.target.value as RiskFilter)}
            >
              <option value="all">전체 등급</option>
              <option value="normal">정상</option>
              <option value="suspicious">의심</option>
              <option value="danger">위험</option>
            </select>
          )}
          {onSortByChange && (
            <select
              className="filter-select"
              value={sortBy ?? "recent"}
              onChange={(e) => onSortByChange(e.target.value as SortBy)}
            >
              <option value="recent">최신순</option>
              <option value="risk">위험 점수 높은순</option>
            </select>
          )}
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
                {isFiltered
                  ? "해당 등급의 거래가 없습니다."
                  : "거래 데이터가 없습니다."}
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
                <td>
                  <span className={`badge status-${item.status}`}>
                    {statusLabel[item.status] ?? item.status}
                  </span>
                </td>
                <td>{new Date(item.purchasedAt).toLocaleString("ko-KR")}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}
