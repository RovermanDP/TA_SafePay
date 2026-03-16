import { Router } from "express";
import { transactionRouter } from "./transaction.routes.js";

export const router = Router();

router.use("/transactions", transactionRouter);
