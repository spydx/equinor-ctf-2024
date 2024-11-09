import os
import subprocess
import time
import datetime

# Define the specific week in September 2024
start_date = datetime.datetime(2024, 9, 15)  # Start of September
# Adjust to the specific week
week_start = start_date  # Second week of September
week_end = week_start + datetime.timedelta(days=7)

# Generate timestamps within that week
timestamps = []
current_date = week_start
while current_date < week_end:
    timestamps.append(int(current_date.timestamp()))
    current_date += datetime.timedelta(seconds=1)

# Iterate over possible ITER values
for timestamp in timestamps:
    iter_value = timestamp // 1000000  # Calculate ITER based on timestamp
    env = os.environ.copy()
    env['ITER'] = str(iter_value)

    # Prepare OpenSSL decryption command
    command = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-iter", str(iter_value), "-in", "enc.enc", "-k", "ubuntu-s-1vcpu-512mb-10gb-ams3-01", "-a"
    ]

    # Run the command and capture the output
    try:
        output = subprocess.check_output(command, env=env, stderr=subprocess.DEVNULL)
        print(f"Success with ITER = {iter_value}")
        print("Decrypted content:", output.decode('utf-8'))
        break  # Stop if the correct ITER value is found
    except subprocess.CalledProcessError:
        # Continue if decryption fails
        continue
