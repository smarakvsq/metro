from datetime import datetime
from functools import wraps

from flask import jsonify, request

from app.models import CrimeUnvetted, CrimeVetted

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
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_obj


async def select_crime_table(vetted: bool):
    return CrimeVetted if vetted else CrimeUnvetted


async def format_line_data(data: dict) -> dict:
    formatted_data = {}
    category_names = set()
    for month, category, count in data:
        category_names.add(category)
        month = month.strftime("%Y-%-m-%-d")
        if month not in formatted_data:
            formatted_data[month] = {}
        formatted_data[month][category] = count
    line_data = []
    for date_ in formatted_data:
        dct = {"name": date_}
        for category in category_names:
            dct.update({category: formatted_data[date_].get(category, 0)})
        line_data.append(dct)
    return line_data
