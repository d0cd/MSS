from copy import deepcopy
from dataclasses import dataclass
from networkx import DiGraph, is_directed_acyclic_graph, topological_sort
from typing import List, Dict


@dataclass
# TODO: If function logic starts getting complicated, then we should move this to a different file
class Function:
    """Class for defining a function, its required resources, execution time, etc."""
    unique_id: str                     # We need this to refer to individual functions in our DAG
    request_time: int                  # Time the request arrives into our system
    cpu_time: int                      # Time in CPU
    transfer_into_cpu_time: int        # Transfer from previous function's GPU into our CPU
    gpu_time: int                      # Time in GPU
    transfer_into_gpu_time: int        # Transfer from previous function's CPU into our GPU
    next_functions: List[str]          # List of subsequent unique_ud's if more functions in DAG


class Dag:
    functions: Dict[str, Function]
    graph: DiGraph

    def __init__(self, funs: List[Function]=[]):
        self.functions = {}
        self.graph = DiGraph()
        for fun in funs:
            self.add_function(fun)

    def add_function(self, fun: Function):
        assert fun.unique_id not in self.functions
        self.functions[fun.unique_id] = fun
        self.graph.add_node(fun.unique_id)
        for uid in fun.next_functions:
            self.graph.add_node(uid)
            self.graph.add_edge(fun.unique_id, uid)

    def add_edge(self, fun1_unique_id: str, fun2_unique_id: str):
        assert fun1_unique_id in self.functions
        assert fun2_unique_id in self.functions
        assert self.graph
        fun1_next_functions = self.functions[fun1_unique_id].next_functions
        if fun2_unique_id not in fun1_next_functions:
            fun1_next_functions.append(fun2_unique_id)
        self.graph.add_edge(fun1_unique_id, fun2_unique_id)

    def __contains__(self, index: str) -> bool:
        return index in self.functions

    def __getitem__(self, index: str) -> Function:
        return self.functions[index]

    def sanity_check(self):
        # Check that all nodes are present
        func_keys = set(self.functions.keys())
        graph_nodes = set(self.graph.nodes)
        assert func_keys == graph_nodes, "All functions must be present in the graph and in each function's `next_functions`"
        # Check that there are no cycles
        assert is_directed_acyclic_graph(self.graph), "Function graph must actually be a DAG"

    def get_topological_execution_order(self) -> List[Function]:
        sorted_uids = topological_sort(self.graph)
        return list(map(lambda uid: self.functions[uid], sorted_uids))

    def get_dep_graph_original(self) -> DiGraph:
        return self.graph

    def get_dep_graph_copy(self) -> DiGraph:
        return deepcopy(self.graph)






