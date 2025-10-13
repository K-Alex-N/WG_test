import random

from config import MAX_PARAM_VALUE, MIN_PARAM_VALUE


def get_rand_param_value() -> int:
    """Как сказано в задании, все параметры заполняются случайным числом от 1 до 20."""
    return random.randint(MIN_PARAM_VALUE, MAX_PARAM_VALUE)
