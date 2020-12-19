from simulator.resource import *

from workloads.toy.fifo_system import FifoSystem
from workloads.toy.benchmarks.gen_bench import gen_single_burst_bench



cpu_pool = ResourcePool("STD_CPU_POOL", ResourceType.CPU, [("STD_CPU_1", Resource("STD_CPU", ResourceType.CPU))])
gpu_pool = ResourcePool("STD_GPU_POOL", ResourceType.GPU, [("STD_GPU_1", Resource("STD_GPU", ResourceType.GPU))])

# Add DAGs here
events, hist = gen_single_burst_bench(50, 50, time_in_ms=1200, number_of_requests=1200)

system = FifoSystem(events,
					  {
						  "STD_CPU_POOL" : cpu_pool,
						  "STD_GPU_POOL" : gpu_pool
					  })


if __name__ == "__main__":
	overall_latency = system.run()
	print(f"Time all functions finished is: {overall_latency}")
	total_requests = 0
	latency_slos_met = 0
	cost_slos_met = 0
	for tag, (lat_met, cost_met) in system.logs.items():
		total_requests += 1
		if lat_met: latency_slos_met += 1
		if cost_met: cost_slos_met += 1
	print(f"Total requests: {total_requests}")
	print(f"Latency SLOs met: {latency_slos_met}")
	print(f"Cost SLOs met: {cost_slos_met}")
	print(f"Goodput latency (r/s): {latency_slos_met / (overall_latency / 1000)}")
	print(f"Goodput cost (r/s): {cost_slos_met / (overall_latency / 1000)}")
