#!/bin/bash

mkdir data
#for i in $(seq 1000 1000 10000)
#do
   #python3 creating_random_network.py $i $i nodos

#done

#for i in $(seq 20000 10000 100000)
#do
   #python3 creating_random_network.py $i $i nodos

#done

for i in $(seq 150000 50000 1000000)
do
   python3 creating_random_network.py $i $i nodos

done
