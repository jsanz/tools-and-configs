#!/bin/sh

#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE":
#  <xurxosanz@gmail.com> wrote this file. As long as you retain this notice you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer in return.
#  ----------------------------------------------------------------------------

# Why: creates the most simple web server on the folder this script is run
# Require: standard python
# Provides: go to http://localhost:8000
# 

python -m SimpleHTTPServer

# You can place your preferred port also
# python -m SimpleHTTPServer 8080