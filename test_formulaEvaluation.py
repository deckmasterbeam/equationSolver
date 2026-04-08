import unittest

from formulaEvaluation import Formula, BooleanFormula, NumericFormula, VariableFormula, BooleanOperatorFormula, RelationalOperatorFormula, PlainTextFormula, ArithmeticFormula


class TestFormulaEvaluation(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_base_boolean_formula(self):
        formula = Formula(formula=BooleanFormula(True))
        self.assertTrue(formula.evaluate_formula())

    def test_base_numeric_formula(self):
        formula = Formula(formula=NumericFormula(42))
        self.assertEqual(formula.evaluate_formula(), 42)

    def test_boolean_operator_and_formula(self):
        formula = Formula(formula=BooleanOperatorFormula(
            operator='AND',
            left=BooleanFormula(True),
            right=BooleanFormula(False)
        ))
        self.assertFalse(formula.evaluate_formula())

    def test_boolean_operator_or_formula(self):
        formula = Formula(formula=BooleanOperatorFormula(
            operator='OR',
            left=BooleanFormula(True),
            right=BooleanFormula(False)
        ))
        self.assertTrue(formula.evaluate_formula())

    def test_relational_operator_greater_than_formula(self):
        formula = Formula(formula=RelationalOperatorFormula(
            operator='>',
            left=NumericFormula(10),
            right=NumericFormula(5)
        ))
        self.assertTrue(formula.evaluate_formula())

    def test_relational_operator_less_than_formula(self):
        formula = Formula(formula=RelationalOperatorFormula(
            operator='<',
            left=NumericFormula(5),
            right=NumericFormula(10)
        ))
        self.assertTrue(formula.evaluate_formula())

    def test_relational_operator_equal_formula(self):
        formula = Formula(formula=RelationalOperatorFormula(
            operator='==',
            left=NumericFormula(5),
            right=NumericFormula(5)
        ))
        self.assertTrue(formula.evaluate_formula())

    def test_relational_layered_formula(self):
        formula = Formula(formula=BooleanOperatorFormula(
            operator='AND',
            left=RelationalOperatorFormula(
                operator='>',
                left=NumericFormula(10),
                right=NumericFormula(5)
            ),
            right=RelationalOperatorFormula(
                operator='<',
                left=NumericFormula(5),
                right=NumericFormula(10)
            )
        ))
        self.assertTrue(formula.evaluate_formula())

    def test_variables_in_formula(self):
        variables: dict[str, bool | int | float] = {
            'x': 10,
            'y': 5
        }
        formula = Formula(formula=RelationalOperatorFormula(
            operator='>',
            left=VariableFormula('x'),
            right=VariableFormula('y')
        ))
        self.assertTrue(formula.evaluate_formula(variables))

    def test_plain_text_formula(self):
        formula = Formula(formula=PlainTextFormula("x > y AND z < 10"))
        variables: dict[str, bool | int | float] = {
            'x': 10,
            'y': 5,
            'z': 3
        }
        self.assertTrue(formula.evaluate_formula(variables))

    def test_arithmetic_formula(self):
        formula = Formula(formula=ArithmeticFormula(
            operator='+',
            left=NumericFormula(10),
            right=NumericFormula(5)
        ))
        self.assertEqual(formula.evaluate_formula(), 15)

    def test_arithmetic_formula_with_variables(self):
        variables: dict[str, bool | int | float] = {
            'x': 10,
            'y': 5
        }
        formula = Formula(formula=ArithmeticFormula(
            operator='*',
            left=VariableFormula('x'),
            right=VariableFormula('y')
        ))
        self.assertEqual(formula.evaluate_formula(variables), 50)

    def test_arithmetic_formula_with_nested_operations(self):
        variables: dict[str, bool | int | float] = {
            'x': 10,
            'y': 5,
            'z': 2
        }
        formula = Formula(formula=ArithmeticFormula(
            operator='-',
            left=ArithmeticFormula(
                operator='+',
                left=VariableFormula('x'),
                right=VariableFormula('y')
            ),
            right=VariableFormula('z')
        ))
        self.assertEqual(formula.evaluate_formula(variables), 13)

    def test_relational_formula_with_nested_arithmetic(self):
        variables: dict[str, bool | int | float] = {
            'x': 6,
            'y': 5,
            'z': 10
        }
        formula = Formula(formula=RelationalOperatorFormula(
            operator='>',
            left=ArithmeticFormula(
                operator='+',
                left=VariableFormula('x'),
                right=VariableFormula('y')
            ),
            right=VariableFormula('z')
        ))
        self.assertTrue(formula.evaluate_formula(variables))

if __name__ == "__main__":
    unittest.main()
