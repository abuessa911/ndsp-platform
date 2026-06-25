import express from "express";

const app = express();
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    ok: true,
    name: "NDSP Platform",
    transport: "streamablehttp",
    status: "ready"
  });
});

app.get("/health", (req, res) => {
  res.json({ ok: true });
});

app.post("/mcp", (req, res) => {
  res.json({
    jsonrpc: "2.0",
    id: req.body?.id ?? null,
    result: {
      protocolVersion: "2024-11-05",
      capabilities: {},
      serverInfo: {
        name: "ndsp-platform",
        version: "1.0.0"
      }
    }
  });
});

const port = process.env.PORT || 3000;
app.listen(port, "0.0.0.0", () => {
  console.log(`NDSP MCP server running on port ${port}`);
});
