BASEDIR=$(dirname "$0")
pushd .
cd $BASEDIR

# Clean the current state to make sure the code runs again
#   Note:   1. This is done just as part of the example
#           2. It can done by appending "--cs" to the "ssm shell" command below
ssm data -p ssm-ex -t ex1 --cs
# Run the task
ssm shell -p ssm-ex -t ex1 -o ./out1 --it ml.p3.2xlarge --cmd_line "cat /proc/cpuinfo && nvidia-smi"

cat ./out1/logs/logs0

popd