import { RiskLevel, Transaction } from "../models/transaction.model.js";
import { riskService } from "./risk.service.js";

function resolveRiskLevel(score: number): RiskLevel {
  if (score >= 80) {
    return "danger";
  }

  if (score >= 50) {
    return "suspicious";
  }

  return "normal";
}

export const fraudDetectionService = {
  classifyTransaction(
    payload: Omit<Transaction, "id" | "riskScore" | "riskLevel" | "status">
  ): Transaction {
    const riskScore = riskService.calculateRiskScore(payload);
    const riskLevel = resolveRiskLevel(riskScore);

    return {
      ...payload,
      id: crypto.randomUUID(),
      riskScore,
      riskLevel,
      status: riskLevel === "danger" ? "blocked" : riskLevel === "suspicious" ? "held" : "approved"
    };
  }
};
