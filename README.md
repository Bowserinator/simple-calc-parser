# Python Math Parser / Calculator

A quick n' dirty math expression parser I wrote to replace the calculator in [jacobot](https://github.com/jacob1/jacobot/tree/master). Should be correct, but not necessarily fast. Uses a modified shunting yard algorithm.

## Features:
- **Regular numbers:** Like `1`, `-1`, `1.5e-5`, `0.2`, `+1.44·`, etc...
- **Hex and bin numbers:** Like `0xBEEF`, `0b10101`
- **All the regular operators:** Like `2 + 2`, `5 % 2`, `5 / 2`, `5 // 2`, `5 ^ 2`
- **Complex numbers:** Like `5j`, `sqrt(-1)`, `1 + i`
- **Functions:** Like `sin`, `angle`, `sum`, `sqrt`, etc...
- **Constants:** Like `pi`, `tau`, `sqrt2`, etc...
- **Vectors:** Like `[1, 2, 3] + 1 = [2, 3, 4]`, etc...
- **Parentheses:** They work!
- **Formatter:** For displaying calculator friendly output without floating point errors

## Demo:

There is an interactive demo you can play around with

```
python3 demo.py
```

## Usage:

```py
from calc.parse import calc
from calc.format import format

result = calc("1 + 1") # 2
print(format(result))
```

Since this is used for a Minecraft bot, format also has an option for Minecraft stack (64) formatting if the result is between 0 and 1e8 inclusive (rounded up to nearest integer). It shows the number of stacks, items, and (shulkers if large enough).

```py
print(format(100, True)) # 1s36
print(format(10000, True)) # 156s16 (5sh 21s16)
```

## Extending functions / operators

### Adding Functions
In `calc/maths.py` add to the `FUNCTIONS` dictionary. Functions take in an array of arguments (either numeric or vector) and a number of arguments (`-1` for variable count)

A function with only 1 argument will be applied to every element of a vector independently (ie, `sin([1, 2]) = [sin(1), sin(2)]`), and a function with var args will be called with the contents of the vector (array) when passed an array (ie `max([1, 2, 3]) = max(1, 2, 3)`)

Functions cannot be overloaded.

### Adding Constants

Add the constant to the `CONSTANTS` dictionary.

### Adding a Binary Operator

Add the function to the `BIN_OPS` dictionary and set the precedence in the `BIN_OPS_PRECEDENCE` dictionary, higher means evaluated first.

### Adding a new Matchable Token

A matchable token is a pair of characters that group a region, ie '[' and ']'. In `lexer.py` add a new token that extends `MatchableToken`, copy the general format of `ParenToken` (the static variables are required, use `MatchableToken.scan`)

Next in `parse.py/shunting_yard`, copy the general example where it checks for a right paren or vector bracket. A dummy `START` token is added before the left brackets / parens so vararg functions can know when to stop popping.

###


## Tests:

```
python3 -m unittest discover -s tests/ -p "*.py"
```

## License

See `LICENSE.md`
