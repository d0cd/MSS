import matplotlib.pyplot as plt
import numpy as np

from workloads.toy.benchmarks.gen_bench import *
from workloads.toy.linear_dag import linear_dag

TIME_IN_MS = 5000
NUM_REQS = 5000

_, uniform_times = gen_uniform_bench(0, 0, [linear_dag],TIME_IN_MS, NUM_REQS)
_, single_burst_times = gen_single_burst_bench(0, 0, [linear_dag], TIME_IN_MS, NUM_REQS)
_, pillar_times = gen_pillar_bench(0, 0, [linear_dag], TIME_IN_MS, NUM_REQS)


plt.hist(uniform_times, bins=100, range=(0, TIME_IN_MS), label="Uniform Requests Benchmark")
plt.savefig('uniform.png')
plt.clf()

plt.hist(single_burst_times, bins=100, range=(0, TIME_IN_MS), label="Single Burst Requests Benchmark")
print(np.histogram(single_burst_times, bins=100, range=(0, TIME_IN_MS)))
plt.savefig('single-burst.png')
plt.clf()

plt.hist(pillar_times, bins=100, range=(0, TIME_IN_MS), label="Pillar Requests Benchmark")
plt.savefig('pillar.png')
plt.clf()
