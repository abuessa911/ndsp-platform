from __future__ import annotations
import json
from pathlib import Path

class SourceRegistry:
    def __init__(self, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.sources = {x["source_id"]: x for x in data.get("sources") or []}
        if len(self.sources) != len(data.get("sources") or []):
            raise ValueError("duplicate source_id")

    def get(self, source_id):
        source = self.sources.get(source_id)
        if not source:
            return {"ok":False,"status":"UNKNOWN_SOURCE","decision_use_allowed":False}
        return {"ok":True,"status":"RESOLVED",**source}
