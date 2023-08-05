import logging
import os
import shutil
import sys
from time import gmtime, strftime

logger = logging.getLogger(__name__)

file_path = os.path.split(__file__)[0]
if "TOX_ENV_NAME" not in os.environ:
    srcPath = os.path.abspath(os.path.join(file_path, "..", "..", "src"))
    sys.path.append(srcPath)
from simple_sagemaker.sm_project import SageMakerProject  # noqa: E402


def setDefaultParams(sm_project):
    # docker image params
    aws_repo_name = "task_repo"  # remote (ECR) rpository name
    repo_name = "task_repo"  # local repository name
    image_tag = "latest"  # tag for local & remote images
    docker_file_path = os.path.join(file_path, "docker")  # path of the local Dockerfile
    sm_project.setDefaultImageParams(
        aws_repo_name, repo_name, image_tag, docker_file_path
    )

    # job code path, entrypoint and params
    source_dir = os.path.join(file_path, "code")
    entry_point = "algo.py"
    dependencies = [os.path.join(file_path, "external_dependency")]
    sm_project.setDefaultCodeParams(source_dir, entry_point, dependencies)

    # instances type an count
    instance_type = "ml.m5.large"
    training_instance_count = 2
    volume_size = (
        30  # Size in GB of the EBS volume to use for storing input data during training
    )
    use_spot_instances = True  # False
    max_run_mins = 15
    sm_project.setDefaultInstanceParams(
        instance_type,
        training_instance_count,
        volume_size,
        use_spot_instances,
        max_run_mins,
    )


def buildImage(sm_project, fallback_uri=None):
    try:
        # build a local image
        image_uri = sm_project.buildOrGetImage(
            instance_type=sm_project.defaultInstanceParams.instance_type
        )
        # use an AWS pre-built image
        # image_uri = "763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:1.6.0-cpu-py3"
    except:  # noqa: E722
        logger.exception("Couldn't build image")
        if not fallback_uri:
            raise
        logger.info(f"falling back to {fallback_uri}")
        # for debugging whe're
        image_uri = fallback_uri

    return image_uri


def runner(
    project_name="simple-sagemaker-example", prefix="", postfix="", output_path=None
):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    sm_project = SageMakerProject(prefix + project_name + postfix)

    setDefaultParams(sm_project)
    image_uri = buildImage(
        sm_project, "667232328135.dkr.ecr.us-east-1.amazonaws.com/task_repo:latest"
    )

    # task name
    task_name = (
        "Task1"  # must satisfy regular expression pattern: ^[a-zA-Z0-9](-*[a-zA-Z0-9])*
    )
    # input data params
    input_data_path = os.path.join(
        file_path, "input_data"
    )  # Can also provide a URI to an S3 bucket, e.g. next commented line
    # input_data_path = sagemaker.s3.s3_path_join("s3://", "sagemaker-us-east-1-667232328135", "task3", "input")
    distribution = "ShardedByS3Key"  # or "FullyReplicated" which is the default
    model_uri = (
        None  # Can be used to supply model data as an additional input, local/s3
    )
    hyperparameters = {"arg1": 5, "arg2": "hello"}

    sm_project.runTask(
        task_name,
        image_uri,
        hyperparameters,
        input_data_path,
        model_uri=model_uri,
        input_distribution=distribution,
        clean_state=True,
    )

    # delete the output directory
    if not output_path:
        output_path = os.path.join(file_path, "output")
    shutil.rmtree(output_path, ignore_errors=True)
    sm_project.downloadResults(task_name, output_path)

    return sm_project


if __name__ == "__main__":
    py_version_string = f"py{sys.version_info.major}{sys.version_info.minor}"
    time_string = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    sm_project = runner(postfix=f"_{time_string}_{py_version_string}", prefix="tests/")
