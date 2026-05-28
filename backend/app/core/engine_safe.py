from app.contracts.validator import validate_engine

def safe_run(name, func, *args, **kwargs):

    try:
        result = func(*args, **kwargs)

        validate_engine(name, result)

        return result

    except Exception as e:
        return {
            "error": str(e),
            "engine": name,
            "fallback": True
        }
