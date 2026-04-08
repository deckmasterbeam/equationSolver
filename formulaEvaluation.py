
import argparse
import re
from typing import Literal, Union, cast

# Type aliases for formula types
FormulaType = Union['Formula.BaseFormula', 'Formula.BooleanFormula', 'Formula.NumericFormula', 'Formula.VariableFormula', 'Formula.BooleanOperatorFormula', 'Formula.RelationalOperatorFormula', 'Formula.ArithmeticFormula', 'Formula.PlainTextFormula']
SubFormulaType = Union['Formula.BooleanFormula', 'Formula.NumericFormula', 'Formula.VariableFormula', 'Formula.BooleanOperatorFormula', 'Formula.RelationalOperatorFormula', 'Formula.ArithmeticFormula', 'Formula.ArithmeticFormula']
EvalFormulaType = Union[SubFormulaType, 'Formula.PlainTextFormula', None]
variablesType = dict[str, Union[bool, int, float]]

booleanOperators = Literal['OR', 'AND']
arithmeticOperatorsType = Literal['+', '-', '*', '/']
arithmeticOperators = ('+', '-', '*', '/')
relationalOperators = Literal['==', '!=', '<', '<=', '>', '>=']

class Formula:
  def __init__(self, formula: FormulaType) -> None:
    self.formula = formula

  class BaseFormula:
    type: Literal['BaseFormula']
    value: Union[bool, int, float]

    def __init__(self, value: Union[bool, int, float]) -> None:
      self.type = 'BaseFormula'
      self.value = value
    
  class BooleanFormula:
    type: Literal['BooleanFormula']
    value: bool

    def __init__(self, value: bool) -> None:
      self.type = 'BooleanFormula'
      self.value = value

    def evaluate_as_boolean(self, variables: variablesType) -> bool:
      return self.value
    
    def evaluate_as_numeric(self, variables: variablesType) -> Union[int, float]:
      return 1 if self.value else 0

  class NumericFormula:
    type: Literal['NumericFormula']
    value: Union[int, float]

    def __init__(self, value: Union[int, float]) -> None:
      self.type = 'NumericFormula'
      self.value = value

    def evaluate_as_boolean(self, variables: variablesType) -> bool:
      return self.value != 0
    
    def evaluate_as_numeric(self, variables: variablesType) -> Union[int, float]:
      return self.value
  
  class ArithmeticFormula:
    type: Literal['ArithmeticFormula']
    operator: arithmeticOperatorsType
    left: SubFormulaType
    right: SubFormulaType

    def __init__(self, operator: arithmeticOperatorsType, left: SubFormulaType, right: SubFormulaType) -> None:
      self.type = 'ArithmeticFormula'
      self.operator = operator
      self.left = left
      self.right = right

    def evaluate_as_numeric(self, variables: variablesType) -> Union[int, float]:
      left_value = self._resolve_numeric(self.left, variables)
      right_value = self._resolve_numeric(self.right, variables)
      if self.operator == '+':
        return left_value + right_value
      elif self.operator == '-':
        return left_value - right_value
      elif self.operator == '*':
        return left_value * right_value
      elif self.operator == '/':
        if right_value == 0:
          raise ZeroDivisionError('Division by zero in arithmetic formula')
        return left_value / right_value
      raise ValueError(f'Unsupported arithmetic operator: {self.operator}')

    def evaluate_as_boolean(self, variables: variablesType) -> bool:
      return self.evaluate_as_numeric(variables) != 0

    def _resolve_numeric(self, operand: SubFormulaType, variables: variablesType) -> Union[int, float]:
      if operand.type == 'NumericFormula':
        return operand.evaluate_as_numeric(variables)
      elif operand.type == 'VariableFormula':
        return operand.evaluate_as_numeric(variables)
      elif operand.type == 'ArithmeticFormula':
        return operand.evaluate_as_numeric(variables)
      else:
        raise ValueError(f'Unsupported arithmetic operand type: {operand.type}')
  
  class VariableFormula:
    type: Literal['VariableFormula']
    name: str

    def __init__(self, name: str) -> None:
      self.type = 'VariableFormula'
      self.name = name

    def evaluate_as_boolean(self, variables: dict[str, Union[bool, int, float]]) -> bool:
      if self.name not in variables:
        raise ValueError(f"Variable '{self.name}' not found in variables dictionary")
      if isinstance(variables[self.name], bool):
        return bool(variables[self.name])
      elif isinstance(variables[self.name], (int, float)):
        return variables[self.name] != 0
      else:
        raise ValueError(f"Unsupported variable type for '{self.name}': {type(variables[self.name])}")
    
    def evaluate_as_numeric(self, variables: dict[str, Union[bool, int, float]]) -> Union[int, float]:
      if self.name not in variables:
        raise ValueError(f"Variable '{self.name}' not found in variables dictionary")
      if isinstance(variables[self.name], bool):
        return 1 if variables[self.name] else 0
      elif isinstance(variables[self.name], (int, float)):
        return variables[self.name]
      else:
        raise ValueError(f"Unsupported variable type for '{self.name}': {type(variables[self.name])}")

  class BooleanOperatorFormula:
    type: Literal['BooleanOperatorFormula']
    operator: booleanOperators
    left: SubFormulaType
    right: SubFormulaType

    def __init__(self, operator: booleanOperators, left: SubFormulaType, right: SubFormulaType) -> None:
      self.type = 'BooleanOperatorFormula'
      self.operator = operator
      self.left = left
      self.right = right

    def _evaluate_sub_formula(self, sub_formula: SubFormulaType, variables: dict[str, Union[bool, int, float]]) -> bool:
      if sub_formula.type == 'BooleanFormula':
        return sub_formula.evaluate_as_boolean(variables)
      elif sub_formula.type == 'NumericFormula':
        return sub_formula.evaluate_as_boolean(variables)
      elif sub_formula.type == 'VariableFormula':
        return sub_formula.evaluate_as_boolean(variables)
      elif sub_formula.type == 'ArithmeticFormula':
        return sub_formula.evaluate_as_boolean(variables)
      elif sub_formula.type == 'BooleanOperatorFormula':
        return sub_formula.evaluate_as_boolean(variables)
      elif sub_formula.type == 'RelationalOperatorFormula':
        return sub_formula.evaluate_as_boolean(variables)
      else:
        raise ValueError(f"Cannot evaluate sub-formula of type {sub_formula.type}")

    def evaluate_as_boolean(self, variables: dict[str, Union[bool, int, float]]) -> bool:
      left_value = self._evaluate_sub_formula(self.left, variables)
      right_value = self._evaluate_sub_formula(self.right, variables)
      
      if self.operator == 'OR':
        return left_value or right_value
      elif self.operator == 'AND':
        return left_value and right_value
      else:
        raise ValueError(f"Unsupported operator: {self.operator}")

  class RelationalOperatorFormula:
    type: Literal['RelationalOperatorFormula']
    operator: relationalOperators
    left: SubFormulaType
    right: SubFormulaType

    def __init__(self, operator: relationalOperators, left: SubFormulaType, right: SubFormulaType) -> None:
      self.type = 'RelationalOperatorFormula'
      self.operator = operator
      self.left = left
      self.right = right

    def _evaluate_sub_formula(self, sub_formula: SubFormulaType, variables: dict[str, Union[bool, int, float]]) -> Union[bool, int, float]:
      if sub_formula.type == 'BooleanFormula':
        return sub_formula.evaluate_as_boolean(variables)
      elif sub_formula.type == 'NumericFormula':
        return sub_formula.evaluate_as_numeric(variables)
      elif sub_formula.type == 'VariableFormula':
        return sub_formula.evaluate_as_numeric(variables)
      elif sub_formula.type == 'ArithmeticFormula':
        return sub_formula.evaluate_as_numeric(variables)
      elif sub_formula.type == 'BooleanOperatorFormula':
        return sub_formula.evaluate_as_boolean(variables)
      elif sub_formula.type == 'RelationalOperatorFormula':
        return sub_formula.evaluate_as_boolean(variables)
      else:
        raise ValueError(f"Cannot evaluate sub-formula of type {sub_formula.type}")

    def evaluate_as_boolean(self, variables: dict[str, Union[bool, int, float]]) -> bool:
      left_value = self._evaluate_sub_formula(self.left, variables)
      right_value = self._evaluate_sub_formula(self.right, variables)
      
      if self.operator == '==':
        return left_value == right_value
      elif self.operator == '!=':
        return left_value != right_value
      elif self.operator == '<':
        return left_value < right_value
      elif self.operator == '<=':
        return left_value <= right_value
      elif self.operator == '>':
        return left_value > right_value
      elif self.operator == '>=':
        return left_value >= right_value
      else:
        raise ValueError(f"Unsupported operator: {self.operator}")

  class PlainTextFormula:
    type: Literal['PlainTextFormula']
    text: str

    def __init__(self, text: str) -> None:
      self.type = 'PlainTextFormula'
      self.text = text

    def to_formula(self) -> FormulaType:
      tokens = self._tokenize(self.text)
      return self._parse_relational_or(tokens)

    def _tokenize(self, text: str) -> list[str]:
      tokens = re.findall(r'==|!=|<=|>=|\+|\-|\*|\/|<|>|\bAND\b|\bOR\b|\bTRUE\b|\bFALSE\b|\d+\.\d+|\d+|[A-Za-z_]\w*', text, flags=re.IGNORECASE)
      return [token.upper() if token.upper() in ('AND', 'OR', 'TRUE', 'FALSE') else token for token in tokens]

    def _parse_relational_or(self, tokens: list[str]) -> SubFormulaType:
      parts: list[list[str]] = []
      current: list[str] = []

      for token in tokens:
        if token == 'OR':
          if not current:
            raise ValueError('Empty OR term in plain text formula')
          parts.append(current)
          current = []
        else:
          current.append(token)

      if not current:
        raise ValueError('Empty OR term in plain text formula')
      parts.append(current)

      formula = self._parse_relational_and(parts[0])
      for part in parts[1:]:
        formula = Formula.BooleanOperatorFormula('OR', formula, self._parse_relational_and(part))
      return formula

    def _parse_relational_and(self, tokens: list[str]) -> SubFormulaType:
      parts: list[list[str]] = []
      current: list[str] = []

      for token in tokens:
        if token == 'AND':
          if not current:
            raise ValueError('Empty AND term in plain text formula')
          parts.append(current)
          current = []
        else:
          current.append(token)

      if not current:
        raise ValueError('Empty AND term in plain text formula')
      parts.append(current)

      formula = self._parse_relational(parts[0])
      for part in parts[1:]:
        formula = Formula.BooleanOperatorFormula('AND', formula, self._parse_relational(part))
      return formula

    def _parse_relational(self, tokens: list[str]) -> SubFormulaType:
      if len(tokens) == 1:
        return self._parse_term(tokens[0])

      for op in ('==', '!=', '<=', '>=', '<', '>'):
        if op in tokens:
          index = tokens.index(op)
          if len(tokens) != 3 or index != 1:
            break
          left = self._parse_term(tokens[0])
          right = self._parse_term(tokens[2])
          return Formula.RelationalOperatorFormula(op, left, right)

      return self._parse_arithmetic(tokens)

    def _parse_arithmetic(self, tokens: list[str]) -> SubFormulaType:
      precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
      output: list[str] = []
      operators: list[str] = []

      for token in tokens:
        if token in arithmeticOperators:
          while operators and operators[-1] in precedence and precedence[operators[-1]] >= precedence[token]:
            output.append(operators.pop())
          operators.append(token)
        else:
          output.append(token)

      while operators:
        output.append(operators.pop())

      stack: list[SubFormulaType] = []
      for token in output:
        if token in ['+', '-', '*', '/']:
          right = stack.pop()
          left = stack.pop()
          stack.append(Formula.ArithmeticFormula(cast(arithmeticOperatorsType, token), left, right))
        else:
          stack.append(self._parse_term(token))

      if len(stack) != 1:
        raise ValueError(f'Unsupported arithmetic expression: {" ".join(tokens)}')
      return stack[0]

    def _parse_term(self, token: str) -> SubFormulaType:
      if token in ('TRUE', 'FALSE'):
        return Formula.BooleanFormula(token == 'TRUE')
      if re.fullmatch(r'\d+\.\d+|\d+', token):
        return Formula.NumericFormula(float(token) if '.' in token else int(token))
      return Formula.VariableFormula(token)

  def evaluate_formula(self, variables: dict[str, Union[bool, int, float]] = {}) -> Union[bool, int, float]:

    if self.formula.type == 'BooleanFormula':
      return self.formula.value
    elif self.formula.type == 'NumericFormula':
      return self.formula.evaluate_as_numeric(variables)
    elif self.formula.type == 'BooleanOperatorFormula':
      return self.formula.evaluate_as_boolean(variables)
    elif self.formula.type == 'RelationalOperatorFormula':
      return self.formula.evaluate_as_boolean(variables)
    elif self.formula.type == 'ArithmeticFormula':
      return self.formula.evaluate_as_numeric(variables)
    elif self.formula.type == 'PlainTextFormula':
      return Formula(self.formula.to_formula()).evaluate_formula(variables)
    else:
      return False

