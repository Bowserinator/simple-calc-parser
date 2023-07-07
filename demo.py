from calc.parse import calc
from calc.format import format

while True:
    prompt = input("> ")
    try:
        print(format(calc(prompt), True))
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        print(e)
