from workloads.clockwork.clockwork import Clockwork
from workloads.clockwork.benchmarks.azure_functions import azure_bench_1

if __name__ == "__main__":
    events = azure_bench_1("../../../azuretools/azurefunctions-dataset2019")
    clockwork = Clockwork(events, num_workers=12)
    clockwork.run()