#!/bin/bash

# Number of CPU cores to use
CORES=20

# Function to fix a single directory
fix_directory() {
    local dir="$1"
    if [ -d "$dir/$dir" ]; then
        echo "Fixing $dir"
        # Move all contents from inner directory to outer directory
        mv "$dir/$dir"/* "$dir/"
        # Remove the now-empty inner directory
        rmdir "$dir/$dir"
    fi
}

export -f fix_directory

# Navigate to the dataset directory
cd data/caxton_dataset

echo "Starting directory fix process with $CORES cores..."

# Use find to get all directories and pipe to parallel
# The -j option specifies the number of jobs to run simultaneously
find . -maxdepth 1 -type d -name "print*" | parallel -j$CORES fix_directory

echo "Directory structure fixed."

echo "Process completed."