import unittest


class TestCase(unittest.TestCase):
    def test_example_1(self):
        result = self.main(nums=[2, 7, 11, 15], target=9)
        self.assertEqual(result, (0, 1))

    def test_example_2(self):
        result = self.main(nums=[3, 2, 4], target=6)
        self.assertEqual(result, (1, 2))

    def test_example_3(self):
        result = self.main(nums=[3, 3], target=6)
        self.assertEqual(result, (0, 1))

    def test_no_solution(self):
        result = self.main(nums=[1, 2, 3], target=7)
        self.assertIsNone(result)

    def test_empty_list(self):
        result = self.main([], 5)
        self.assertIsNone(result)
