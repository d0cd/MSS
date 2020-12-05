"""
1. Start with collapsed array of the linearized DAG
2. Iterate through array, at each step trying each configuration, updating the set of resources as you go
3. Recursively call the function at each valid config,
"""
from enum import Enum


class Resource(Enum):
	CPU = [1, 100]
	GPU = [3, 20]


class Node:

	def __init__(self, first_type):
		self.resource_type = first_type
		self.memory = first_type.value[1]


class Cluster:

	def __init__(self, nodes):
		self.nodes = nodes


class Function:

	def __init__(self, runtimes, max_memory, is_root=False, is_leaf=False, prev_funcs=[], next_funcs=[]):
		self.runtimes = runtimes
		self.max_memory = max_memory
		self.is_root = is_root
		self.is_leaf = is_leaf
		self.prev_funcs = prev_funcs
		self.next_funcs = next_funcs

	def get_resource_runtime(self, resource):
		return self.runtimes[resource]


class DAG:

	def __init__(self, root, max_time, max_cost):
		self.root = root
		self.max_time = max_time
		self.max_cost = max_cost
		self.valid_placements = []
		self.all_functions = []
		seen_set = set()
		curr_set = set()
		curr_set.add(self.root)


		while len(curr_set) > 0:
			self.all_functions.append(curr_set.copy())

			seen_set = seen_set.union(curr_set)

			curr_list = list(curr_set)
			new_curr_set = set()
			for function in curr_list:
				temp_next = list(function.next_funcs)
				for next_func in temp_next:
					temp_prev = next_func.prev_funcs
					if len(temp_prev.difference(seen_set)) == 0:
						new_curr_set.add(next_func)

			curr_set = new_curr_set


class Placement:

	def __init__(self, cluster, dag):
		self.cluster = cluster
		self.dag = dag
		self.func_place = []
		for batch in dag.all_functions:
			batch_map = {}
			batch_list = list(batch)
			for function in batch_list:
				batch_map[function] = None

			self.func_place.append(batch_map)

	def place_copy(self):
		new_place = Placement(self.cluster, self.dag)
		for i in range(len(self.func_place)):
			for function, place in self.func_place[i]:
				new_place.func_place[i][function] = place

		return new_place