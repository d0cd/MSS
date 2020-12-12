from simulator.dag import Dag, Function
from simulator.resource import ResourceType
from simulator.runtime import ConstantTime


densenet121 = Function(
    unique_id='densenet121',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.001,
            'pre' : 3.0,
            'input' : 0.000602,
            'exec_b1' : 3.8,
            'exec_b2' : 5.0,
            'exec_b4' : 7.0,
            'exec_b8' : 10.0,
            'exec_b16' : 18.0,
            'output' : 4e-06,
            'post' : 3.0,
        }
    }
)
densenet121_dag = Dag('densenet121', funs=[densenet121])
densenet121_dag.sanity_check()

densenet161 = Function(
    unique_id='densenet161',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00359375,
            'pre' : 9.0,
            'input' : 0.000602,
            'exec_b1' : 8.0,
            'exec_b2' : 10.0,
            'exec_b4' : 15.0,
            'exec_b8' : 24.0,
            'exec_b16' : 40.0,
            'output' : 4e-06,
            'post' : 9.0,
        }
    }
)
densenet161_dag = Dag('densenet161', funs=[densenet161])
densenet161_dag.sanity_check()

densenet169 = Function(
    unique_id='densenet169',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00178125,
            'pre' : 4.5,
            'input' : 0.000602,
            'exec_b1' : 5.0,
            'exec_b2' : 6.0,
            'exec_b4' : 9.0,
            'exec_b8' : 13.0,
            'exec_b16' : 22.0,
            'output' : 4e-06,
            'post' : 4.5,
        }
    }
)
densenet169_dag = Dag('densenet169', funs=[densenet169])
densenet169_dag.sanity_check()

densenet201 = Function(
    unique_id='densenet201',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0025,
            'pre' : 7.0,
            'input' : 0.000602,
            'exec_b1' : 7.0,
            'exec_b2' : 8.0,
            'exec_b4' : 12.0,
            'exec_b8' : 18.3,
            'exec_b16' : 31.0,
            'output' : 4e-06,
            'post' : 7.0,
        }
    }
)
densenet201_dag = Dag('densenet201', funs=[densenet201])
densenet201_dag.sanity_check()

dla34 = Function(
    unique_id='dla34',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00203125,
            'pre' : 5.0,
            'input' : 0.000602,
            'exec_b1' : 3.0,
            'exec_b2' : 5.0,
            'exec_b4' : 7.0,
            'exec_b8' : 11.0,
            'exec_b16' : 16.0,
            'output' : 4e-06,
            'post' : 5.0,
        }
    }
)
dla34_dag = Dag('dla34', funs=[dla34])
dla34_dag.sanity_check()

googlenet = Function(
    unique_id='googlenet',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00084375,
            'pre' : 2.0,
            'input' : 0.000602,
            'exec_b1' : 2.0,
            'exec_b2' : 2.0,
            'exec_b4' : 3.0,
            'exec_b8' : 4.0,
            'exec_b16' : 7.0,
            'output' : 4e-06,
            'post' : 2.0,
        }
    }
)
googlenet_dag = Dag('googlenet', funs=[googlenet])
googlenet_dag.sanity_check()

inceptionv3 = Function(
    unique_id='inceptionv3',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00296875,
            'pre' : 8.0,
            'input' : 0.001073,
            'exec_b1' : 4.0,
            'exec_b2' : 7.0,
            'exec_b4' : 11.0,
            'exec_b8' : 16.0,
            'exec_b16' : 26.0,
            'output' : 4e-06,
            'post' : 8.0,
        }
    }
)
inceptionv3_dag = Dag('inceptionv3', funs=[inceptionv3])
inceptionv3_dag.sanity_check()

xception = Function(
    unique_id='xception',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00496875,
            'pre' : 13.0,
            'input' : 0.000602,
            'exec_b1' : 4.0,
            'exec_b2' : 7.0,
            'exec_b4' : 10.0,
            'exec_b8' : 19.0,
            'exec_b16' : 35.0,
            'output' : 4e-06,
            'post' : 13.0,
        }
    }
)
xception_dag = Dag('xception', funs=[xception])
xception_dag.sanity_check()

mobile_pose_mobilenet1_0 = Function(
    unique_id='mobile_pose_mobilenet1_0',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.000625,
            'pre' : 2.0,
            'input' : 0.00059,
            'exec_b1' : 0.99,
            'exec_b2' : 2.0,
            'exec_b4' : 3.0,
            'exec_b8' : 6.0,
            'exec_b16' : 11.0,
            'output' : 0.000209,
            'post' : 2.0,
        }
    }
)
mobile_pose_mobilenet1_0_dag = Dag('mobile_pose_mobilenet1_0', funs=[mobile_pose_mobilenet1_0])
mobile_pose_mobilenet1_0_dag.sanity_check()

mobile_pose_mobilenetv3 = Function(
    unique_id='mobile_pose_mobilenetv3',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00059375,
            'pre' : 2.0,
            'input' : 0.00059,
            'exec_b1' : 1.0,
            'exec_b2' : 2.0,
            'exec_b4' : 3.0,
            'exec_b8' : 6.0,
            'exec_b16' : 12.0,
            'output' : 0.000209,
            'post' : 2.0,
        }
    }
)
mobile_pose_mobilenetv3_dag = Dag('mobile_pose_mobilenetv3', funs=[mobile_pose_mobilenetv3])
mobile_pose_mobilenetv3_dag.sanity_check()

