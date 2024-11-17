#!/bin/sh
scp -r ./pi2/src/* admin@192.168.178.130:/home/admin/garden/src

#scp -r ./gardening-control-panel/build/* admin@192.168.178.130:/var/www/html/
scp -r ./gardening-control-panel/build/* admin@192.168.178.130:/home/admin/static