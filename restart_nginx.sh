#!/bin/sh

initctl stop uwsgi
initctl start uwsgi
service nginx restart
