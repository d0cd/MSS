from azuretools.utils import read_function_invocations


# Note: This is a good place to test intermediate logic for new benchmarks
def gen_simple_workload(path_to_invocations, number_of_functions):
    invocations = read_function_invocations(path_to_invocations, triggers=['http'], start=1, end=1440)
    funcs = invocations.sample(n=number_of_functions)
    tot = 0
    for f in funcs.itertuples():
        tot += sum(f[5:5+10])
    print(tot)


if __name__ == "__main__":
    gen_simple_workload('../../azuretools/azurefunctions-dataset2019/', 50)
