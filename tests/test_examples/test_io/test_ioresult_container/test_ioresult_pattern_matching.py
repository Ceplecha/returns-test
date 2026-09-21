from returns.io import IOFailure, IOSuccess
from returns.result import Success

container = IOSuccess(42)
match container:
    case IOSuccess(Success(42)):
        print('Result is "42"')
    case IOSuccess(value):
        print(f'Result is "{value}"')
    case IOFailure(_):
        print('A failure was occurred')
