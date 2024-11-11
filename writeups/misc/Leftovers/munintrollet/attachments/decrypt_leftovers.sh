#!/bin/bash

# File containing the encrypted content
ENCRYPTED_OUTPUT="./encrypted.txt"

# Set the "Printed Worked" Directory, or PWD, retrived from the log file
PWD="ubuntu-s-1vcpu-512mb-10gb-ams3-01"

# Array of the dates representing every day in week 38 2024 (Sept 16 - Sept 22)
DATES=("2024-09-16" "2024-09-17" "2024-09-18" "2024-09-19" "2024-09-20" "2024-09-21" "2024-09-22")

# Loop through each date and calculate ITER
for DATE in "${DATES[@]}"; do
  ITER=$(($(date -d "$DATE" +%s) / 1000000))
  echo "Trying with ITER=$ITER for date $DATE"

  # Attempt decryption
  DECRYPTED_OUTPUT=$(openssl enc -aes-256-cbc -pbkdf2 -iter $ITER -d -in $ENCRYPTED_OUTPUT -k "$PWD" -a 2>&1)

  # Check if decryption command was successful
  if [[ $? -eq 0 && -n "$DECRYPTED_OUTPUT" ]]; then
    echo "Decryption successful for ITER=$ITER on $DATE"
    echo "Decrypted content:"
    echo "$DECRYPTED_OUTPUT"
    exit 0 
  fi
done

echo "Decryption failed for all possible ITER values in week 38 of September 2024."
