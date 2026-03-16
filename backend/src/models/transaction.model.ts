export type RiskLevel = "normal" | "suspicious" | "danger";

export interface Transaction {
  id: string;
  userId: string;
  amount: number;
  paymentMethod: string;
  ipAddress: string;
  location: string;
  purchasedAt: string;
  riskScore: number;
  riskLevel: RiskLevel;
  status: "approved" | "held" | "blocked";
}
