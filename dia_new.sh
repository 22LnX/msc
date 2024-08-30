#!/bin/bash

#SBATCH --partition=medium
#SBATCH --output=job_example_%A_%a.out
#SBATCH --error=job_example_%A_%a.err
#SBATCH --mem=100G
#SBATCH --cpus-per-task=8
#SBATCH --array=0-5

# Activate the conda environment
source activate diamond

# Define the base directory containing all barcode directories
BASE_DIR="/mnt/shared/home/lxu/sample_data/WeeklyGardenSampling/run-9/fasta_chunks"

# Get the list of barcode directories
BARCODE_DIRS=($(ls -d "$BASE_DIR"/barcode*))

# Get the current barcode directory based on the SLURM array task ID
DIR=${BARCODE_DIRS[$SLURM_ARRAY_TASK_ID]}

if [ -d "$DIR" ]; then
    # Extract barcode identifier
    BARCODE=$(basename "$DIR")

    # Combine all .fasta files in the current barcode directory
    cat "$DIR"/*.fasta > "$DIR"/reads.fna

    # Define the output file with run and barcode information
    OUTPUT_FILE="$DIR/run-9_${BARCODE}_matches.m8"

    # Run DIAMOND blastx with the specified output format
    diamond blastx -d /mnt/shared/apps/databases/diamond/nr.dmnd -q "$DIR"/reads.fna -o "$OUTPUT_FILE" \
                   -f 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle staxids salltitles sscinames sskingdoms skingdoms sphylums
fi


