import pytest


# def test_1():
#     try:
#         a = 1/0
#     except Exception as e:
#         pytest.fail(e)

def test_2():
    try:
        a = 1/0
    except Exception as e:
        print("asasdasd", e)