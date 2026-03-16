export interface Transaction {
  id: string;
  userId: string;
  amount: number;
  riskScore: number;
  status: "approved" | "held" | "blocked";
}
