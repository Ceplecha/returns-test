from returns.result import Failure, Success


def test_result_error_success():
    """Ensures that ResultE can be typecasted to success."""
    container = Success(1)
    assert container.unwrap() == 1


def test_result_error_failure():
    """Ensures that ResultE can be typecasted to failure."""
    container = Failure(ValueError('1'))
    assert str(container.failure()) == '1'
