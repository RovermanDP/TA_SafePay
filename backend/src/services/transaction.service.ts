import { Transaction } from "../models/transaction.model.js";
import { fraudDetectionService } from "./fraud-detection.service.js";

type TransactionInput = Omit<Transaction, "id" | "riskScore" | "riskLevel" | "status">;

const transactions: Transaction[] = [];

const seedInputs: TransactionInput[] = [
  {
    userId: "user-01",
    amount: 250000,
    paymentMethod: "new-card",
    ipAddress: "203.0.113.10",
    location: "unknown",
    purchasedAt: "2026-05-03T09:12:00.000Z",
  },
  {
    userId: "user-02",
    amount: 15000,
    paymentMethod: "card",
    ipAddress: "203.0.113.22",
    location: "Seoul",
    purchasedAt: "2026-05-03T09:30:00.000Z",
  },
  {
    userId: "user-03",
    amount: 89000,
    paymentMethod: "new-card",
    ipAddress: "198.51.100.7",
    location: "Busan",
    purchasedAt: "2026-05-03T10:05:00.000Z",
  },
  {
    userId: "user-04",
    amount: 430000,
    paymentMethod: "new-card",
    ipAddress: "192.0.2.55",
    location: "unknown",
    purchasedAt: "2026-05-03T10:40:00.000Z",
  },
  {
    userId: "user-05",
    amount: 32000,
    paymentMethod: "card",
    ipAddress: "203.0.113.40",
    location: "Incheon",
    purchasedAt: "2026-05-03T11:02:00.000Z",
  },
  {
    userId: "user-06",
    amount: 175000,
    paymentMethod: "card",
    ipAddress: "198.51.100.18",
    location: "unknown",
    purchasedAt: "2026-05-03T11:30:00.000Z",
  },
  {
    userId: "user-07",
    amount: 7500,
    paymentMethod: "card",
    ipAddress: "203.0.113.91",
    location: "Daegu",
    purchasedAt: "2026-05-03T12:14:00.000Z",
  },
  {
    userId: "user-08",
    amount: 310000,
    paymentMethod: "new-card",
    ipAddress: "192.0.2.77",
    location: "unknown",
    purchasedAt: "2026-05-03T12:48:00.000Z",
  },
];

for (const input of seedInputs) {
  transactions.unshift(fraudDetectionService.classifyTransaction(input));
}

export const transactionService = {
  collectTransaction(input: TransactionInput) {
    const transaction = fraudDetectionService.classifyTransaction(input);
    transactions.unshift(transaction);
    return transaction;
  },

  listTransactions() {
    return transactions;
  }
};
