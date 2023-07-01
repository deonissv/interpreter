from typing import Optional, List

from interpreter.interpreter import Scope, Var, Function


class GlobalScope:
    def __init__(self):
        self.glob: Scope = Scope()
        self.stack: [Scope] = []

    def top(self) -> Optional[Scope]:
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

    def look_up(self, name: str) -> Optional[Var | Function]:
        if top := self.top():
            if res := top.look_up(name):
                return res
        return self.glob.look_up(name)

    def update(self, var: Var | Function) -> None:
        if top := self.top():
            return top.update(var)
        return self.glob.update(var)

    def fn_call(self, fn: Function, *args: [Var]) -> None:
        scope = Scope(*args)
        scope.update(fn)
        self.stack.append(scope)

    def fn_return(self) -> bool:
        if len(self.stack) == 0:
            return False
        self.stack.pop()
        return True