mobile_pose_resnet18_v1 = Function(
    unique_id='mobile_pose_resnet18_v1',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00159375,
            'pre' : 4.0,
            'input' : 0.00059,
            'exec_b1' : 1.0,
            'exec_b2' : 2.0,
            'exec_b4' : 4.0,
            'exec_b8' : 6.0,
            'exec_b16' : 11.0,
            'output' : 0.000209,
            'post' : 4.0,
        }
    }
)
mobile_pose_resnet18_v1_dag = Dag('mobile_pose_resnet18_v1', funs=[mobile_pose_resnet18_v1])
mobile_pose_resnet18_v1_dag.sanity_check()

mobile_pose_resnet50_v1 = Function(
    unique_id='mobile_pose_resnet50_v1',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0031875,
            'pre' : 8.0,
            'input' : 0.00059,
            'exec_b1' : 3.0,
            'exec_b2' : 5.0,
            'exec_b4' : 9.0,
            'exec_b8' : 16.0,
            'exec_b16' : 30.0,
            'output' : 0.000209,
            'post' : 8.0,
        }
    }
)
mobile_pose_resnet50_v1_dag = Dag('mobile_pose_resnet50_v1', funs=[mobile_pose_resnet50_v1])
mobile_pose_resnet50_v1_dag.sanity_check()

simple_pose_resnet18_v1b = Function(
    unique_id='simple_pose_resnet18_v1b',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0019375,
            'pre' : 5.0,
            'input' : 0.00059,
            'exec_b1' : 2.0,
            'exec_b2' : 4.0,
            'exec_b4' : 7.0,
            'exec_b8' : 10.7,
            'exec_b16' : 19.0,
            'output' : 0.000209,
            'post' : 5.0,
        }
    }
)
simple_pose_resnet18_v1b_dag = Dag('simple_pose_resnet18_v1b', funs=[simple_pose_resnet18_v1b])
simple_pose_resnet18_v1b_dag.sanity_check()

resnest14 = Function(
    unique_id='resnest14',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0013125,
            'pre' : 3.0,
            'input' : 0.000602,
            'exec_b1' : 2.7,
            'exec_b2' : 4.0,
            'exec_b4' : 7.0,
            'exec_b8' : 13.0,
            'exec_b16' : 23.0,
            'output' : 4e-06,
            'post' : 3.0,
        }
    }
)
resnest14_dag = Dag('resnest14', funs=[resnest14])
resnest14_dag.sanity_check()

resnest26 = Function(
    unique_id='resnest26',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.002125,
            'pre' : 6.0,
            'input' : 0.000602,
            'exec_b1' : 4.3,
            'exec_b2' : 6.0,
            'exec_b4' : 10.0,
            'exec_b8' : 18.0,
            'exec_b16' : 33.0,
            'output' : 4e-06,
            'post' : 6.0,
        }
    }
)
resnest26_dag = Dag('resnest26', funs=[resnest26])
resnest26_dag.sanity_check()

resnest50 = Function(
    unique_id='resnest50',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0034375,
            'pre' : 9.0,
            'input' : 0.000602,
            'exec_b1' : 7.0,
            'exec_b2' : 9.0,
            'exec_b4' : 14.0,
            'exec_b8' : 30.0,
            'exec_b16' : 56.0,
            'output' : 4e-06,
            'post' : 9.0,
        }
    }
)
resnest50_dag = Dag('resnest50', funs=[resnest50])
resnest50_dag.sanity_check()

resnest101 = Function(
    unique_id='resnest101',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00603125,
            'pre' : 16.0,
            'input' : 0.000602,
            'exec_b1' : 12.0,
            'exec_b2' : 16.0,
            'exec_b4' : 26.0,
            'exec_b8' : 45.0,
            'exec_b16' : 78.0,
            'output' : 4e-06,
            'post' : 16.0,
        }
    }
)
resnest101_dag = Dag('resnest101', funs=[resnest101])
resnest101_dag.sanity_check()

resnet18_v1 = Function(
    unique_id='resnet18_v1',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00146875,
            'pre' : 4.0,
            'input' : 0.000602,
            'exec_b1' : 1.0,
            'exec_b2' : 2.0,
            'exec_b4' : 3.0,
            'exec_b8' : 4.0,
            'exec_b16' : 7.0,
            'output' : 4e-06,
            'post' : 4.0,
        }
    }
)
resnet18_v1_dag = Dag('resnet18_v1', funs=[resnet18_v1])
resnet18_v1_dag.sanity_check()

resnet18_v1b = Function(
    unique_id='resnet18_v1b',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00146875,
            'pre' : 4.0,
            'input' : 0.000602,
            'exec_b1' : 1.0,
            'exec_b2' : 2.0,
            'exec_b4' : 2.0,
            'exec_b8' : 4.0,
            'exec_b16' : 7.0,
            'output' : 4e-06,
            'post' : 4.0,
        }
    }
)
resnet18_v1b_dag = Dag('resnet18_v1b', funs=[resnet18_v1b])
resnet18_v1b_dag.sanity_check()

