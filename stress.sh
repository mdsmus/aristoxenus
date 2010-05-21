#!/bin/bash

function test_lines {
    # 10 columns
    for x in $(seq $2 $4 $3)
    do
        ./stress.py generate ".stress/$x.krn" 10 $x
        thetime=$(/usr/bin/time -f "%e" ./stress.py $1 ".stress/$x.krn" 2>&1 >/dev/null)
        echo $thetime, $x, $1, lines
    done
}

function test_columns {
    for x in $(seq $2 $4 $3)
    do
        ./stress.py generate ".stress/$x.krn" $x $5
        thetime=$(/usr/bin/time -f "%e" ./stress.py $1 ".stress/$x.krn" 2>&1 >/dev/null)
        echo $thetime, $x, $1, columns
    done
}

function test_max {
# fn, line, col
    ./stress.py generate ".stress/max.krn" $2 $3
    thetime=$(/usr/bin/time -f "%e" ./stress.py $1 ".stress/max.krn" 2>&1 >/dev/null)
    echo $thetime, $2, $3, $1, max
}

function basic_tests {
# # fn, from, to, step
    test_lines parse 10 1000 10
    test_lines emit 10 1000 10

# # fn, from, to, step, line_number
    test_columns parse 10 1000 10 10
    test_columns emit 10 1000 10 10
}

function long_test {
    test_max parse 10000 2000
}

if [ "$1" != "" ]
then
    case "$1" in
        basic)  basic_tests ;;
        long)   long_test ;;
        *) echo "command not found" ; exit ;;
    esac

else
    echo "usage: stress <basic|long>"
fi
