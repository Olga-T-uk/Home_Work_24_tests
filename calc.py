
import pytest

from app.calc import Calculator

class TestCalc:
    def setup_method(self):
        self.calc = Calculator

    def test_adding_success(self):
        assert self.calc.adding(self, 1, 1) == 2

    def test_adding_unsuccess(self):
        assert self.calc.adding(self, 1, 1) == 3

    def test_multiply_calculate_correctly(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_multiply_failed(self):
        assert self.calc.multiply(self, 2, 2) == 5

    def test_division_correctly(self):
        assert self.calc.division(self, 8, 2) == 4

    def test_division_failed(self):
        assert self.calc.division(self, 5, 2) == 2

    def test_subtraction_correctly(self):
        assert self.calc.subtraction(self, 6, 2) == 4

    def test_subtraction_failed(self):
        assert self.calc.subtraction(self, 4, 2) == 3

    def test_zero_division(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.division(self, 1, 0)

    def teardown(self):
        print('Выполнение метода Teardown')