resnet34_v1 = Function(
    unique_id='resnet34_v1',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00271875,
            'pre' : 7.0,
            'input' : 0.000602,
            'exec_b1' : 2.4,
            'exec_b2' : 3.0,
            'exec_b4' : 5.0,
            'exec_b8' : 8.0,
            'exec_b16' : 14.4,
            'output' : 4e-06,
            'post' : 7.0,
        }
    }
)
resnet34_v1_dag = Dag('resnet34_v1', funs=[resnet34_v1])
resnet34_v1_dag.sanity_check()

resnet34_v1b = Function(
    unique_id='resnet34_v1b',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00271875,
            'pre' : 7.0,
            'input' : 0.000602,
            'exec_b1' : 2.0,
            'exec_b2' : 3.0,
            'exec_b4' : 5.0,
            'exec_b8' : 8.0,
            'exec_b16' : 13.0,
            'output' : 4e-06,
            'post' : 7.0,
        }
    }
)
resnet34_v1b_dag = Dag('resnet34_v1b', funs=[resnet34_v1b])
resnet34_v1b_dag.sanity_check()

resnet50_v1 = Function(
    unique_id='resnet50_v1',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0031875,
            'pre' : 8.0,
            'input' : 0.000602,
            'exec_b1' : 3.0,
            'exec_b2' : 4.0,
            'exec_b4' : 6.0,
            'exec_b8' : 9.0,
            'exec_b16' : 16.0,
            'output' : 4e-06,
            'post' : 8.0,
        }
    }
)
resnet50_v1_dag = Dag('resnet50_v1', funs=[resnet50_v1])
resnet50_v1_dag.sanity_check()

resnet50_v1b = Function(
    unique_id='resnet50_v1b',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0031875,
            'pre' : 8.0,
            'input' : 0.000602,
            'exec_b1' : 3.0,
            'exec_b2' : 4.0,
            'exec_b4' : 6.0,
            'exec_b8' : 10.0,
            'exec_b16' : 17.0,
            'output' : 4e-06,
            'post' : 8.0,
        }
    }
)
resnet50_v1b_dag = Dag('resnet50_v1b', funs=[resnet50_v1b])
resnet50_v1b_dag.sanity_check()

resnet50_v1c = Function(
    unique_id='resnet50_v1c',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0031875,
            'pre' : 8.0,
            'input' : 0.000602,
            'exec_b1' : 3.0,
            'exec_b2' : 4.0,
            'exec_b4' : 6.0,
            'exec_b8' : 10.0,
            'exec_b16' : 17.0,
            'output' : 4e-06,
            'post' : 8.0,
        }
    }
)
resnet50_v1c_dag = Dag('resnet50_v1c', funs=[resnet50_v1c])
resnet50_v1c_dag.sanity_check()

resnet50_v1d = Function(
    unique_id='resnet50_v1d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0031875,
            'pre' : 8.0,
            'input' : 0.000602,
            'exec_b1' : 3.0,
            'exec_b2' : 4.0,
            'exec_b4' : 6.0,
            'exec_b8' : 10.0,
            'exec_b16' : 17.0,
            'output' : 4e-06,
            'post' : 8.0,
        }
    }
)
resnet50_v1d_dag = Dag('resnet50_v1d', funs=[resnet50_v1d])
resnet50_v1d_dag.sanity_check()

resnet50_v1s = Function(
    unique_id='resnet50_v1s',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00321875,
            'pre' : 8.0,
            'input' : 0.000602,
            'exec_b1' : 3.0,
            'exec_b2' : 4.0,
            'exec_b4' : 7.0,
            'exec_b8' : 12.0,
            'exec_b16' : 20.0,
            'output' : 4e-06,
            'post' : 8.0,
        }
    }
)
resnet50_v1s_dag = Dag('resnet50_v1s', funs=[resnet50_v1s])
resnet50_v1s_dag.sanity_check()

resnet50_tuned_1_8x = Function(
    unique_id='resnet50_tuned_1_8x',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00275,
            'pre' : 7.0,
            'input' : 0.000602,
            'exec_b1' : 2.0,
            'exec_b2' : 3.0,
            'exec_b4' : 4.0,
            'exec_b8' : 7.0,
            'exec_b16' : 11.0,
            'output' : 4e-06,
            'post' : 7.0,
        }
    }
)
resnet50_tuned_1_8x_dag = Dag('resnet50_tuned_1_8x', funs=[resnet50_tuned_1_8x])
resnet50_tuned_1_8x_dag.sanity_check()

resnet101v1 = Function(
    unique_id='resnet101v1',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0055625,
            'pre' : 15.0,
            'input' : 0.000602,
            'exec_b1' : 5.0,
            'exec_b2' : 8.0,
            'exec_b4' : 11.0,
            'exec_b8' : 18.0,
            'exec_b16' : 30.3,
            'output' : 4e-06,
            'post' : 15.0,
        }
    }
)
resnet101v1_dag = Dag('resnet101v1', funs=[resnet101v1])
resnet101v1_dag.sanity_check()

