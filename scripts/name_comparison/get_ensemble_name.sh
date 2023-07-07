#!/bin/bash

curl -l ftp://ftp.ensemblgenomes.org/pub/bacteria/release-56/fasta/bacteria_{0..128}_collection/*.dna.toplevel.fa.gz | awk -F'/' '{ print $NF }' | awk -F'.' '{ print $1 }' > ensemble_name.csv
