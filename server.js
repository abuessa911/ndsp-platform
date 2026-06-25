import express from "express";

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.status(200).json({
    ok: true,
    project: "NDSP Platform",
    service: "Alpic MCP health bridge",
    status: "running"
  });
});

app.get("/health", (req, res) => {
  res.status(200).json({ ok: true, status: "healthy" });
});

app.post("/mcp", (req, res) => {
  res.status(200).json({
    jsonrpc: "2.0",
    id: req.body?.id ?? null,
    result: {
      protocolVersion: "2024-11-05",
      capabilities: {
        tools: {}
      },
      serverInfo: {
        name: "ndsp-platform",
        version: "1.0.0"
      }
    }
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`NDSP Alpic MCP server listening on ${PORT}`);
});
