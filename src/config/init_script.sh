# To avoid generating .pyc files
export PYTHONDONTWRITEBYTECODE=1

# Update and get tookit for python
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install python3-pip
sudo apt-get install python3-venv
pip install --upgrade pip

# Fetch docker convenience script and install docker
curl -sSL https://get.docker.com/ | sh
# Add user to docker group
sudo usermod -aG docker $USER
# Expose docker socket to localhost:2375
sudo cat ./config/docker.conf > /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo service docker restart
# Install
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash




export DOCKER_HOST=tcp://localhost:2375

