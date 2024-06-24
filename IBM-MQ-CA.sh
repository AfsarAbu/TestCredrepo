#!/bin/bash

# Function to check MQ attributes
check_mq_attributes() {
    # Get the Queue Manager name, Queue name, Channel name, Host, Port, User, and Password as arguments
    local qmgr_name=$1
    local queue_name=$2
    local channel=$3
    local host=$4
    local port=$5
    local user=$6
    local password=$7

    # Create a temporary file to store MQSC commands and results
    mqsc_file=$(mktemp)

    # Check Queue Manager attributes
    echo "DIS QMGR PERFMEV" > $mqsc_file

    # Check Queue attributes
    echo "DIS QLOCAL($queue_name) QDPHIEV" >> $mqsc_file

    # Connect to the Queue Manager and run the commands
    runmqsc -c -x "$qmgr_name" < $mqsc_file | tee mqsc_output.txt

    # Parse the output
    perfmev=$(grep -A 1 "PERFMEV" mqsc_output.txt | tail -n 1 | awk '{print $2}')
    qdphiev=$(grep -A 1 "QDPHIEV" mqsc_output.txt | tail -n 1 | awk '{print $2}')

    # Display the results
    echo "PERFMEV (Queue Manager Performance Events): $perfmev"
    echo "QDPHIEV (Queue Depth High Event): $qdphiev"

    # Clean up
    rm $mqsc_file mqsc_output.txt
}

# Get configuration parameters from user input
read -p "Enter the Queue Manager name: " qmgr_name
read -p "Enter the Queue name: " queue_name
read -p "Enter the Channel name (mandatory for connection): " channel  # Example: APP.SVRCONN
read -p "Enter the Host: " host
read -p "Enter the Port: " port
read -p "Enter the User: " user
read -s -p "Enter the Password: " password
echo ""

# Check the MQ attributes using the provided configuration
check_mq_attributes "$qmgr_name" "$queue_name" "$channel" "$host" "$port" "$user" "$password"
