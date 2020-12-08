from enum import Enum
from typing import Dict, Tuple, List, Optional

import sys

from .dag import Function
from .runtime import Runtime


class ResourceType(Enum):
    CPU = 1
    GPU = 2


class Resource:
    """A class representing an actual resource, e.g ARMv7_CPU"""
    name: str
    typ: ResourceType
    active: Dict[Tuple[str, str], Tuple[float, int]]
    available_space: float
    nearest_finish: int

    def __init__(self, _name: str, _typ: ResourceType):
        self.name = _name
        self.typ = _typ
        self.active = {}
        self.available_space = 100.0
        self.nearest_finish = sys.maxsize

    def add_function(self, fun: Function, tag: str, curr_time: int, *args, **kwargs) -> bool:
        needed_space = fun.resources[self.name]['space']
        if self.can_add_function(fun, tag):
            self.available_space -= needed_space
            pre_rt: Runtime = fun.resources[self.name]['pre']
            exec_rt: Runtime = fun.resources[self.name]['exec']
            post_rt: Runtime = fun.resources[self.name]['post']
            finish_time = curr_time + pre_rt.get_runtime(*args, **kwargs) + exec_rt.get_runtime(*args, **kwargs) + post_rt.get_runtime(*args, **kwargs)
            self.active[(fun.unique_id, tag)] = (needed_space, finish_time)
            self.nearest_finish = self.__find_nearest_finish()
            print(f"Added resource: {tag} at time: {curr_time} on resource: {self.name}")
            return True
        else:
            return False

    def can_add_function(self, fun: Function, tag: str) -> bool:
        assert (fun.unique_id, tag) not in self.active.keys(), \
            f"Function: {fun.unique_id} and tag: {tag} is already allocated on this resource."
        assert self.name in fun.resources, f"Function: {fun.unique_id} cannot be scheduled on this resource"
        assert 'space' in fun.resources[self.name], \
            "Function needs to define the amount of space it needs on this resource."
        assert 'exec' in fun.resources[self.name], \
            "Function needs to define the amount of time it takes to execute on this resource."
        assert 'type' in fun.resources[self.name], \
            "Function needs to define the type of the resource it needs"
        if fun.resources[self.name]['type'] == self.typ:
            needed_space = fun.resources[self.name]['space']
            if self.available_space >= needed_space:
                return True
        return False

    def remove_function(self, fun: Function, tag: str, curr_time: int):
        fname = fun.unique_id
        self.__remove_helper(fname, tag, curr_time)

    def remove_at_time(self, curr_time: int) -> List[Tuple[str, str]]:
        removed_functions = []
        for k, v in self.active.copy().items():
            if curr_time >= v[1]:
                self.__remove_helper(k[0], k[1], curr_time)
                removed_functions.append(k)
        return removed_functions

    def __remove_helper(self, fname: str, tag: str, curr_time: int):
        assert (fname, tag) in self.active, f"Function {fname} is not allocated on this resource"
        assert curr_time >= self.active[(fname, tag)][1], "Function execution must finish before removal."
        (freed_space, finish_time) = self.active.pop((fname, tag))
        self.available_space += freed_space
        assert 0.0 <= self.available_space <= 100.0, "Avaailable space must always represent a percentage."
        if finish_time == self.nearest_finish:
            self.nearest_finish = self.__find_nearest_finish()

    def __find_nearest_finish(self) -> int:
        finish_times = []
        for k, v in self.active.items():
            finish_times.append(v[1])
        return min(finish_times, default=-1)


class ResourcePool:
    """A pool of resources of a single type."""
    name: str
    typ: ResourceType
    resources: Dict[str, Resource]

    def __init__(self, _name: str, _typ: ResourceType, _resources: List[Tuple[str, Resource]]=[]):
        self.name = _name
        self.typ = _typ
        self.resources = {}
        for (name, r) in _resources:
            assert _typ == r.typ, "Resource types must all be the same."
            assert name not in self.resources, "Each resource must have a unique identifier"
            self.resources[name] = r

    def __getitem__(self, item: str):
        return self.resources[item]

    def __iter__(self):
        self._resource_iter = iter(self.resources)
        return self

    def __next__(self):
        return next(self._resource_iter)

    def get_all_resources(self) -> List[Resource]:
        return self.resources.values()

    def find_available_resources(self, fun: Function, tag: str) -> List[Tuple[str, Resource]]:
        available = []
        for k, v in self.resources.items():
            if v.name in fun.resources and v.can_add_function(fun, tag):
                available.append((k, v))
        return available

    def find_first_available_resource(self, fun: Function, tag: str) -> Optional[Tuple[str, Resource]]:
        for k, v in self.resources.items():
            if v.name in fun.resources and v.can_add_function(fun, tag):
                return (k, v)
        return None
