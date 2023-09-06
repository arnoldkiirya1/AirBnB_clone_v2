#!/usr/bin/env bash


# Install nginx if not already installed
if ! dpkg -l | grep -q nginx; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi

# create directories if they dont exist (-p)
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

touch /data/web_static/releases/test/index.html
#fake HTML for testing
echo "Hello, This is a test." > /data/web_static/releases/test/index.html

#handling symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

#nginx config to serve content
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

sudo service nginx restart
