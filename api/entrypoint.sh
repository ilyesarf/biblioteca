#!/bin/bash

# Wait for the backend service to be ready
/wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is ready"
/wait-for-it.sh nanolock:50051 --timeout=60 --strict -- echo "NanoLock is ready"

# Start the API server
exec python3 web.py
