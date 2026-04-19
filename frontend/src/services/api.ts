import { Transaction } from "../types/transaction";

export const sampleTransactions: Transaction[] = [
  { id: "TX-1001", userId: "user-01", amount: 250000, riskScore: 85, status: "blocked" },
  { id: "TX-1002", userId: "user-07", amount: 89000, riskScore: 58, status: "held" },
  { id: "TX-1003", userId: "user-03", amount: 15000, riskScore: 10, status: "approved" },
  { id: "TX-1004", userId: "user-12", amount: 430000, riskScore: 91, status: "blocked" },
  { id: "TX-1005", userId: "user-05", amount: 32000, riskScore: 22, status: "approved" },
  { id: "TX-1006", userId: "user-09", amount: 120000, riskScore: 63, status: "held" },
  { id: "TX-1007", userId: "user-02", amount: 7500, riskScore: 8, status: "approved" },
  { id: "TX-1008", userId: "user-15", amount: 310000, riskScore: 88, status: "blocked" },
  { id: "TX-1009", userId: "user-04", amount: 54000, riskScore: 15, status: "approved" },
  { id: "TX-1010", userId: "user-11", amount: 98000, riskScore: 52, status: "held" },
  { id: "TX-1011", userId: "user-06", amount: 175000, riskScore: 71, status: "held" },
  { id: "TX-1012", userId: "user-08", amount: 22000, riskScore: 5, status: "approved" },
];