resnet101_v1b = Function(
    unique_id='resnet101_v1b',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0055625,
            'pre' : 14.0,
            'input' : 0.000602,
            'exec_b1' : 5.0,
            'exec_b2' : 7.8,
            'exec_b4' : 11.0,
            'exec_b8' : 19.0,
            'exec_b16' : 31.0,
            'output' : 4e-06,
            'post' : 14.0,
        }
    }
)
resnet101_v1b_dag = Dag('resnet101_v1b', funs=[resnet101_v1b])
resnet101_v1b_dag.sanity_check()

resnet101_v1c = Function(
    unique_id='resnet101_v1c',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0055625,
            'pre' : 14.0,
            'input' : 0.000602,
            'exec_b1' : 5.0,
            'exec_b2' : 8.0,
            'exec_b4' : 12.0,
            'exec_b8' : 19.0,
            'exec_b16' : 32.0,
            'output' : 4e-06,
            'post' : 14.0,
        }
    }
)
resnet101_v1c_dag = Dag('resnet101_v1c', funs=[resnet101_v1c])
resnet101_v1c_dag.sanity_check()

resnet101_v1d = Function(
    unique_id='resnet101_v1d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0055625,
            'pre' : 14.0,
            'input' : 0.000602,
            'exec_b1' : 5.0,
            'exec_b2' : 8.0,
            'exec_b4' : 11.0,
            'exec_b8' : 19.0,
            'exec_b16' : 32.0,
            'output' : 4e-06,
            'post' : 14.0,
        }
    }
)
resnet101_v1d_dag = Dag('resnet101_v1d', funs=[resnet101_v1d])
resnet101_v1d_dag.sanity_check()

resnet101_v1s = Function(
    unique_id='resnet101_v1s',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00559375,
            'pre' : 15.0,
            'input' : 0.000602,
            'exec_b1' : 5.7,
            'exec_b2' : 8.0,
            'exec_b4' : 12.0,
            'exec_b8' : 21.0,
            'exec_b16' : 35.1,
            'output' : 4e-06,
            'post' : 15.0,
        }
    }
)
resnet101_v1s_dag = Dag('resnet101_v1s', funs=[resnet101_v1s])
resnet101_v1s_dag.sanity_check()

resnet101_tuned_1_9x = Function(
    unique_id='resnet101_tuned_1_9x',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00425,
            'pre' : 11.0,
            'input' : 0.000602,
            'exec_b1' : 4.0,
            'exec_b2' : 6.0,
            'exec_b4' : 7.0,
            'exec_b8' : 13.0,
            'exec_b16' : 21.0,
            'output' : 4e-06,
            'post' : 11.0,
        }
    }
)
resnet101_tuned_1_9x_dag = Dag('resnet101_tuned_1_9x', funs=[resnet101_tuned_1_9x])
resnet101_tuned_1_9x_dag.sanity_check()

resnet101_tuned_2_2x = Function(
    unique_id='resnet101_tuned_2_2x',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00409375,
            'pre' : 11.0,
            'input' : 0.000602,
            'exec_b1' : 4.0,
            'exec_b2' : 5.0,
            'exec_b4' : 7.0,
            'exec_b8' : 11.0,
            'exec_b16' : 19.0,
            'output' : 4e-06,
            'post' : 11.0,
        }
    }
)
resnet101_tuned_2_2x_dag = Dag('resnet101_tuned_2_2x', funs=[resnet101_tuned_2_2x])
resnet101_tuned_2_2x_dag.sanity_check()

resnet152_v1 = Function(
    unique_id='resnet152_v1',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00753125,
            'pre' : 20.0,
            'input' : 0.000602,
            'exec_b1' : 8.0,
            'exec_b2' : 11.0,
            'exec_b4' : 16.0,
            'exec_b8' : 26.0,
            'exec_b16' : 44.6,
            'output' : 4e-06,
            'post' : 20.0,
        }
    }
)
resnet152_v1_dag = Dag('resnet152_v1', funs=[resnet152_v1])
resnet152_v1_dag.sanity_check()

resnet152_v1b = Function(
    unique_id='resnet152_v1b',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.007515625,
            'pre' : 19.54,
            'input' : 0.000602,
            'exec_b1' : 7.86,
            'exec_b2' : 11.36,
            'exec_b4' : 16.41,
            'exec_b8' : 27.05,
            'exec_b16' : 45.49,
            'output' : 4e-06,
            'post' : 19.54,
        }
    }
)
resnet152_v1b_dag = Dag('resnet152_v1b', funs=[resnet152_v1b])
resnet152_v1b_dag.sanity_check()

resnet152_v1c = Function(
    unique_id='resnet152_v1c',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.007515625,
            'pre' : 19.55,
            'input' : 0.000602,
            'exec_b1' : 7.9,
            'exec_b2' : 11.48,
            'exec_b4' : 16.64,
            'exec_b8' : 27.42,
            'exec_b16' : 46.24,
            'output' : 4e-06,
            'post' : 19.55,
        }
    }
)
resnet152_v1c_dag = Dag('resnet152_v1c', funs=[resnet152_v1c])
resnet152_v1c_dag.sanity_check()

