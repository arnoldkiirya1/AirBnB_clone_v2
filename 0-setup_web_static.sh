#!/usr/bin/env bash


# Install nginx if not already installed
if ! dpkg -l | grep -q nginx; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi

# create directories if they dont exist (-p)
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

#fake HTML for testing
echo "<html>
  <head>
  </head>
  <body>
    <p>Hello, This is a test.</p>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

#handling symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

#nginx config to serve content
config_text="location /hbnb_static/ {
    alias /data/web_static/current/;
    index index.html;
}"

sudo sed -i "/default_server/a $config_text" /etc/nginx/sites-available/default

sudo service nginx restart
