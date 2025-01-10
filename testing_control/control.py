import importlib
import re
import unittest

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins, guarded_iter_unpack_sequence, full_write_guard
sample = "\ndef main(nums, target):\n    entryDeg = {}\n    for index, num in enumerate(nums):\n        if num in entryDeg:\n            return entryDeg[num], index\n        delta = target - num\n        entryDeg[delta] = index\n        "

class ControllerTest:
    __GLOBALS_VAR = {
        '__builtins__': safe_builtins,
        '_getattr_': getattr,
        '_setattr_': setattr,
        "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
        "_getiter_": iter,
        'enumerate': enumerate,
        'zip': zip,
        'range': range,
        'len': len,
        'sum': sum,
        'sorted': sorted,
        'map': map,
        'filter': filter,
        'iter': iter,
        'next': next,
        'dict': dict,
        'set': set,
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

    def check_solution(self, source_code: str, test_name: str):
        test_case = importlib.import_module(f"tests.task.{test_name}").TestCase
        try:
            byte_code = compile_restricted(
                source_code,
                filename='<string>',
                mode='exec')
            exec(byte_code, self.get_globals, self.__locals)
        except Exception as e:
            response = self.get_sample_answer
            response.update({"errors": [str(e)], "status": False, "solution": source_code})
            return response
        setattr(test_case, "main", staticmethod(self.__locals.get("main")))
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        result = unittest.TestResult()
        suite.run(result)

        self.__locals.clear()

        response = self.get_sample_answer
        response.update({
            "test_passed": result.testsRun - len(result.failures),
            "count_tests": result.testsRun,
            "status": len(result.failures) == 0 and len(result.errors) == 0,
            "solution": source_code,
        })
        if not result.errors:
            response["errors"] = result.failures[0][-1] if len(result.failures) < 2 else result.failures[-1][-1]
            return response

        error = result.errors[-1][-1] if len(result.errors) > 1 else result.errors[-1]
        match = re.search(r"^\w+Error: .+$", error, re.MULTILINE)

        if match:
            response["errors"] = [match.group(0)]
        else: response["errors"] = result.errors

        return response
