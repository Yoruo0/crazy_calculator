from typing import Dict, List
from pytest import raises
from .calculator_4 import Calculator4
from src.drivers.numpy_handler import NumpyHandler
from src.errors.http_unprocessable_entity import HttpUnprocessableEntityError

class MockRequest:
    def __init__(self, body: Dict) -> None:
        self.json = body

class MockDriverHandler:
    def average(self, numbers: List[float]) -> float:
        return 3

def test_calculate_integration():
    mock_request = MockRequest(body={"numbers": [2, 4, 10, 5]})

    driver = NumpyHandler() # type: ignore
    calculator_4 = Calculator4(driver) # type: ignore
    formated_response = calculator_4.calculate(mock_request)

    assert isinstance(formated_response, dict)
    assert formated_response == {'data': {'Calculator': 4, 'result': 5.25}}

def test_calculate():
    mock_request = MockRequest(body={"numbers": [2, 4, 10, 5]})

    driver = MockDriverHandler()
    calculator_4 = Calculator4(driver) # type: ignore
    formated_response = calculator_4.calculate(mock_request)

    assert isinstance(formated_response, dict)
    assert formated_response == {'data': {'Calculator': 4, 'result': 3.0}}

def test_calculate_with_invalid_body():
    mock_request = MockRequest(body={"numbers": [2, "A"]})
    driver = NumpyHandler()
    calculator_4 = Calculator4(driver)

    with raises(HttpUnprocessableEntityError):
        calculator_4.calculate(mock_request)