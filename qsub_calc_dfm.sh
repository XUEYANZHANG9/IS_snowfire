#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q@compute-0-1,default.q@compute-0-17.local,default.q@compute-0-18.local,default.q@compute-0-19.local,default.q@compute-0-2,default.q@compute-2-3 
#$ -N canesm_45
#$ -p -5 

# which python 
source /home/gergel/.bashrc 
source activate /home/gergel/anaconda/envs/my_env 

# default.q@compute-0-17.local,default.q@compute-0-18.local,default.q@compute-0-19.local,default.q@compute-0-0.local,default.q@compute-0-2.local


#python /raid9/gergel/agg_snowpack/calc_dfm_gridcell_is.py $model $scenario $lat $lon

direc="/state/partition1"
#direc="/fast/gergel" 

cp /raid/gergel/rh/${model}_${scenario}_huss.nc ${direc}
cp /raid/gergel/tmax/${model}_${scenario}_tasmax.nc ${direc}
cp /raid/gergel/tmin/${model}_${scenario}_tasmin.nc ${direc}
cp /raid/gergel/pptdur/${model}_${scenario}.nc ${direc}

python /raid9/gergel/agg_snowpack/calc_dfm_is.py $chunk $model $scenario 

if [ "historical" = "$scenario" ]
        then
	chunk="1970_1999"
elif [ "chunk1" = "$chunk" ] 
	then
	chunk="2010_2039"
elif [ "chunk2" = "$chunk" ]
	then 
	chunk="2040_2069"
else 
	chunk="2070_2099"
fi
 
cp ${direc}/${model}_${scenario}_${chunk}.nc /raid/gergel/dfm/

rm ${direc}/${model}_${scenario}_huss.nc
rm ${direc}/${model}_${scenario}_tasmax.nc
rm ${direc}/${model}_${scenario}_tasmin.nc
rm ${direc}/${model}_${scenario}.nc
rm ${direc}/${model}_${scenario}_${chunk}.nc
