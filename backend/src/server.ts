import { app } from "./app.js";
import { env } from "./config/env.js";

app.listen(env.port, () => {
  console.log(`SafePay backend listening on port ${env.port}`);
});
