import yaml

def load_config():
    with open("app/config/engine.yaml") as f:
        return yaml.safe_load(f)
