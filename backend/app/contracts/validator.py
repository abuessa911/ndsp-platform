from app.contracts.contracts import ENGINE_CONTRACTS

class ContractError(Exception):
    pass

def validate_engine(name, data):

    required = ENGINE_CONTRACTS.get(name, [])

    if not isinstance(data, dict):
        raise ContractError(f"{name} must return dict")

    for key in required:
        if key not in data:
            raise ContractError(f"{name} missing: {key}")

    return True

def validate_full(payload):

    errors = []

    for engine, keys in ENGINE_CONTRACTS.items():
        if engine not in payload:
            errors.append(f"{engine} missing entirely")
            continue

        try:
            validate_engine(engine, payload[engine])
        except Exception as e:
            errors.append(str(e))

    return errors
