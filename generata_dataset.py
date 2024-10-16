import subprocess

def run_workers(num_instances):
    processes = []

    # Example configuration and output file names
    configs = [f"configs/360_Multi.yaml" for _ in range(num_instances)]  # Same config for all instances
    outputs = [f"data/{i}" for i in range(num_instances)]  # Unique output paths for each instance

    # Start multiple worker instances
    for i in range(num_instances):
        # Create a subprocess for each worker with its respective config and output file
        process = subprocess.Popen(['python3', 'render.py', '--config', configs[i], '--outf', outputs[i]])
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.wait()

if __name__ == "__main__":
    # Specify the number of worker instances to run
    num_instances = 2  # Adjust this number as needed
    run_workers(num_instances)

