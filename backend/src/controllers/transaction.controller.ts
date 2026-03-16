import { Request, Response } from "express";
import { transactionService } from "../services/transaction.service.js";

export const transactionController = {
  collect(req: Request, res: Response) {
    const transaction = transactionService.collectTransaction(req.body);
    res.status(201).json(transaction);
  },

  list(_req: Request, res: Response) {
    res.json(transactionService.listTransactions());
  }
};
