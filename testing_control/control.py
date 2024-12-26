import unittest

def tt():
    return 0/0

class MyTest(unittest.TestCase):
    def test_example(self):
        self.assertEqual(tt(), 3)

    def test_example2(self):
        self.assertEqual(tt(), 3)

# Создаем тестовый сьют и тест-раннер
suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
result = unittest.TestResult()

# Запускаем тесты и сохраняем результат в переменную
