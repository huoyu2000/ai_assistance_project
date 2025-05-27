#!/bin/bash

set -x

echo "--- start.sh (Ultra Simple Test v1) IS RUNNING ---"
echo "This is a test to see if Procfile's web command executes this script."
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

echo "Environment variables:"
printenv

echo "Script will now sleep for 300 seconds to keep the container alive for inspection if needed."
sleep 300

echo "--- start.sh (Ultra Simple Test v1) FINISHED ---"
exit 0 