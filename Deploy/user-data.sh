#!/bin/bash
echo 'Hello Yasmin!' > /home/ec2-user/hello.txt
chown ec2-user:ec2-user /home/ec2-user/hello.txt

# Update system and install Git & Python
yum update -y
yum install -y git python3

# Clone the GitHub repo (via HTTPS)
git clone https://github.com/YasminTal/pokemon.git /home/ec2-user/pokemon

# Navigate to the repo
cd /home/ec2-user/pokemon

# (Optional) install Python dependencies
if [ -f requirements.txt ]; then
    python3 -m pip install -r requirements.txt
fi

# Run the Python script (adjust if needed)
python3 poke.py