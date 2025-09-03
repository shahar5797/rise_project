# File: start.sh

#!/bin/bash

docker-compose up  --build &

# Wait until the server is responding
while ! curl -s http://localhost:5050 >/dev/null; do
  echo "⏳ Waiting for server..."
  sleep 1
done

# Open the browser
# xdg-open http://localhost:5050 &  # Linux
open http://localhost:5050 &    # macOS
# start http://localhost:5050     # Windows Git Bash