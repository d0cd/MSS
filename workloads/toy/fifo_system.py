from simulator.event_queue import EventQueue
from simulator.resource import *
from simulator.dag import Dag
from simulator.system import System


class FifoSystem(System):
	pools: Dict[str, ResourcePool]
	outstanding_requests: Dict[str, Tuple[bool, Dag, int, int, int, int]]  # flag, Dag, latency_slo, cost_slo, time_arrived, total_cost
	logs: Dict[str, Tuple[bool, bool]] # latency_slo_met?, cost_slo_met?

	def __init__(self,_events: EventQueue, _pools: Dict[str, ResourcePool]):
		super().__init__(_events)
		self.pools = _pools
		self.logs = {}

	def schedule(self, curr_time, events, *args, **kwargs):
		# First check for any completed functions
		for name, pool in self.pools.items():
			for resource in pool.get_all_resources():
				completed = resource.remove_at_time(curr_time)
				for (fid, tag) in completed:
					assert tag in self.outstanding_requests, "Tag needs to map to an outstanding request"
					self.outstanding_requests[tag] = tuple([True]) +  tuple(self.outstanding_requests[tag][1:])
		# Now process any new events
		for (dag, (latency_slo, cost_slo)) in events:
			dag.execute()  # Need to do this to seal the DAG
			self.outstanding_requests[self.__generate_tag(dag, curr_time)] = (True, dag, latency_slo, cost_slo, self.clock, 0)
		# Now schedule functions
		for tag, (flag, dag, latency_slo, cost_slo, time_arrived, total_cost) in self.outstanding_requests.copy().items():
			if flag:
				if dag.has_next_function():
					# Find which resource is faster
					nxt = dag.peek_next_function()
					std_cpu = nxt.resources['STD_CPU']
					std_gpu = nxt.resources['STD_GPU']
					cpu_time = std_cpu['pre'].get_runtime() + std_cpu['exec'].get_runtime() + std_cpu['post'].get_runtime()
					gpu_time = std_gpu['pre'].get_runtime() + std_gpu['exec'].get_runtime() + std_gpu['post'].get_runtime()
					if cpu_time < gpu_time:
						pool = self.pools['STD_CPU_POOL']
						added_cost = nxt.resources['STD_CPU']['cost']
					else:
						pool = self.pools['STD_GPU_POOL']
						added_cost = nxt.resources['STD_GPU']['cost']
					# If there is a resource available, schedule it
					result : Optional[Tuple[str, Resource]] = pool.find_first_available_resource(nxt, tag)
					if result:
						(name, rsrc) = result
						rsrc.add_function(dag.next_function(), tag, curr_time)
						self.outstanding_requests[tag] = (False, dag, latency_slo, cost_slo, time_arrived, total_cost + added_cost)
				else:
					# Remove if there is no next function
					(flag, dag, latency_slo, cost_slo, time_arrived, total_cost) = self.outstanding_requests.pop(tag)
					assert tag not in self.logs, "Duplicate tag found...FIXME"
					latency_slo_met = True if self.clock <= time_arrived + latency_slo else False
					cost_slo_met = True if total_cost <= cost_slo else False
					self.logs[tag] = (latency_slo_met, cost_slo_met)

	def __generate_tag(self, dag: Dag, time: int):
		return f"{dag.name}:{time}:{id(dag)}"

	def __decode_tag(self, tag: str) -> Dag:
		return self.outstanding_requests[tag]