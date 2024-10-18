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
