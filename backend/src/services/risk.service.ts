import { Transaction } from "../models/transaction.model.js";

type TransactionPayload = Omit<Transaction, "id" | "riskScore" | "riskLevel" | "status">;

export const riskService = {
  calculateRiskScore(transaction: TransactionPayload) {
    let score = 10;

    if (transaction.amount > 100000) {
      score += 35;
    }

    if (transaction.paymentMethod === "new-card") {
      score += 20;
    }

    if (transaction.location === "unknown") {
      score += 20;
    }

    return Math.min(score, 100);
  }
};
