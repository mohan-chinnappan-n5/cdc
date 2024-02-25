'''
This script processes a Salesforce Change Data Capture payload received via stdin.
It checks if the commitTimestamp falls within a specified period and executes a Salesforce CLI command if it does.
The script runs on a loop using the schedule library, acting like a cron job.

Author: Mohan Chinnappan
------------------------------------------------------------------------------

Usage:
 python cron_job.py -u <username> -p <period> -i <interval>

 Example:
  sf mohanc streaming sub -u  mohan.chinnappan.n.ea10@gmail.com  -t  /data/Distributor__ChangeEvent | python3 ~/cdc/scripts/cron_job.py -u mohan.chinnappan.n.ea10@gmail.com   -p 30 -i 1



Arguments:
- username: Your Salesforce username.
- period: Time period in minutes.
- interval: Interval in minutes for scheduling the task.
------------------------------------------------------------------------------
'''

import sys
import json
import subprocess
import argparse
from datetime import datetime, timedelta
import schedule
import time

def process_payload(username, period):
    # Read JSON payload from stdin
    payload = json.load(sys.stdin)

    print (payload)

    # Extract commitTimestamp from payload
    commit_timestamp = datetime.utcfromtimestamp(payload["payload"]["ChangeEventHeader"]["commitTimestamp"] / 1000)

    # Calculate time period
    period_delta = timedelta(minutes=period)

    print (f"current time: {datetime.utcnow()}\ncommit_timestamp: {commit_timestamp}\n range {datetime.utcnow() - commit_timestamp }")

    # Check if commitTimestamp is within the given period
    if datetime.utcnow() - commit_timestamp <= period_delta:
        # Execute the specified command
        print ('=== Going to run the command to start the recipe ===')
        command = ["sf", "mohanc", "ea", "recipe", "list", "-u", username]
        subprocess.run(command)
    else:
        print("commitTimestamp is not within the given period")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process Salesforce Change Data Capture payload")
    parser.add_argument("-u", "--username", help="Salesforce username", required=True)
    parser.add_argument("-p", "--period", help="Time period in minutes", type=int, required=True)
    parser.add_argument("-i", "--interval", help="Interval in minutes for scheduling the task", type=int, default=1)
    args = parser.parse_args()

    # Schedule the task to run at the specified interval
    schedule.every(args.interval).minutes.do(process_payload, args.username, args.period)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
