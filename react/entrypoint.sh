#!/bin/sh

# Write env.js based on environment variable
cat <<EOF > /usr/share/nginx/html/env.js
window.REACT_APP_API_URL="${REACT_APP_API_URL}";
EOF

# Start nginx
nginx -g "daemon off;"
