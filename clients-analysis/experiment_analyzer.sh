#! /bin/bash

mkdir .tmp_exp_analyzer

EXPFILE=$1
ATTACK=$2
POSTATTACK=$3

echo "Extracting $EXPFILE"

tar -zxf $EXPFILE -C .tmp_exp_analyzer --wildcards '*client*'
ls .tmp_exp_analyzer/

echo "Extracted $EXPFILE"

echo "Running experiment analyzer..."
cd .tmp_exp_analyzer
for f in *.tar; do tar -xf "$f"; [ -f client_delay.csv ] && mv client_delay.csv ${f}.csv; done

cd ..

python3 client_metrics.py .tmp_exp_analyzer -a $ATTACK -p $POSTATTACK

echo "Experiment analyzer finished"
rm -rf .tmp_exp_analyzer