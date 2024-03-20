#!/bin/bash
mysqlsh root@localhost -e "util.checkForServerUpgrade();"
