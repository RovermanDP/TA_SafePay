import { Transaction } from "../models/transaction.model.js";
import { fraudDetectionService } from "./fraud-detection.service.js";

type TransactionInput = Omit<Transaction, "id" | "riskScore" | "riskLevel" | "status">;

const transactions: Transaction[] = [];

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