BooleanFormula = Formula.BooleanFormula
NumericFormula = Formula.NumericFormula
VariableFormula = Formula.VariableFormula
BooleanOperatorFormula = Formula.BooleanOperatorFormula
RelationalOperatorFormula = Formula.RelationalOperatorFormula
PlainTextFormula = Formula.PlainTextFormula
ArithmeticFormula = Formula.ArithmeticFormula


def parse_cli_variables(variable_args: list[str]) -> dict[str, Union[bool, int, float]]:
  result: dict[str, Union[bool, int, float]] = {}
  for variable in variable_args:
    if '=' not in variable:
      raise ValueError(f"Invalid variable assignment: {variable}. Use name=value")
    name, raw_value = variable.split('=', 1)
    normalized = raw_value.strip()
    if normalized.lower() in ('true', 'false'):
      result[name] = normalized.lower() == 'true'
    elif re.fullmatch(r'\d+\.\d+', normalized):
      result[name] = float(normalized)
    elif re.fullmatch(r'\d+', normalized):
      result[name] = int(normalized)
    else:
      raise ValueError(f"Unsupported variable value type for {name}: {raw_value}")
  return result


def main() -> None:
  parser = argparse.ArgumentParser(description='Evaluate a plain-text formula.')
  parser.add_argument('formula', help='Plain text formula, e.g. "x + 3 AND y > 1"')
  parser.add_argument('-v', '--var', action='append', default=[], help='Variable assignment in the form name=value', metavar='name=value')
  args = parser.parse_args()

  variables = parse_cli_variables(args.var)
  formula = Formula(Formula.PlainTextFormula(args.formula))
  result = formula.evaluate_formula(variables)
  print(result)

if __name__ == '__main__':
  main()