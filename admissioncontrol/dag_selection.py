"""
1. Start with collapsed array of the linearized DAG
2. Iterate through array, at each step trying each configuration, updating the set of resources as you go
3. Recursively call the function at each valid config,
"""
from enum import Enum


class Resource(Enum):
	CPU = [1, 100]
	GPU = [3, 20]


class IOLatency(Enum):
	CPU = 3
	GPU = 9
	Network = 1


class Node:

	def __init__(self, id, resource_type):
		self.id = id
		self.resource_type = resource_type
		self.memory = resource_type.value[1]


class Cluster:

	def __init__(self, nodes):
		self.nodes = nodes


class Function:

	def __init__(self, id, runtimes, max_memory, prev_funcs=set(), next_funcs=set()):
		self.id = id
		self.runtimes = runtimes
		self.max_memory = max_memory
		self.prev_funcs = prev_funcs
		self.next_funcs = next_funcs

	def get_resource_runtime(self, resource):
		return self.runtimes[resource]


class FunctionInstance:

	def __init__(self, function, prev_instances=set(), next_instances=set(), node=None):
		self.function = function
		self.prev_instances = prev_instances
		self.next_instances = next_instances
		self.node = node
		self.evaluated = False
		self.accessible = False

	def set_accessible(self):
		for instance in self.prev_instances:
			if not instance.evaluated:
				self.accessible = False
				return False

		self.accessible = True
		return True


class DAG:

	def __init__(self, root, max_time, max_cost):
		self.root = root
		self.max_time = max_time
		self.max_cost = max_cost


class Placement:

	def __init__(self, cluster, dag):
		self.cluster = cluster
		self.dag = dag
		self.dag_instances = FunctionInstance(dag.root)



def gen_valid_placements(cluster, dag):


