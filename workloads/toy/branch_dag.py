from simulator.dag import Dag, Function
from simulator.resource import ResourceType
from simulator.runtime import ConstantTime
from .constants import *

branch_front = Function(
	unique_id='branch_front',
	resources= {
		'STD_CPU' : {
			'type' : ResourceType.CPU,
			'space': 100.0,  # Ignoring space this function requires on the CPU
			'pre'  : ConstantTime(1),
			'exec' : ConstantTime(3),
			'post' : ConstantTime(0)
		},
		'STD_GPU' : {
			'type' : ResourceType.GPU,
			'space': 100.0,
			'pre'  : ConstantTime(1),
			'exec' : ConstantTime(1),
			'post' : ConstantTime(0)
		}
	}
)

branch_middles = [Function(    # This function takes a long time to run on a CPU
	unique_id='branch_middle_' + str(ind),
	resources= {
		'STD_CPU' : {
			'type' : ResourceType.CPU,
			'space': 100.0,  # Ignoring space this function requires on the CPU
			'pre'  : ConstantTime(1),
			'exec' : ConstantTime(5),
			'post' : ConstantTime(0)
		},
		'STD_GPU' : {
			'type' : ResourceType.GPU,
			'space': 100.0,
			'pre'  : ConstantTime(1),
			'exec' : ConstantTime(1),
			'post' : ConstantTime(0)
		}
	}
) for ind in range(10)]



branch_back = Function(     # This function takes a long time to run on a GPU
	unique_id='branch_back',
	resources= {
		'STD_CPU' : {
			'type' : ResourceType.CPU,
			'space': 100.0,  # Ignoring space this function requires on the CPU
			'pre'  : ConstantTime(1),
			'exec' : ConstantTime(1),
			'post' : ConstantTime(0)
		},
		'STD_GPU' : {
			'type' : ResourceType.GPU,
			'space': 100.0,
			'pre'  : ConstantTime(1),
			'exec' : ConstantTime(5),
			'post' : ConstantTime(0)
		}
	}
)

# Add costs to functions
all_funs = [branch_front] + branch_middles + [branch_back]
for f in all_funs:
	for rsrc_name, specs in f.resources.items():
		if rsrc_name == 'STD_CPU':
			specs['cost'] = COST_PER_CPU_TIME * specs['exec'].get_runtime()
		else:
			specs['cost'] = COST_PER_GPU_TIME * specs['exec'].get_runtime()

branch_dag = Dag('branch', funs=[branch_front] + branch_middles + [branch_back])
for branch_middle in branch_middles:
	branch_dag.add_edge(branch_front, branch_middle)
	branch_dag.add_edge(branch_middle, branch_back)
branch_dag.sanity_check()