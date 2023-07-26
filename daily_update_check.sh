#!/bin/bash

# The base URL for the HTTP request
BASE_URL="http://example.com/check_update?project="

# The location of your project
PROJECT_DIR="/var/www/content-site"

# Change to the project directory
cd $PROJECT_DIR

# The location of the log file
LOG_FILE="/path/to/log.txt"

# Function to log errors
function log_error() {
    echo "$(date) [ERROR]: $1" >> $LOG_FILE
}

# Function to log information
function log_info() {
    echo "$(date) [INFO]: $1" >> $LOG_FILE
}

# Get the content site variable from the config.py file
CONTENT_SITE=$(python -c "from config import content_site; print(content_site)")

# Create the URL for the HTTP request
URL="${BASE_URL}${CONTENT_SITE}"

# Send the HTTP request and store the response
RESPONSE=$(curl -s --fail $URL)

# Check if the curl command was successful
if [[ $? -ne 0 ]]; then
    log_error "Failed to fetch data from $URL. Is the server down?"
    exit 1
fi

# Check if the expected parameter is in the response
if ! echo "$RESPONSE" | grep -q "update_required"; then
    log_error "The expected parameter was not found in the server's response. Is the server working correctly?"
    exit 1
fi

# Check if an update is required
if echo "$RESPONSE" | grep -q "update_required = True"; then
    # If an update is required, run a git pull
    log_info "Update required, updating..."
    if ! git pull origin master; then
        log_error "Failed to update the project from GitHub. Is the repo accessible?"
        exit 1
    fi
    log_info "Update completed successfully."
else
    log_info "No update required."
fi