resnet152_v1d = Function(
    unique_id='resnet152_v1d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.007515625,
            'pre' : 19.55,
            'input' : 0.000602,
            'exec_b1' : 7.89,
            'exec_b2' : 11.45,
            'exec_b4' : 16.59,
            'exec_b8' : 27.38,
            'exec_b16' : 46.01,
            'output' : 4e-06,
            'post' : 19.55,
        }
    }
)
resnet152_v1d_dag = Dag('resnet152_v1d', funs=[resnet152_v1d])
resnet152_v1d_dag.sanity_check()

resnet152_v1s = Function(
    unique_id='resnet152_v1s',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00753125,
            'pre' : 19.58,
            'input' : 0.000602,
            'exec_b1' : 8.15,
            'exec_b2' : 11.91,
            'exec_b4' : 17.5,
            'exec_b8' : 28.95,
            'exec_b16' : 49.27,
            'output' : 4e-06,
            'post' : 19.58,
        }
    }
)
resnet152_v1s_dag = Dag('resnet152_v1s', funs=[resnet152_v1s])
resnet152_v1s_dag.sanity_check()

resnet18_v2 = Function(
    unique_id='resnet18_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0014593750000000002,
            'pre' : 3.81,
            'input' : 0.000602,
            'exec_b1' : 1.32,
            'exec_b2' : 1.81,
            'exec_b4' : 2.48,
            'exec_b8' : 4.42,
            'exec_b16' : 7.12,
            'output' : 4e-06,
            'post' : 3.81,
        }
    }
)
resnet18_v2_dag = Dag('resnet18_v2', funs=[resnet18_v2])
resnet18_v2_dag.sanity_check()

resnet34_v2 = Function(
    unique_id='resnet34_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.002725,
            'pre' : 7.11,
            'input' : 0.000602,
            'exec_b1' : 2.55,
            'exec_b2' : 3.44,
            'exec_b4' : 4.83,
            'exec_b8' : 7.9,
            'exec_b16' : 14.01,
            'output' : 4e-06,
            'post' : 7.11,
        }
    }
)
resnet34_v2_dag = Dag('resnet34_v2', funs=[resnet34_v2])
resnet34_v2_dag.sanity_check()

resnet50_v2 = Function(
    unique_id='resnet50_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00319375,
            'pre' : 8.32,
            'input' : 0.000602,
            'exec_b1' : 2.73,
            'exec_b2' : 4.05,
            'exec_b4' : 5.87,
            'exec_b8' : 9.93,
            'exec_b16' : 17.3,
            'output' : 4e-06,
            'post' : 8.32,
        }
    }
)
resnet50_v2_dag = Dag('resnet50_v2', funs=[resnet50_v2])
resnet50_v2_dag.sanity_check()

resnet101_v2 = Function(
    unique_id='resnet101_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.005565624999999999,
            'pre' : 14.47,
            'input' : 0.000602,
            'exec_b1' : 5.51,
            'exec_b2' : 8.05,
            'exec_b4' : 11.83,
            'exec_b8' : 18.14,
            'exec_b16' : 33.57,
            'output' : 4e-06,
            'post' : 14.47,
        }
    }
)
resnet101_v2_dag = Dag('resnet101_v2', funs=[resnet101_v2])
resnet101_v2_dag.sanity_check()

resnet152_v2 = Function(
    unique_id='resnet152_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.007518749999999999,
            'pre' : 19.56,
            'input' : 0.000602,
            'exec_b1' : 8.21,
            'exec_b2' : 11.66,
            'exec_b4' : 17.03,
            'exec_b8' : 27.6,
            'exec_b16' : 48.54,
            'output' : 4e-06,
            'post' : 19.56,
        }
    }
)
resnet152_v2_dag = Dag('resnet152_v2', funs=[resnet152_v2])
resnet152_v2_dag.sanity_check()

resnext50_32x4d = Function(
    unique_id='resnext50_32x4d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.003125,
            'pre' : 8.15,
            'input' : 0.000602,
            'exec_b1' : 2.18,
            'exec_b2' : 3.23,
            'exec_b4' : 5.35,
            'exec_b8' : 9.21,
            'exec_b16' : 17.42,
            'output' : 4e-06,
            'post' : 8.15,
        }
    }
)
resnext50_32x4d_dag = Dag('resnext50_32x4d', funs=[resnext50_32x4d])
resnext50_32x4d_dag.sanity_check()

resnext101_32x4d = Function(
    unique_id='resnext101_32x4d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0055125,
            'pre' : 14.34,
            'input' : 0.000602,
            'exec_b1' : 4.65,
            'exec_b2' : 6.27,
            'exec_b4' : 10.06,
            'exec_b8' : 17.75,
            'exec_b16' : 32.83,
            'output' : 4e-06,
            'post' : 14.34,
        }
    }
)
resnext101_32x4d_dag = Dag('resnext101_32x4d', funs=[resnext101_32x4d])
resnext101_32x4d_dag.sanity_check()

resnext101_64x4d = Function(
    unique_id='resnext101_64x4d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.01041875,
            'pre' : 27.18,
            'input' : 0.000602,
            'exec_b1' : 6.46,
            'exec_b2' : 10.24,
            'exec_b4' : 17.13,
            'exec_b8' : 30.42,
            'exec_b16' : 60.23,
            'output' : 4e-06,
            'post' : 27.18,
        }
    }
)
resnext101_64x4d_dag = Dag('resnext101_64x4d', funs=[resnext101_64x4d])
resnext101_64x4d_dag.sanity_check()

