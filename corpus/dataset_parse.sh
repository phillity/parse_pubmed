#!/bin/bash

dataset=$1
thread=$2

total_lines=$(wc -l <"corpus/"${dataset}".tsv")
((lines_per_file = (total_lines + $thread - 1) / $thread))
split -d --lines=${lines_per_file} "corpus/"${dataset}".tsv" --additional-suffix=.tsv "corpus/"$dataset"_"

for i in $(seq -f "%02g" 0 $(($thread - 1)))
do
  ( python3 corpus/dataset_parse.py -i $dataset"_"$i".tsv" ) &
done
wait

cat "corpus/"$dataset"_ce_"**"_pos.tsv" > "corpus/"$dataset"_ce_pos.tsv"
cat "corpus/"$dataset"_ce_"**"_neg.tsv" > "corpus/"$dataset"_ce_neg.tsv"
cat "corpus/"$dataset"_hyp_"**"_pos.tsv" > "corpus/"$dataset"_hyp_pos.tsv"
cat "corpus/"$dataset"_hyp_"**"_neg.tsv" > "corpus/"$dataset"_hyp_neg.tsv"
cat "corpus/"$dataset"_me_"**"_pos.tsv" > "corpus/"$dataset"_me_pos.tsv"
cat "corpus/"$dataset"_me_"**"_neg.tsv" > "corpus/"$dataset"_me_neg.tsv"

for i in $(seq -f "%02g" 0 $(($thread - 1)))
do
  rm "corpus/"$dataset"_"$i"_ce_pos.tsv"
  rm "corpus/"$dataset"_"$i"_ce_neg.tsv"
  rm "corpus/"$dataset"_"$i"_hyp_pos.tsv"
  rm "corpus/"$dataset"_"$i"_hyp_neg.tsv"
  rm "corpus/"$dataset"_"$i"_me_pos.tsv"
  rm "corpus/"$dataset"_"$i"_me_neg.tsv"
  rm "corpus/"$dataset"_"$i".tsv"
done
