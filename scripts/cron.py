'''
This script processes a Salesforce Change Data Capture payload received via stdin.
It checks if the commitTimestamp falls within a specified period and executes a specified command if it does.
The script runs on a loop using the schedule library, acting like a cron job.

Usage:
python cron_job.py -u <username> -p <period> -i <interval> -c <command>

Arguments:
- username: Your Salesforce username.
- period: Time period in minutes.
- interval: Interval in minutes for scheduling the task.
- command: Command to execute when conditions are met.
'''

import sys
import json
import subprocess
import argparse
from datetime import datetime, timedelta
import schedule
import time

def process_payload(username, period, command):
    # Read JSON payload from stdin
    try:
        payload = json.loads(input())
        print(payload)
    except EOFError:
        print("waiting...")
        return

    # Extract commitTimestamp from payload
    commit_timestamp = datetime.utcfromtimestamp(payload["payload"]["ChangeEventHeader"]["commitTimestamp"] / 1000)

    # Calculate time period
    period_delta = timedelta(minutes=period)

    # Check if commitTimestamp is within the given period
    if datetime.utcnow() - commit_timestamp <= period_delta:
        # Execute the specified command
        subprocess.run(command, shell=True)
    else:
        print("commitTimestamp is not within the given period")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process Salesforce Change Data Capture payload")
    parser.add_argument("-u", "--username", help="Salesforce username", required=True)
    parser.add_argument("-p", "--period", help="Time period in minutes", type=int, required=True)
    parser.add_argument("-i", "--interval", help="Interval in minutes for scheduling the task", type=int, default=1)
    parser.add_argument("-c", "--command", help="Command to execute when conditions are met", required=True)
    args = parser.parse_args()

    # Schedule the task to run at the specified interval
    schedule.every(args.interval).minutes.do(process_payload, args.username, args.period, args.command)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
