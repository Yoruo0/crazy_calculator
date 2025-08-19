from typing import Dict, List, Union
from flask import request as FlaskRequest
from src.errors.http_unprocessable_entity import HttpUnprocessableEntityError
from src.drivers.interfaces.driver_handler_interface import DriverHandlerInterface

class Calculator4():
    def __init__(self, driver_handler: DriverHandlerInterface) -> None:
        self.__driver_handler = driver_handler

    def calculate(self, request: FlaskRequest) -> Dict: # type: ignore
        body = request.json
        numbers = self.__validate_body(body)
        average = self.__calculate_average(numbers)

        formated_response = self.__format_response(average)
        return formated_response


    def __validate_body(self, body: Dict) -> List[float]:
        if "numbers" not in body or not isinstance (body["numbers"], list):
            raise HttpUnprocessableEntityError("Missing 'numbers' key in request body")

        numbers = body["numbers"]
        for num in numbers:
            if not isinstance(num, (int, float)):
                raise HttpUnprocessableEntityError ("All elements of the list must be numbers")
            
        return numbers
    
    def __calculate_average(self, numbers: List[Union[int, float]]) -> float:
        if not numbers:
            raise HttpUnprocessableEntityError("A lista de números não pode estar vazia.")

        return self.__driver_handler.average(numbers)

    def __format_response(self, average: float) -> Dict:
        return{
            "data":{
                "Calculator": 4,
                "result" : round(average, 3)
            }
        }