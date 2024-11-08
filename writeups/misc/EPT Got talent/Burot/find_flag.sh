!/bin/bash

echo "searching for hidden files"

sudo find / -type f -name ".secret"

if [ $? -ne 0 ]; then
	echo "No .secret file was found"
else
	echo "The .secret file was found"
fi