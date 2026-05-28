from fastapi import APIRouter
import json

CONFIG_PATH = "/home/nawaf511/empire-core-new/backend/app/config/layers_config.json"

router = APIRouter(prefix="/layers")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

########################################
# 📥 GET ALL
########################################
@router.get("/")
def get_layers():
    return load_config()

########################################
# 🔥 ENABLE / DISABLE
########################################
@router.post("/toggle")
def toggle_layer(name: str, enabled: bool):

    config = load_config()

    if name not in config:
        return {"error": "layer_not_found"}

    config[name]["enabled"] = enabled

    save_config(config)

    return {"status": "updated", "layer": name, "enabled": enabled}

########################################
# 🔀 CHANGE VARIANT (A/B)
########################################
@router.post("/variant")
def change_variant(name: str, variant: str):

    config = load_config()

    if name not in config:
        return {"error": "layer_not_found"}

    config[name]["variant"] = variant

    save_config(config)

    return {"status": "updated", "layer": name, "variant": variant}
