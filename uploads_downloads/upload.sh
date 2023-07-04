#!/bin/bash

upload_folder="./upload_folder"
file_path="$upload_folder/1GB.png"


curl -X POST -F "file=@$file_path" http://192.168.1.118:5002/upload