def to_dict(keys=[], items=[]):
    return {item[0]: {keys[i]: item_value for i, item_value in enumerate(item)} for item in items}



