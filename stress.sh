#!/bin/bash

function test_lines {
    # 10 columns
    for x in $(seq $2 $4 $3)
    do
        ./stress.py generate ".stress/$x.krn" 10 $x
        thetime=$(/usr/bin/time -f "%e" ./stress.py $1 ".stress/$x.krn" 2>&1 >/dev/null)
        echo $thetime, $x, $1
    done
}

function test_columns {
    for x in $(seq $2 $4 $3)
    do
        ./stress.py generate ".stress/$x.krn" $x $5
        thetime=$(/usr/bin/time -f "%e" ./stress.py $1 ".stress/$x.krn" 2>&1 >/dev/null)
        echo $thetime, $x, $1
    done
}

# fn, from, to, step
test_lines parse 10 1000 10
test_lines emit 10 1000 10

# fn, from, to, step, line_number
test_columns parse 10 1000 10 10
test_columns emit 10 1000 10 10
