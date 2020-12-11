from simulator.resource import Resource, ResourceType

# We are only defining GPUs as relevant resources since the CPUs are only used to run
# worker threads and RAM is only used as a storage tier.
# A 'heterogenous' version of Clockwork would include both CPU and GPU

NVIDIA_TESLA_V100_GPU = Resource('NVIDIA_TESLA_V100_GPU', ResourceType.GPU)