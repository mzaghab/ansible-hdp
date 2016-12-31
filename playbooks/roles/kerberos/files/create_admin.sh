#!/bin/bash
# Author : Mounir ZAGHAB
# Date : 31/07/2016 

echo -e "$1\n$1" | kadmin.local  -q "addprinc $2/admin"

