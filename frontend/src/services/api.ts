import { Transaction } from "../types/transaction";

const BASE_URL = "http://localhost:4000";

export async function fetchTransactions(): Promise<Transaction[]> {
  const res = await fetch(`${BASE_URL}/api/transactions`);
  if (!res.ok) throw new Error("거래 데이터를 불러오지 못했습니다.");
  return res.json();
}
