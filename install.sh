#!/bin/bash

version=$(python3 --version 2>&1) && awk -F. -v ver="$version" '{ if ($1 >= 3 && $2 >= 8) print "Found Python version: " ver; else { print "Python 3.8+ is required. Please install Python 3.8 or newer."; exit 1 } }' <<<"$version"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Writing a Flask secret key to the config file..."
python create_files.py

if [ -n "$1" ]; then
    user_id_arg="--user_id $1"
    echo "Using existing user with id: $1..."
else
    user_id_arg=""
    echo "Creating a new user..."
fi

output=$(python token_manager.py create-user $user_id_arg)
#echo "$output"

if echo "$output" | grep -q "has been created with default token"; then
    user_id=$user_id_arg
    token=$(echo "$output" | grep -oP 'default token: \K[a-fA-F0-9]+')
    #echo "Extracted token (new user): $token"
else
    user_id=$(echo "$output" | grep -oP 'User with ID \K\d+')
    tokens_output=$(python token_manager.py list-tokens "$user_id")
    #echo "$tokens_output"
    token=$(echo "$tokens_output" | grep -oP "^- \K[a-fA-F0-9]+")
    #echo "Extracted token (existing user): $token"
fi
echo "Using token: $token for user with id: $user_id"
echo "Creating userscript and config file..."

python create_files.py --token "$token"
