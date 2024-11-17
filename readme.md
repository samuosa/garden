# Setup Raspberry

## Cloudflare

```
sudo apt install curl lsb-release
```

```
curl -L https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-archive-keyring.gpg >/dev/null
```

```
sudo apt update
```

```
sudo apt install cloudflared
```

```
cloudflared tunnel login
```

TODO Domain kaufen

## Jenkins

https://www.jenkins.io/blog/2018/04/25/configuring-jenkins-pipeline-with-yaml-file/

```
curl https://pkg.jenkins.io/debian/jenkins.io-2023.key | gpg --dearmor | sudo tee /usr/share/keyrings/jenkins-archive-keyring.gpg >/dev/null
```

```
sudo nano /etc/apt/sources.list.d/jenkins.list
```

```
deb [signed-by=/usr/share/keyrings/jenkins-archive-keyring.gpg] https://pkg.jenkins.io/debian binary/
```

```
sudo apt update
```

`sudo apt install jenkins`

`hostname -I`

cat /home/pi/.jenkins/secrets/initialAdminPassword

`jenkins`

webhook setup https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/testing-webhooks

## Python backend

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install Flask RPi.GPIO


python3 HelloWorld.py
```

ESP

ID 3443cd51-6070-4f92-9238-c3766c299f0c

key

28v#PXN@XKF#@1uASxSy!Bzvz

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">sudo apt install -y libraspberrypi0 libraspberrypi-dev
</code></div></div></pre>

sudo apt-get install -y v4l-utils

sudo apt install -y python3-opencv python3-pi

mariaDB

sudo apt install mariadb-server -y

sudo mysql_secure_installation

sudo systemctl start mariadb
sudo systemctl enable mariadb

CREATE DATABASE sensor_data;

CREATE USER 'flask'@'localhost' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON sensor_data.* TO 'flask'@'localhost';
FLUSH PRIVILEGES;

```sql
CREATE TABLE air_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    UNIQUE KEY unique_timestamp (timestamp)
);

```

```sql
CREATE TABLE floor_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    soil_moisture FLOAT,
    UNIQUE KEY unique_timestamp (timestamp)
);
```

```sql
CREATE TABLE fill_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    fill_level FLOAT,
    UNIQUE KEY unique_timestamp (timestamp)
);
```

sudo apt update
sudo apt install -y python3-dev build-essential

sudo apt-get install -y libgl1-mesa-glx

sudo apt install -y python3-picamera2

nginx

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">sudo nano /etc/nginx/sites-available/default
</code></div></div></pre>

server {
    listen 80;
    server_name _;

    root /var/www/html;
    index index.html;

    location / {
        # Handles React Router: Serves index.html for any unmatched routes
        try_files$uri $uri/ /index.html;
    }

    # Ensure Nginx can serve static assets like JS, CSS, images, etc.
    location /static/ {
        alias /var/www/html/static/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
}


sudo chown -R www-data:www-data /var/www/html

sudo chmod -R 755 /var/www/html