se_resnext50_32x4d = Function(
    unique_id='se_resnext50_32x4d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0034406249999999997,
            'pre' : 8.95,
            'input' : 0.000602,
            'exec_b1' : 3.2,
            'exec_b2' : 4.47,
            'exec_b4' : 6.87,
            'exec_b8' : 11.5,
            'exec_b16' : 20.64,
            'output' : 4e-06,
            'post' : 8.95,
        }
    }
)
se_resnext50_32x4d_dag = Dag('se_resnext50_32x4d', funs=[se_resnext50_32x4d])
se_resnext50_32x4d_dag.sanity_check()

se_resnext101_32x4d = Function(
    unique_id='se_resnext101_32x4d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.006109375,
            'pre' : 15.89,
            'input' : 0.000602,
            'exec_b1' : 6.23,
            'exec_b2' : 8.24,
            'exec_b4' : 12.53,
            'exec_b8' : 21.02,
            'exec_b16' : 37.89,
            'output' : 4e-06,
            'post' : 15.89,
        }
    }
)
se_resnext101_32x4d_dag = Dag('se_resnext101_32x4d', funs=[se_resnext101_32x4d])
se_resnext101_32x4d_dag.sanity_check()

se_resnext101_64x4d = Function(
    unique_id='se_resnext101_64x4d',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.011015625,
            'pre' : 28.75,
            'input' : 0.000602,
            'exec_b1' : 8.18,
            'exec_b2' : 12.97,
            'exec_b4' : 19.93,
            'exec_b8' : 34.99,
            'exec_b16' : 66.44,
            'output' : 4e-06,
            'post' : 28.75,
        }
    }
)
se_resnext101_64x4d_dag = Dag('se_resnext101_64x4d', funs=[se_resnext101_64x4d])
se_resnext101_64x4d_dag.sanity_check()

tsn_inceptionv1_kinetics400 = Function(
    unique_id='tsn_inceptionv1_kinetics400',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00075,
            'pre' : 1.96,
            'input' : 0.001073,
            'exec_b1' : 1.95,
            'exec_b2' : 2.76,
            'exec_b4' : 4.44,
            'exec_b8' : 7.51,
            'exec_b16' : 13.43,
            'output' : 1.6000000000000001e-06,
            'post' : 1.96,
        }
    }
)
tsn_inceptionv1_kinetics400_dag = Dag('tsn_inceptionv1_kinetics400', funs=[tsn_inceptionv1_kinetics400])
tsn_inceptionv1_kinetics400_dag.sanity_check()

tsn_inceptionv3_kinetics400 = Function(
    unique_id='tsn_inceptionv3_kinetics400',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0028250000000000003,
            'pre' : 7.37,
            'input' : 0.001073,
            'exec_b1' : 4.47,
            'exec_b2' : 6.87,
            'exec_b4' : 10.97,
            'exec_b8' : 16.43,
            'exec_b16' : 26.12,
            'output' : 1.6000000000000001e-06,
            'post' : 7.37,
        }
    }
)
tsn_inceptionv3_kinetics400_dag = Dag('tsn_inceptionv3_kinetics400', funs=[tsn_inceptionv3_kinetics400])
tsn_inceptionv3_kinetics400_dag.sanity_check()

tsn_resnet18_v1b_kinetics400 = Function(
    unique_id='tsn_resnet18_v1b_kinetics400',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.001421875,
            'pre' : 3.71,
            'input' : 0.000602,
            'exec_b1' : 1.25,
            'exec_b2' : 1.72,
            'exec_b4' : 2.38,
            'exec_b8' : 3.93,
            'exec_b16' : 6.83,
            'output' : 1.6000000000000001e-06,
            'post' : 3.71,
        }
    }
)
tsn_resnet18_v1b_kinetics400_dag = Dag('tsn_resnet18_v1b_kinetics400', funs=[tsn_resnet18_v1b_kinetics400])
tsn_resnet18_v1b_kinetics400_dag.sanity_check()

tsn_resnet34_v1b_kinetics400 = Function(
    unique_id='tsn_resnet34_v1b_kinetics400',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.002684375,
            'pre' : 7.01,
            'input' : 0.000602,
            'exec_b1' : 2.38,
            'exec_b2' : 3.38,
            'exec_b4' : 4.59,
            'exec_b8' : 7.74,
            'exec_b16' : 13.37,
            'output' : 1.6000000000000001e-06,
            'post' : 7.01,
        }
    }
)
tsn_resnet34_v1b_kinetics400_dag = Dag('tsn_resnet34_v1b_kinetics400', funs=[tsn_resnet34_v1b_kinetics400])
tsn_resnet34_v1b_kinetics400_dag.sanity_check()

