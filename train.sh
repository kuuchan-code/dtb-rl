#!/bin/bash

max=1000

for ((i=0; i<$max; i++)) do
    ./train.py
done
