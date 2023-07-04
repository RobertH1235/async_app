#!/bin/bash

# Number of concurrent downloads
num_downloads=1024

# Filename to download
filename="test.jpg"

# Download URL
download_url="http://192.168.1.118:5003/download/$filename"

# Folder to save the downloaded files
download_folder="./download_folder"

# Folder to save the timing information
timing_folder="./timing_folder"

# Log file to store the download logs
log_file="$timing_folder/download_logs.txt"

# Create the download and timing folders if they don't exist
mkdir -p "$download_folder"
mkdir -p "$timing_folder"

# Function to download a file and measure the time
download_file() {
  start_time=$(date +%s.%N)
  curl -o "$download_folder/$filename.$1" "$download_url"
  end_time=$(date +%s.%N)
  elapsed_time=$(bc <<< "$end_time - $start_time")
  echo "File $1: Started at $(date -d @$start_time +'%H:%M:%S'), Finished at $(date -d @$end_time +'%H:%M:%S'), Elapsed time: $elapsed_time seconds" >> "$log_file"
}

# Start the loop
for ((i=1; i<=$num_downloads; i++))
do
  # Download the file in the background and measure the time
  download_file $i &
done

# Wait for all background processes to finish
wait
