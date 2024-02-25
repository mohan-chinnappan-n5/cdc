'''
This script reads a JSON file containing a command and runs it with specified parameters.
It runs on a loop using the schedule library, acting like a cron job.

Author: Mohan Chinnappan
Usage:
python simple_scheduler.py -p <period> -i <interval> -f <file_path>

Arguments:
- interval: Interval in minutes for scheduling the task.
- file_path: Path to the JSON file containing the command to execute.
'''

import json
import subprocess
import argparse
import schedule
import time

def run_command( interval, file_path):
    # Read command from JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
        command = data.get("command")

    # Schedule the task to run at the specified interval
    schedule.every(interval).minutes.do(subprocess.run, command.split(), shell=True)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run a command on a schedule")
    parser.add_argument("-i", "--interval", help="Interval in minutes for scheduling the task", type=int, default=1)
    parser.add_argument("-f", "--file_path", help="Path to the JSON file containing the command", required=True)
    args = parser.parse_args()

    # Run the command on a schedule
    run_command(args.interval, args.file_path)

if __name__ == "__main__":
    main()
