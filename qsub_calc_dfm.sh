#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q@compute-0-17.local,default.q@compute-0-18.local,default.q@compute-0-19.local,default.q@compute-0-0.local,default.q@compute-0-2.local
#$ -N dfm
#$ -p -5 

# which python 
source /home/gergel/.bashrc 
source activate /home/gergel/anaconda/envs/my_env 

#python /raid9/gergel/agg_snowpack/calc_dfm_gridcell_is.py $model $scenario $lat $lon

cp /raid/gergel/rh/${model}_${scenario}_huss.nc /fast/gergel
cp /raid/gergel/tmax/${model}_${scenario}_tasmax.nc /fast/gergel
cp /raid/gergel/tmin/${model}_${scenario}_tasmin.nc /fast/gergel
cp /raid/gergel/pptdur/${model}_${scenario}.nc /fast/gergel

python /raid9/gergel/agg_snowpack/calc_dfm_is.py $chunk $model $scenario

cp /fast/gergel/${model}_${scenario}.nc /raid/gergel/dfm/${model}_${scenario}.nc 

rm /fast/gergel/${model}_${scenario}.nc
rm /fast/gergel/${model}_${scenario}_huss.nc
rm /fast/gergel/${model}_${scenario}_tasmax.nc
rm /fast/gergel/${model}_${scenario}_tasmin.nc
rm /fast/gergel/${model}_${scenario}.nc
