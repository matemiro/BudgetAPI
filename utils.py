def pop_null_values_from_dict(data: dict) -> dict:
    return {key: value for key, value in data.items() if value}
