
from simulator.event_queue import EventQueue
from simulator.resource import *
from simulator.dag import Dag
from simulator.system import System

from workloads.toy.linear_dag import linear_dag
from workloads.toy.branch_dag import branch_dag

class SimpleSystem(System):

	def __init__(self,_events: EventQueue, _pools: Dict[str, ResourcePool]):
		super().__init__(_events, _pools)

	def schedule(self, curr_time, events, *args, **kwargs):
		# First check for any completed functions
		for name, pool in self.pools.items():
			for resource in pool.get_all_resources():
				completed = resource.remove_at_time(curr_time)
				for (fid, tag) in completed:
					assert tag in self.outstanding_requests, "Tag needs to map to an outstanding request"
					self.outstanding_requests[tag] = (True, self.outstanding_requests[tag][1])
		# Now process any new events
		for (dag, input) in events:
			dag.execute()  # Need to do this to seal the DAG
			self.outstanding_requests[self.__generate_tag(dag, curr_time)] = (True, dag)
		# Now schedule functions
		for tag, (flag, dag) in self.outstanding_requests.copy().items():
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
					else:
						pool = self.pools['STD_GPU_POOL']
					# If there is a resource available, schedule it
					result : Optional[Tuple[str, Resource]] = pool.find_first_available_resource(nxt, tag)
					if result:
						(name, rsrc) = result
						rsrc.add_function(dag.next_function(), tag, curr_time)
						self.outstanding_requests[tag] = (False, self.outstanding_requests[tag][1])
				else:
					# Remove if there is no next function
					self.outstanding_requests.pop(tag)

	def __generate_tag(self, dag: Dag, time: int):
		return f"{dag.name}:{time}:{id(dag)}"

	def __decode_tag(self, tag: str) -> Dag:
		return self.outstanding_requests[tag]


cpu_pool = ResourcePool("STD_CPU_POOL", ResourceType.CPU, [("STD_CPU_1", Resource("STD_CPU", ResourceType.CPU))])
gpu_pool = ResourcePool("STD_GPU_POOL", ResourceType.GPU, [("STD_GPU_1", Resource("STD_GPU", ResourceType.GPU))])

# Add DAGs here
events = EventQueue([
	(linear_dag, [(0, None), (0, None), (0, None), (0, None), (1, None), (1, None)]),
	(branch_dag, [(0, None), (0, None), (0, None), (0, None), (1, None), (1, None)])
])

system = SimpleSystem(events,
					  {
						  "STD_CPU_POOL" : cpu_pool,
						  "STD_GPU_POOL" : gpu_pool
					  })


if __name__ == "__main__":
	overall_latency = system.run()
	print(f"Time all functions finished is: {overall_latency}")

