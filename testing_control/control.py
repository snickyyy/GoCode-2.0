import importlib
import pprint
import time
import unittest

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins, guarded_iter_unpack_sequence, full_write_guard



# source_code = """
# def main(nums, target):
#     entryDeg = {}
#     for index, num in enumerate(nums):
#         if num in entryDeg:
#             return entryDeg[num], index
#         delta = target - num
#         entryDeg[delta] = index
# """
#
# byte_code = compile_restricted(
#     source_code,
#     filename='<string>',
#     mode='exec'
# )
#
# exec_globals = {
#     '__builtins__': safe_builtins,
#     '_getattr_': getattr,
#     '_setattr_': setattr,
#
# }
# exec_locals = {}
# exec(byte_code, exec_globals, exec_locals)
#
# setattr(TestCase, "main", staticmethod(exec_locals.get("main")))
#
# suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
# result = unittest.TestResult()
# suite.run(result)
# print(result.errors)

class ControllerTest:
    __GLOBALS_VAR = {
        '__builtins__': safe_builtins,
        '_getattr_': getattr,  # разрешаем getattr
        '_setattr_': setattr,  # разрешаем setattr
        "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
        "_getiter_": iter,
        'enumerate': enumerate,  # Явно разрешаем enumerate
        'zip': zip,  # Явно разрешаем zip
        'range': range,  # Явно разрешаем range
        'len': len,  # Явно разрешаем len
        'sum': sum,  # Явно разрешаем sum
        'sorted': sorted,  # Явно разрешаем sorted
        'map': map,  # Явно разрешаем map
        'filter': filter,  # Явно разрешаем filter
        'iter': iter,  # Явно разрешаем iter
        'next': next,  # Явно разрешаем next
        'dict': dict,  # Разрешаем работу с словарями
        'set': set,  # Разрешаем работу с множествами
        'list': list,
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'None': None,
        'tuple': tuple,
        '_write_': full_write_guard,
        '_getitem_': lambda obj, key: obj[key]
    }

    __BODY_ANSWER = {
        "errors": [],
        "solution": "",
        "status": None,
        "test_passed": 0,
        "time": 0
    }

    def __init__(self):
        self.__locals = dict({})

    @property
    def get_globals(self):
        return self.__GLOBALS_VAR

    @property
    def get_sample_answer(self):
        return self.__BODY_ANSWER.copy()

    def _compile_code(self, code):
        try:
            byte_code = compile_restricted(
                code,
                filename='<string>',
                mode='exec'
            )
            return byte_code, True
        except Exception as e:
            response = self.get_sample_answer
            response.update({"errors": [str(e)], "status": False, "solution": code})
            return response, False

    def check_solution(self, source_code: str, test_name: str):
        test_case = importlib.import_module(f"tests.task.{test_name}").TestCase
        body, success = self._compile_code(source_code)
        if not success:
            return body
        exec(body, self.get_globals, self.__locals)
        setattr(test_case, "main", staticmethod(self.__locals.get("main")))
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        result = unittest.TestResult()
        suite.run(result)

        self.__locals.clear()

        response = self.get_sample_answer

        response.update({
            "test_passed": len(result.failures),
            "status": len(result.failures) == 0 and len(result.errors) == 0,
            "solution": source_code,
            "errors": result.errors
        })

        return response
