import subprocess
import time

def run_workers(num_instances):
    processes = []
    configs = [f"configs/360_Multi.yaml" for _ in range(num_instances)]  # Same config for all instances
    folder_counter = 0  # Global counter to keep track of unique folder numbers

    while True:  # Infinite loop to keep relaunching processes
        for i in range(num_instances):
            if i >= len(processes) or processes[i].poll() is not None:
                # If the process has finished (poll() returns None if it's running), restart it
                output_folder = f"data/{folder_counter}"
                print(f"Starting or restarting worker {i} with output folder {output_folder}")
                
                # Launch a new process with the incremented folder number
                process = subprocess.Popen(['python3', 'render.py', '--config', configs[i], '--outf', output_folder])
                
                if i < len(processes):
                    processes[i] = process  # Update existing process slot
                else:
                    processes.append(process)  # Append new process if it's the first run
                
                # Increment the folder counter for the next output
                folder_counter += 1

        # Sleep for a short interval to avoid busy-waiting
        time.sleep(1)

if __name__ == "__main__":
    num_instances = 1  # Adjust this number as needed
    run_workers(num_instances)