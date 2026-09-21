from returns.result import Failure, Success, safe


@safe
def div(first_number, second_number):
    return first_number // second_number


match div(1, 0):
    case Success(10):
        print('Result is "10"')
    case Success(value):
        print(f'Result is "{value}"')
    case Failure(ZeroDivisionError()):
        print('"ZeroDivisionError" was raised')
    case Failure(_):
        print('The division was a failure')
