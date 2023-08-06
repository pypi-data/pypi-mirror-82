# GearUp

Have you ever had a moment, when the code is ready, you are eager to launch it,
you want to know if your new and shiny method works or not, just to realize you need to write
100+ lines of `argparse` or `click`?

Gear up and get ready to go! 

## Quick (and only) intro

Assume your project contains `main.py` script with the following functions: 

```python
def train(method : str, dataset : str, alpha : float):
  <do stuff>

def test(method : str, dataset : str):
  <do testing>
```

Just add:

```python
from gearup import gearup

if __name__ == '__main__':
  gearup(train, test)()
```

and you are ready to go!

```bash
> python main.py train method=resnet dataset=mnist alpha=0.01
> python main.py test method=resnet dataset=mnist
```

## Installation

As usual:
```bash
pip install gearup
```
or
```bash
pip install git+https://gitlab.com/craynn/gearup.git
```

## How it works

`gearup`, applied to a function, reads signature of the function
and infers types of its arguments from the annotations:

```python
def f(x: int, y: int):
  return x + y
```

Annotations here can be any callable of type `str -> A`,
that raises either `ValueError` or `TypeError` when its argument is not a proper
representation of any instance of type `A`.

When gear-uped function is called without arguments it reads `sys.argv`,
alternatively, it can be called with a list of strings:

```python
gearup(f)(['1', '2']) ### result = 3
gearup(f)() ### read from console arguments
```

Then, gear-uped function parses arguments using the following rules:
- if `=` symbol is present in the argument: `k=v`, value `v` is assigned
  to the argument `k` and added to `kwargs`;
- otherwise, the argument is treated as a positional one and appended to `args`.

After that the underlying function is called: `f(*args, **kwargs)`,
converting arguments in their respective types beforehand...

Yes, no flags, no aliases, just launch script like
a python function (Haskell style)...

```bash
> python main.py 1 y=2
```

*Notes:*
- **spaces should not appear between argument name, `=` and argument value**:
  - `a=x` sets value of argument `a` to `x`;
  - `a = x` is interpreted as three separate arguments: two positional: `a` and `x`, and a keyword one
  (with empty name and value);
- if you need to supply a value with a space character in it, use quotes:
  `python main.py x='a b c'`;
- if you need to supply a value with `=` character in it, just specify argument name:
  `python main.py x=a=b` or, better, `python main.py x='a=b'`;
- it is impossible to set one of variational positional arguments (`*args`) to a value,
  that contains `=` character;
- if annotation is absent, type of the argument is inferred from its default value;
  - the only exception from this rule is `None`, in such case, type of the argument is still considered to be absent;
- default value can be of different type than annotation:
  - this can be used to detect if value was specified or not, e.g. `def f(flag: bool = None)`; 
- `bool` is automatically wrapped into `gearup.common.boolean` (see below).

As a bonus, `gearup.apply(f, *args, **kwargs)` provides a Python-friendly way to do the same thing, which
is useful when your script contains multiple methods with non-identical sets of parameters.

```python
import gearup

def method1(x: int, y: int): return x + y
def method2(x: int, z: float): return x / z

def main(method: gearup.choice(method1, method2), x: int, **kwargs):
  gearup.apply(method, x, **kwargs)

if __name__ == '__main__':
  gearup.gearup(main)()
``` 
 

### Commands

Sometimes you need to pack several functions into one script:

```python
gearup(train, test)()
### or
gearup(train=train, test=test)()
### or
gearup(train, test=test)()
```

```bash
> python main.py train <arguments for train>
> python main.py test <arguments for test>
```

More precisely, if supplied with more than one argument or at least one keyword argument,
`gearup` consumes the first CLI argument and
switches between provided functions.

Bonus: it is recursive!

```python
def train(...): pass
def test_fast(...): pass
def test_slow(...): pass

gearup(
  train,
  test=dict(
    fast=test_fast,
    slow=test_slow
  )
)()
```

```bash
> python main.py train method=resnet alpha=0.1
> python main.py test slow method=resnet
```

Note: when a non-keyword argument is passed to `gearup`,
it reads `__name__` attribute of this argument. For example, `gearup(f1, f2)` is equivalent to
`gearup(f1=f1, f2=f2)`.

## Misc.

### Flags

As `bool` type behaves strangely in Python (e.g., `bool('False') == True`),
annotation `bool` is automatically replaced by `gearup.common.boolean`,
that parses strings that represent boolean values properly.

### Variable keyword arguments

Variable keyword arguments (`**kwargs`) are automatically processes by `gearup.special.kwargs`.

`gearup.special.kwargs` supports complex arguments like `classifier.alpha=1.0`, in which case,
it expands variables into nested dictionaries, for example:

```python
from gearup import gearup

def f(**kwargs):
  print(kwargs)

gearup(f)(['clf.alpha=1', 'clf.beta=2', 'method.beta=3'])
```

