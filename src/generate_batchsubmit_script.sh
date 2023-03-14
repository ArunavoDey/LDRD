#!/bin/bash

bank=$1
num_node=$2
num_proc=$3
epoch=$4
trial=$5  ## It only used during training
appname=$6
phase=$7 #train source-only linear_probing fine_tuning stacked kregressor random_forest
target=$8 #runtime etc.
queue=$9
tlimit=${10}
train_test_split=${11}
validation_split=${12}
frozen_layer=${13}
db="sqlite:///dbs/MG.db"
output="submit_${appname}_${phase}_e${epoch}_tt${train_test_split}_tv${validation_split}_fl${frozen_layer}.sub"

echo "#!/bin/bash" > $output
echo "#SBATCH -A $bank" >> $output
echo "#SBATCH -J $output" >> $output          
echo "#SBATCH -o $output.o%j" >> $output
echo "#SBATCH -e $output.e%j" >> $output
echo "#SBATCH -p $queue" >> $output
echo "#SBATCH -N $num_node" >> $output
echo "#SBATCH -n $num_proc" >> $output
echo "#SBATCH -t $tlimit" >> $output
echo "date" >> $output
echo "source ../../../dev/bin/activate" >> $output


## Remove percent from experiment.py file.
percent=0.1
## frozen_layer only applies to linear probing.
cmd="srun -N $num_node -n $num_proc python3 experiment.py $epoch $trial $appname $db $percent /results/ $appname $phase /data/${appname}/src/ /data/${appname}/tar/ /results/ /models/ /chckpoints/ $target ${train_test_split} ${validation_split} 42 84 ${frozen_layer}"
echo $cmd >> $output
echo "$cmd" >> experiment.log
squeue $output >> experiment.log
