# NDSP API Standard

Standard response shape:

```json
{
  "ok": true,
  "service": "SERVICE-ID",
  "version": "1.0.0",
  "timestamp": "ISO-8601",
  "data": {}
}
```

Error response shape:

```json
{
  "ok": false,
  "service": "SERVICE-ID",
  "version": "1.0.0",
  "timestamp": "ISO-8601",
  "error": {
    "code": "NDSP-XXXX",
    "message": "..."
  }
}
```
