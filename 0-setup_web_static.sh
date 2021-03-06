#!/usr/bin/env bash
# Setting the web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
ufw allow 'Nginx HTTP'
mkdir -p /data/web_static/releases/test /data/web_static/shared/
fake_html=/data/web_static/releases/test/index.html
echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n<\html>" | sudo tee $fake_html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
config_file=/etc/nginx/sites-available/default
tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
listen 80 default_server;
listen [::]:80 default_server;
server_name localhost;

location /hbnb_static {
alias /data/web_static/current/;
}
}
EOF
service nginx restart
