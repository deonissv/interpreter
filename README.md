# Setup

### Run interpreter
```shell
  python -m interpreter <source>
```

### Run tests
```shell
  pytest
```


# Description

### BuiltIn types

|          |      |
| :------- | ---: |
| Numeric  |  num |
| Text     |  str |
| Logical  | bool |
| NullType | null |

### Order of operations

| ↑ (highest) |    Operator     | Associativity |
| :---------- | :-------------: | ------------: |
| 1           |       ()        |          left |
| 2           |     not  -      |         right |
| 3           |     *  /  %     |          left |
| 4           |      +  -       |          left |
| 5           | <  <=  >  >= is |          left |
| 6           |     ==  !=      |         right |
| 7           |       and       |          left |
| 8           |       or        |          left |
| 9           |        =        |         right |

### Key Words

|          |       |       |       |        |             |            |
| :------: | :---: | :---: | :---: | :----: | :---------: | :--------: |
|   and    | else  |  let  | null  |  num   |    isOdd    | isQuarterF |
|  break   | false | match |  or   |  str   | isQuarterO  |   return   |
|   case   |  fn   |  mut  | true  |  bool  | isQuarterTw |            |
| continue |  is   |  not  | while | isEven | isQuarterTh |            |

# Grammar

<pre>
program                         = { statement };

statement                       = assignment
                                | conditional_statement
                                | loop_statement
                                | match_statement
                                | function_call, ";" ;
                                | "break", ";" ;
                                | "continue", ";" ;


assignment                      = "let", [ "mut"], identifier, assign_operator, expression, ";" ;

expression                      = or_expression;
or_expression                   = and_expression, { "or", and_expression };
and_expression                  = relational_expression, { "and", relational_expression };
relational_expression           = additive_expression, { relational_operator,  additive_expression};
additive_expression             = multiplicative_expression, { additive_operator,  multiplicative_expression };
multiplicative_expression       = unary_expression, { multiplicative_operator, unary_expression };
unary_expression                = [ unary_operator ] factor;
factor                          = literal
                                | data_type
                                | identifier
                                | function_call
                                | "(", expression, ")";

conditional_statement           = "if", expression, code_block, [ "else", code_block ];

loop_statement                  = "while", "(" expression ")", code_block;

match_statement                 = "match", match_parameters, ":", { case_statement }, default_statement;
match_parameters                = expression, { ",", expression };
case_statement                  = "case", identifier, ":", case_parameters, code_block;
case_identifier                 = literal
                                | data_type
                                | case_operator;

default_statement               = "default", ":", case_parameters, code_block;
case_parameters                 = identifier, { ",", identifier };
case_operator                   = "isEven"
                                | "isOdd"
                                | "isQuarterO"
                                | "isQuarterTw"
                                | "isQuarterTh"
                                | "isQuarterF";


function_call                   = identifier, "(", [argument_list], ")";
argument_list                   = expression, {",", expression};
function_definition             = "fn", identifier, "(", [function_parameters] ")", code_block;
function_parameters             = function_parameter, {",", function_parameter};
function_parameter              = ["mut"], identifier;

code_block                      = "{" { statement | return_statement } "}";
return_statement                = "return", [ expression ], ";" ;

identifier                      = leading_char, { char_alpha_numeric };

leading_char                    = "_"
                                | alpha_char;

alpha_char                      = ? A-z ?;
char_alpha_numeric              = alpha_char
                                | digit
                                | "_";

data_type                       = "num"
                                | "str"
                                | "bool"
                                | "null";

assign_operator                 = "="
                                | "+="
                                | "-=";

relational_operator             = "<"
                                | ">"
                                | "<="
                                | ">="
                                | "=="
                                | "is";

additive_operator               = "+"
                                | "-"

multiplicative_operator         = "*"
                                | "/"
                                | "%";

unary_operator                  = "!"
                                | "not";

literal                         = number
                                | string
                                | bool
                                | "null";

number                          = integer, [ "." ], digit, {digit};
integer                         = digit { non_zero_digit };
digit                           = "0"
                                | non_zero_digit;

non_zero_digit                  = ? 1-9 ?;

string                          = quote_string
                                | double_quote_string;

quote_string                    = "'", any_char, { any_char } "'";
double_quote_string             = '"', any_char, { any_char } '"';
any_char                        = ? any character ?;

</pre>

# Code samples:

### Hello world:

```rust
  print("Hello world!");
```

### by default variables are immutable:

```rust
  let x = 5;
  x = 6;
```
```
  attempt to assign to immutable variable x
   |
 2 | x = 6;
   | ^^^
```

### `string` variable definition:

```rust
let foo = "foo";
let bar = 'baz';
```

### function definition:

```rust
fn sum(arg1, arg2) {
    let sum = arg1 + arg2;
    return sum;
}
```

### recursion:

```rust
fn factorial(n) {
    if n < 0 { return null; }
    if (n == 0)
    or(n == 1)
    { return 1; }
    return n * factorial(n - 1);
}
```

### conditional

```rust
  let a = 5;
  if a < 10 {
    print("!");
  }
  else {
    print("¡");
  }
```

### loop

```rust
  while (x < 100) {
    print(x);
  }
```

### match

```rust
  let x = 1;
  match x:
    case isEven: {
      print("x is even");
    }
    case isOdd: x {
      print("x is odd");
    }

```
