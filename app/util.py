from datetime import datetime
from flask import request, jsonify
from functools import wraps
from app.models import CrimeVetted, CrimeUnvetted


mapper = {"true": True, "True": True, "false": False, "False": False}


def validate_and_get_args(**kwargs):
    """
    Decorator to validate and extract arguments from a Flask request,
    supporting async endpoints and marking arguments as optional.

    Args:
        **kwargs: A dictionary where keys are argument names and values are booleans indicating if the argument is required (True) or optional (False).

    Returns:
        A decorator function.

    Raises:
        KeyError: If a required argument is missing.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*f_args, **f_kwargs):
            missing_args = []
            validated_args = {}
            for arg, is_required in kwargs.items():
                if request.method == "GET":
                    value = request.args.get(arg)
                else:
                    raise ValueError(f"Unsupported request method: {request.method}")

                if value is None and is_required:
                    missing_args.append(arg)
                else:
                    # Add custom validation logic here (e.g., type checking)
                    if value and value.lower() in mapper.keys():
                        value = mapper[value]
                    validated_args[arg] = value

            if missing_args:
                return (
                    jsonify(
                        {
                            "error": "Missing required arguments",
                            "missing_args": missing_args,
                        }
                    ),
                    400,
                )

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


async def select_crime_table(vetted: bool):
    return CrimeVetted if vetted else CrimeUnvetted


