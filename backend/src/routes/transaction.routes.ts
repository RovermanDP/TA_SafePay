import { Router } from "express";
import { transactionController } from "../controllers/transaction.controller.js";

export const transactionRouter = Router();

transactionRouter.post("/", transactionController.collect);
transactionRouter.get("/", transactionController.list);
