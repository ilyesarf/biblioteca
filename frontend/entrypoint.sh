#!/bin/bash

# Wait for the backend service to be ready
/wait-for-it.sh api:8000 --timeout=60 --strict -- echo "API is ready"

# Start Nginx
exec nginx -g 'daemon off;'
