from interpreter.interpreter import Scope, Var, DataType, Value
from interpreter.program import LiteralType, Literal


def test_ctor_args():
    args = [
        Var("a", Value(DataType.NULL, None), False),
        Var("b", Value(DataType.NUM, 1), False),
    ]
    s = Scope(*args)
    assert s.look_up("a") == args[0]
    assert s.look_up("b") == args[1]


def test_update():
    var = Var("a", Value(DataType.NULL, None), False)

    s = Scope()
    s.update(var)
    assert s.var["a"] == var


def test_look_up():
    var = Var("a", Value(DataType.NULL, None), False)
    s = Scope()
    s.update(var)
    assert s.look_up("a") == var
