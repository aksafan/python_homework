import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))


def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        logger.info(f"function: {func.__name__}")
        logger.info(f"positional parameters: {args}")
        logger.info(f"keyword parameters: {kwargs}")
        logger.info(f"return: {result}")

        return result

    return wrapper


@logger_decorator
def test_func():
    print("Hello, World!")

@logger_decorator
def test_func2(*number):
    return True

@logger_decorator
def test_func3(**k_number):
    return logger_decorator

test_func()
test_func2("test", 1)
test_func3(key="test", key2=2)
