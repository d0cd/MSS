# Initially wanted this to be a true `interface` in the OOP sense, but I don't particularly like Python's ABC module
class Runtime:
    """An interface to describe runtimes for DAGs and system components"""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Runtime class should not be implemented. Create a subclass.")

    def get_runtime(self, *args, **kwargs) -> int:
        raise NotImplementedError("`time` method should not be implemented. Implement in a subclass of runtime")


class ConstantTime(Runtime):
    """"Constant runtime"""
    time: int

    def __init__(self, _time: int):
        self.time =  _time

    def get_runtime(self) -> int:
        return self.time