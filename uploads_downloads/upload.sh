#!/bin/bash

upload_folder="./upload_folder"
file_path="$upload_folder/test.jpg"


curl -X POST -F "file=@$file_path" http://192.168.1.118:5004/upload