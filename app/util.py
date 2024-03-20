from datetime import datetime
from functools import wraps
from flask import request
from functools import wraps


mapper = {"true": True, "True": True, "false": False, "False": False}


def validate_and_get_args(*args):
    """
    Decorator to validate and extract arguments from a Flask request,
    supporting async endpoints.

    Args:
        *args: A list of argument names to extract and validate, or "all" to return all request.args.

    Returns:
        A decorator function.

    Raises:
        ValueError: If a required argument is missing or invalid.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*f_args, **f_kwargs):
            if "all" in args:
                validated_args = request.args.to_dict()  # Get all request.args
            else:
                validated_args = {}
                for arg in args:
                    if request.method == "GET":
                        value = request.args.get(arg)
                    else:
                        raise ValueError(f"Unsupported request method: {request.method}")

                    if value is None and arg != "all":  # Don't raise error for missing "all"
                        raise ValueError(f"Missing required argument: {arg}")

                    # Add custom validation logic here (e.g., type checking)
                    # validated_args[arg] = validate_value(value)  # Replace with your validation function
                    if value.lower() in mapper.keys():
                        value = mapper[value]
                    validated_args[arg] = value

            # Call the decorated function asynchronously
            return await func(*f_args, validated_args, **f_kwargs)

        return wrapper

    return decorator


async def parse_date(date_string):
    date_obj = None
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m")
    except Exception as exc:
        print(exc)
        raise ValueError(str(exc))

    return date_obj
