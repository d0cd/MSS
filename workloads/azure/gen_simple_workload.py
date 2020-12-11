import pandas as pd

from utils import read_function_invocations

def gen_simple_workload(path_to_invocations, number_of_functions):
    invocations = read_function_invocations(path_to_invocations, start=1, end=1440)
    funcs = invocations.sample(n=number_of_functions)
    for f in funcs.iterrows():
        print(type(f))


if __name__ == "__main__":
    gen_simple_workload('azurefunctions-dataset2019/', 10)
