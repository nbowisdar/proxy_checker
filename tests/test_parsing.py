from loguru import logger


logger.add("logs.log")


@logger.catch(level="CRITICAL", message="An error caught in test()")
def test(x):
    50 / x


test(0)

print("next")
