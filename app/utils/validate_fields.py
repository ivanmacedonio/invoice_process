def validate_fields(target_fields: dict, error_message: str):
    missing_fields = [field_name for field_name,
                      field_value in target_fields.items() if field_value is None]

    if missing_fields:
        raise ValueError(
            f'{error_message}: {missing_fields}')
