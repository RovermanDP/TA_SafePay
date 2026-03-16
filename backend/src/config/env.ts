import dotenv from "dotenv";

dotenv.config();

export const env = {
  nodeEnv: process.env.NODE_ENV ?? "development",
  port: Number(process.env.PORT ?? 4000),
  dbUrl: process.env.DB_URL ?? "",
  mlServiceUrl: process.env.ML_SERVICE_URL ?? "",
  paymentApiUrl: process.env.PAYMENT_API_URL ?? ""
};
