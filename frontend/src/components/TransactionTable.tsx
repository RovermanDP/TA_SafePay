import { Transaction } from "../types/transaction";

type TransactionTableProps = {
  items: Transaction[];
};

export function TransactionTable({ items }: TransactionTableProps) {
  return (
    <section className="table-card">
      <div className="table-header">
        <h2>의심 거래 목록</h2>
      </div>
      <table>
        <thead>
          <tr>
            <th>거래 ID</th>
            <th>사용자</th>
            <th>금액</th>
            <th>위험 점수</th>
            <th>상태</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.userId}</td>
              <td>{item.amount.toLocaleString()}원</td>
              <td>{item.riskScore}</td>
              <td>{item.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
