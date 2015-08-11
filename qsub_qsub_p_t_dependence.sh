#!/bin/bash 

basins="cascades california northernrockies southernrockies whites"
scenarios="historical rcp45 rcp85"

# basins="northernrockies"
# scenarios="rcp45"

### loop over basins
for basin in $basins 
do 
	for scenario in $scenarios
	do
		echo "processing $basin $scenario" 
		qsub -v basin=$basin,scenario=$scenario qsub_p_t_dependence.sh 
	done
done 