tsn_resnet50_v1b_kinetics400 = Function(
    unique_id='tsn_resnet50_v1b_kinetics400',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0030375000000000003,
            'pre' : 7.93,
            'input' : 0.000602,
            'exec_b1' : 2.77,
            'exec_b2' : 3.94,
            'exec_b4' : 5.85,
            'exec_b8' : 9.77,
            'exec_b16' : 16.52,
            'output' : 1.6000000000000001e-06,
            'post' : 7.93,
        }
    }
)
tsn_resnet50_v1b_kinetics400_dag = Dag('tsn_resnet50_v1b_kinetics400', funs=[tsn_resnet50_v1b_kinetics400])
tsn_resnet50_v1b_kinetics400_dag.sanity_check()

tsn_resnet101_v1b_kinetics400 = Function(
    unique_id='tsn_resnet101_v1b_kinetics400',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.005409375,
            'pre' : 14.11,
            'input' : 0.000602,
            'exec_b1' : 5.42,
            'exec_b2' : 7.8,
            'exec_b4' : 11.3,
            'exec_b8' : 18.63,
            'exec_b16' : 31.15,
            'output' : 1.6000000000000001e-06,
            'post' : 14.11,
        }
    }
)
tsn_resnet101_v1b_kinetics400_dag = Dag('tsn_resnet101_v1b_kinetics400', funs=[tsn_resnet101_v1b_kinetics400])
tsn_resnet101_v1b_kinetics400_dag.sanity_check()

tsn_resnet152_v1b_kinetics400 = Function(
    unique_id='tsn_resnet152_v1b_kinetics400',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0073625,
            'pre' : 19.21,
            'input' : 0.000602,
            'exec_b1' : 7.87,
            'exec_b2' : 11.35,
            'exec_b4' : 16.42,
            'exec_b8' : 27.07,
            'exec_b16' : 45.44,
            'output' : 1.6000000000000001e-06,
            'post' : 19.21,
        }
    }
)
tsn_resnet152_v1b_kinetics400_dag = Dag('tsn_resnet152_v1b_kinetics400', funs=[tsn_resnet152_v1b_kinetics400])
tsn_resnet152_v1b_kinetics400_dag.sanity_check()

cifar_wideresnet16_10 = Function(
    unique_id='cifar_wideresnet16_10',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.002140625,
            'pre' : 5.59,
            'input' : 1.2e-05,
            'exec_b1' : 1.27,
            'exec_b2' : 1.72,
            'exec_b4' : 2.61,
            'exec_b8' : 4.07,
            'exec_b16' : 7.62,
            'output' : 4e-08,
            'post' : 5.59,
        }
    }
)
cifar_wideresnet16_10_dag = Dag('cifar_wideresnet16_10', funs=[cifar_wideresnet16_10])
cifar_wideresnet16_10_dag.sanity_check()

cifar_wideresnet28_10 = Function(
    unique_id='cifar_wideresnet28_10',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.004559375,
            'pre' : 11.93,
            'input' : 1.2e-05,
            'exec_b1' : 2.21,
            'exec_b2' : 3.57,
            'exec_b4' : 5.42,
            'exec_b8' : 8.41,
            'exec_b16' : 16.05,
            'output' : 4e-08,
            'post' : 11.93,
        }
    }
)
cifar_wideresnet28_10_dag = Dag('cifar_wideresnet28_10', funs=[cifar_wideresnet28_10])
cifar_wideresnet28_10_dag.sanity_check()

cifar_wideresnet40_8 = Function(
    unique_id='cifar_wideresnet40_8',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00446875,
            'pre' : 11.69,
            'input' : 1.2e-05,
            'exec_b1' : 2.49,
            'exec_b2' : 3.9,
            'exec_b4' : 5.99,
            'exec_b8' : 9.86,
            'exec_b16' : 17.14,
            'output' : 4e-08,
            'post' : 11.69,
        }
    }
)
cifar_wideresnet40_8_dag = Dag('cifar_wideresnet40_8', funs=[cifar_wideresnet40_8])
cifar_wideresnet40_8_dag.sanity_check()

winograd_resnet18_v2 = Function(
    unique_id='winograd_resnet18_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.0024187500000000003,
            'pre' : 6.31,
            'input' : 0.000602,
            'exec_b1' : 0.95,
            'exec_b2' : 1.17,
            'exec_b4' : 1.71,
            'exec_b8' : 2.81,
            'exec_b16' : 5.09,
            'output' : 4e-06,
            'post' : 6.31,
        }
    }
)
winograd_resnet18_v2_dag = Dag('winograd_resnet18_v2', funs=[winograd_resnet18_v2])
winograd_resnet18_v2_dag.sanity_check()

winograd_resnet50_v2 = Function(
    unique_id='winograd_resnet50_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.004021874999999999,
            'pre' : 10.49,
            'input' : 0.000602,
            'exec_b1' : 3.39,
            'exec_b2' : 4.24,
            'exec_b4' : 6.07,
            'exec_b8' : 10.28,
            'exec_b16' : 18.84,
            'output' : 4e-06,
            'post' : 10.49,
        }
    }
)
winograd_resnet50_v2_dag = Dag('winograd_resnet50_v2', funs=[winograd_resnet50_v2])
winograd_resnet50_v2_dag.sanity_check()

