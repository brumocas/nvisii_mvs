# Use an official Ubuntu as the base image
FROM ubuntu:18.04

# Set environment variables to prevent prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.6 \
    python3.6-venv \
    python3.6-dev \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python3.6 as the default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1

# Upgrade pip to the latest version
RUN python3.6 -m pip install --upgrade pip

# Verify the Python and pip versions
RUN python3 --version && pip3 --version

# Set the working directory
WORKDIR /workspace/

# Clone nvisii repository
RUN git clone https://github.com/TontonTremblay/nvisii_mvs.git

# Optional: Set default command to open a shell in the workspace
CMD ["/bin/bash"]
