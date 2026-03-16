import { Transaction } from "../types/transaction";

export const sampleTransactions: Transaction[] = [
  {
    id: "TX-1001",
    userId: "user-01",
    amount: 250000,
    riskScore: 82,
    status: "blocked"
  },
  {
    id: "TX-1002",
    userId: "user-07",
    amount: 89000,
    riskScore: 58,
    status: "held"
  }
];
