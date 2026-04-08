<h1>Formula Evaluation</h1>

<h2>Description</h2>

This project combines ideas from several different formula processing problems I've worked on while studying. I've seen questions asking:

1. Parse an equation into tokens and solve the equation

2. Evaluate an equation that is represented as a tree. The tree can have left and right nodes that are also trees

3. Handle variables in 1 and 2

<h2>Usage</h2>

A formula can be expressed as any logical combination of numbers, booleans, variables, boolean operators (OR, AND), arithmetic operations (+, -, *, /), and relational operators (==, !=, <, <=, >, >=). 

These formulas can be expressed as a tree:

```
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
```

These formulas can be expressed in plaintext:

```
formula = Formula(formula=PlainTextFormula("10 > 5 AND 10 < 20"))
```

These formulas can also be expressed in the CLI as plaintext:

```
python formulaEvaluation.py "x + y" -v x=6 -v y=5
```

<h2>Future work</h2>

- I'm not convinced this evalutor works for all logically coherent possible inputs

- I want this evaluator to handle some Javascript-esque logic, like "1 + True = 2", currently it does not support specifically arithmetic operations on a boolean value. It probably doesn't support a variety of other odd combos like this