#!/bin/bash

# Set your FLAG value here
FLAG="your_flag_value_here"

# Write the FLAG value to /flag
echo "$FLAG" > /flag
chmod 600 /flag

# Unset the FLAG variable
unset FLAG

# Set the CAP_SETFCAP capability for mariadb
setcap CAP_SETFCAP=ep /usr/bin/mariadb

# Start the MySQL server
/mysql.sh &

# Start Apache
apache2ctl start

echo "start.sh finished"
