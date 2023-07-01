from interpreter.interpreter import GlobalScope, Scope, Var, Function, DataType, Value
from interpreter.program import Block, LiteralType, Literal


def test_top():
    gs = GlobalScope()
    s = Scope()
    gs.stack.append(s)
    assert gs.top() == s


def test_top_empty():
    gs = GlobalScope()
    assert gs.top() is None


def test_update_empty():
    gs = GlobalScope()
    var = Var("a", Value(DataType.NULL, None), False)
    gs.update(var)
    assert gs.glob.var["a"] == var


def test_update():
    gs = GlobalScope()
    s = Scope()
    gs.stack.append(s)
    var = Var("a", Value(DataType.NULL, None), False)
    gs.update(var)
    assert gs.top().var["a"] == var


def test_look_up_empty():
    gs = GlobalScope()
    var = Var("a", Value(DataType.NULL, None), False)
    gs.update(var)
    assert gs.look_up("a") == var


def test_look_up():
    gs = GlobalScope()
    s = Scope()
    gs.stack.append(s)
    var = Var("a", Value(DataType.NULL, None), False)
    gs.update(var)
    assert gs.look_up("a") == var


def test_look_not_defined():
    gs = GlobalScope()
    s = Scope()
    gs.stack.append(s)
    var = Var("a", Value(DataType.NULL, None), False)
    gs.update(var)
    assert gs.look_up("b") is None


def test_fn_call():
    args = [
        Var("a", Value(DataType.NULL, None), False),
        Var("b", Value(DataType.NUM, 1), False),
    ]
    fn = Function("fn", [], Block([]))

    gs = GlobalScope()
    gs.fn_call(fn, *args)

    assert gs.look_up("a") == args[0]
    assert gs.look_up("b") == args[1]
    assert gs.look_up("fn") == fn
    assert len(gs.stack) == 1


def test_return():
    args = [
        Var("a", Value(DataType.NULL, None), False),
        Var("b", Value(DataType.NUM, 1), False),
    ]
    fn = Function("fn", [], Block([]))

    gs = GlobalScope()
    gs.fn_call(fn, *args)
    assert gs.fn_return() == True
    assert len(gs.stack) == 0


def test_return_out_of_fn():
    gs = GlobalScope()
    assert gs.fn_return() == False


def test_args():
    args = [
        Var("a", Value(DataType.NULL, None), False),
        Var("b", Value(DataType.NUM, 1), False),
    ]
    fn = Function("fn", [], Block([]))

    gs = GlobalScope()
    gs.fn_call(fn, *args)
    assert gs.look_up("a") == args[0]
    assert gs.look_up("b") == args[1]