prints `{'clf': {'alpha': '1', 'beta': '2'}, 'method': {'beta': '3'}}`.

This might be useful for handling configuration of methods with non-identical sets of parameters:
```python
from gearup import gearup, apply, choice

def f1(alpha: float): return alpha
def f2(beta: float, gamma: float): return beta + gamma

def main(f: choice(f1, f2), **kwargs):
  return apply(f, **kwargs.get('func', dict()))

gearup(main)(['f=f1', 'func.alpha=3']) ### returns 6.0
gearup(main)(['f=f2', 'func.beta=5', 'func.gamma=6']) ### returns 11.0
```

### Config

`gearup.config` offers a more strict version of such behavior.
`gearup.config(arg_name_1, arg_name_2, ..., arg_name_n, typed_arg_1=type_1, ..., typed_arg_m=type_m)`:
- checks that all arguments are from the defined set of arguments (`arg_name_1, ..., typed_arg_m`);
- checks that all arguments are provided;
- if supplied with a type, automatically converts values into the corresponding type;
- `type_i` can also be a dictionary, which will be converted into a nested `config`;
- `typed_arg = None` as well as untyped configuration option `arg_name` indicate unchecked values,
  which might be either a string value (e.g., `argument=1`) or a dictionary
  (possibly with nested dictionaries), e.g., `argument.x=1` or `argument.coefs.alpha=1e-3`.

`config` might be useful if you want to separate arguments into several sets, for example:

```python
from gearup import gearup, apply, choice, config

def f1(alpha: float): return 2 * alpha
def f2(beta: float, gamma: float): return beta + gamma

def g1(x: float): return x + 1
def g2(x: float, y: float): return x + y

def main(f: choice(f1, f2), g: choice(g1, g2), **kwargs: config(fargs=None, gargs=None)):
  return apply(f, **kwargs['fargs']) * apply(g, **kwargs['gargs'])

assert gearup(main)(['f=f1', 'g=g2', 'fargs.alpha=2', 'gargs.x=2.0', 'gargs.y=1.5']) == 14.0
assert gearup(main)(['f=f2', 'g=g1', 'fargs.beta=2', 'fargs.gamma=1e-1', 'gargs.x=9.0']) == 21.0
```

### Help

Just add `--help`:

```
> python examples/main.py --help
Available commands:
train -> (method: {nonlogreg, logreg}, power: [-2, 5), alpha: float)   Trains method with alpha.
test -> slow -> (method: {nonlogreg, logreg})   Tests method...
        fast -> (method: {nonlogreg, logreg, inception})   Undocumented test function.
```

`--help` also works with commands:

```
> python examples/main.py test --help
Available commands:
slow -> (method: {logreg, nonlogreg})   Tests method...
fast -> (method: {logreg, inception, nonlogreg})   Undocumented test function.
```

```
> python examples/main.py test slow --help

  Tests method...

  A long
  several lines
  long
  description.
  
(method: {nonlogreg, logreg})
```

### Non-standard types

`gearup` also defines several non-standard types:
- `choice(x_1, x_2, ..., x_n, k_1=v_1, k_2=v_2, ..., k_m=v_m)` --- only accepts arguments from the provided set;
    for a keyword argument `k=v`, `k` is used to retrieve the value `v`, 
    for a positional argument `x` `x.__name__` is used as the key, or `str(x)` if `__name__` attribute is absent;
    works nicely with functions, e.g. `choice(function1, function2)`.
    Don't use with numbers as a single number has multiple string representations, e.g.,
    `choice(1, 2, 3)` does not accept string `'01'`, use `interval` instead.
- `member[module]` --- similar to choice, but retrieves elements from `module.__all__` or
    `dir(object)` if `__all__` is not defined. For example, given a module `utils`,
    `member[utils]` allows to switch between functions defined in the module.
    Also can retrieve values from submodules, e.g., `member[utils]('data.functions.mean')`
    returns `utils.data.functions.mean`.
- `either[type_1, type_2, ..., type_n]` --- tries to convert supplied value to one of the provided types;
  note, that `type_i` has priority over `type_j` if `i < j`, thus, e.g., `either[float, int]`
  is equivalent to `float` as any string representing `int` is also a valid `float`.
- `interval[a:b]` --- half-open interval `a <= x < b`, type (int or float) is inferred from types of `a` and `b`;
  also a more complete constructor exists: `interval(start, stop, left=True, right=False, cast=None)`.
- `a < number`, `a <= number`, `number < b`, `number <= b` - an alternative syntax for constructing intervals,
  intervals can also be combined via `&`, e.g., `(a < number) & (number < b)`
  (note, that parenthesis are required as almost every operator has higher priority than comparison operators).
  Unfortunately,   Python does not support overloading chained comparisons,
  thus, a nice `a < number < b` syntax is not available,
  however, `(a < number) < b` works fine.
