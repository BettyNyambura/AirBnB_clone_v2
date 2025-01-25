#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static

# Install Nginx if it is not already installed
if ! dpkg -l | grep -qw nginx; then
  sudo apt-get update -y
  sudo apt-get install nginx -y
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Hello, world!
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or update the symbolic link
if [ -L /data/web_static/current ]; then
  sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Change ownership of /data/ to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
NGINX_CONF="/etc/nginx/sites-available/default"
sudo sed -i '/location \/hbnb_static {/d' $NGINX_CONF
sudo sed -i '/server {/a\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' $NGINX_CONF

# Restart Nginx to apply changes
sudo service nginx restart

exit 0