winograd_resnet101_v2 = Function(
    unique_id='winograd_resnet101_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.00736875,
            'pre' : 19.23,
            'input' : 0.000602,
            'exec_b1' : 6.36,
            'exec_b2' : 7.71,
            'exec_b4' : 10.71,
            'exec_b8' : 17.26,
            'exec_b16' : 33.52,
            'output' : 4e-06,
            'post' : 19.23,
        }
    }
)
winograd_resnet101_v2_dag = Dag('winograd_resnet101_v2', funs=[winograd_resnet101_v2])
winograd_resnet101_v2_dag.sanity_check()

winograd_resnet152_v2 = Function(
    unique_id='winograd_resnet152_v2',
    resources={
        'NVIDIA_TESLA_V100_GPU' : {
            'type' : ResourceType.GPU,
            'space' : 0.010128125,
            'pre' : 26.42,
            'input' : 0.000602,
            'exec_b1' : 9.4,
            'exec_b2' : 11.13,
            'exec_b4' : 15.92,
            'exec_b8' : 24.42,
            'exec_b16' : 28.92,
            'output' : 4e-06,
            'post' : 26.42,
        }
    }
)
winograd_resnet152_v2_dag = Dag('winograd_resnet152_v2', funs=[winograd_resnet152_v2])
winograd_resnet152_v2_dag.sanity_check()

model_zoo = {
    'densenet121' : densenet121,
    'densenet161' : densenet161,
    'densenet169' : densenet169,
    'densenet201' : densenet201,
    'dla34' : dla34,
    'googlenet' : googlenet,
    'inceptionv3' : inceptionv3,
    'xception' : xception,
    'mobile_pose_mobilenet1_0' : mobile_pose_mobilenet1_0,
    'mobile_pose_mobilenetv3' : mobile_pose_mobilenetv3,
    'mobile_pose_resnet18_v1' : mobile_pose_resnet18_v1,
    'mobile_pose_resnet50_v1' : mobile_pose_resnet50_v1,
    'simple_pose_resnet18_v1b' : simple_pose_resnet18_v1b,
    'resnest14' : resnest14,
    'resnest26' : resnest26,
    'resnest50' : resnest50,
    'resnest101' : resnest101,
    'resnet18_v1' : resnet18_v1,
    'resnet18_v1b' : resnet18_v1b,
    'resnet34_v1' : resnet34_v1,
    'resnet34_v1b' : resnet34_v1b,
    'resnet50_v1' : resnet50_v1,
    'resnet50_v1b' : resnet50_v1b,
    'resnet50_v1c' : resnet50_v1c,
    'resnet50_v1d' : resnet50_v1d,
    'resnet50_v1s' : resnet50_v1s,
    'resnet50_tuned_1_8x' : resnet50_tuned_1_8x,
    'resnet101v1' : resnet101v1,
    'resnet101_v1b' : resnet101_v1b,
    'resnet101_v1c' : resnet101_v1c,
    'resnet101_v1d' : resnet101_v1d,
    'resnet101_v1s' : resnet101_v1s,
    'resnet101_tuned_1_9x' : resnet101_tuned_1_9x,
    'resnet101_tuned_2_2x' : resnet101_tuned_2_2x,
    'resnet152_v1' : resnet152_v1,
    'resnet152_v1b' : resnet152_v1b,
    'resnet152_v1c' : resnet152_v1c,
    'resnet152_v1d' : resnet152_v1d,
    'resnet152_v1s' : resnet152_v1s,
    'resnet18_v2' : resnet18_v2,
    'resnet34_v2' : resnet34_v2,
    'resnet50_v2' : resnet50_v2,
    'resnet101_v2' : resnet101_v2,
    'resnet152_v2' : resnet152_v2,
    'resnext50_32x4d' : resnext50_32x4d,
    'resnext101_32x4d' : resnext101_32x4d,
    'resnext101_64x4d' : resnext101_64x4d,
    'se_resnext50_32x4d' : se_resnext50_32x4d,
    'se_resnext101_32x4d' : se_resnext101_32x4d,
    'se_resnext101_64x4d' : se_resnext101_64x4d,
    'tsn_inceptionv1_kinetics400' : tsn_inceptionv1_kinetics400,
    'tsn_inceptionv3_kinetics400' : tsn_inceptionv3_kinetics400,
    'tsn_resnet18_v1b_kinetics400' : tsn_resnet18_v1b_kinetics400,
    'tsn_resnet34_v1b_kinetics400' : tsn_resnet34_v1b_kinetics400,
    'tsn_resnet50_v1b_kinetics400' : tsn_resnet50_v1b_kinetics400,
    'tsn_resnet101_v1b_kinetics400' : tsn_resnet101_v1b_kinetics400,
    'tsn_resnet152_v1b_kinetics400' : tsn_resnet152_v1b_kinetics400,
    'cifar_wideresnet16_10' : cifar_wideresnet16_10,
    'cifar_wideresnet28_10' : cifar_wideresnet28_10,
    'cifar_wideresnet40_8' : cifar_wideresnet40_8,
    'winograd_resnet18_v2' : winograd_resnet18_v2,
    'winograd_resnet50_v2' : winograd_resnet50_v2,
    'winograd_resnet101_v2' : winograd_resnet101_v2,
    'winograd_resnet152_v2' : winograd_resnet152_v2,
}
