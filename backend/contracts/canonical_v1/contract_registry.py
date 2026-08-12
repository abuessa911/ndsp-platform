from __future__ import annotations
import json
from pathlib import Path

class ContractRegistry:
    def __init__(self, path):
        data=json.loads(Path(path).read_text(encoding="utf-8"))
        contracts=data.get("contracts") or []
        self.contracts={x["contract_id"]:x for x in contracts}
        if len(self.contracts)!=len(contracts):
            raise ValueError("duplicate contract_id")

    def require(self, contract_id, version=None):
        item=self.contracts.get(contract_id)
        if not item:
            return {"ok":False,"status":"CONTRACT_NOT_REGISTERED"}
        if version and item.get("version")!=version:
            return {"ok":False,"status":"CONTRACT_VERSION_MISMATCH","registered":item.get("version")}
        return {"ok":True,"status":"CONTRACT_ACCEPTED","contract":item}
