#!/usr/bin/env bash
# installs nginx and configures it
apt update
apt -y install nginx

#creates folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# creates a HTML test file
echo "webstatic deploy test" >> /data/web_static/releases/test/index.html

# creates a symbolic link and deletes already exists and recreates it
rm -f /data/web_static/current && ln -s /data/web_static/releases/test/ /data/web_static/current

# giving onwership to user and group
sudo chown -R ubuntu:ubuntu /data/

# updating the nginx config file to serve the content 
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html index.nginx-debian.html;
   
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.nginx-debian.html;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/;
    }

    error_page 404 /error_404.html;
    location / {
        root /var/www/html;
        internal;
    }
}" | sudo tee /etc/nginx/sites-available/default > /dev/null
sudo service nginx restart
