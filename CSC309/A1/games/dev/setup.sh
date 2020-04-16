#!/bin/bash
DB_USER="$1";
DB_HOST="$2";
DB_NAME="$3";
DB_PASSWORD="$4";

if [ -z "$DB_USER" ]  || [ -z "$DB_HOST" ] || [ -z "$DB_NAME" ]  || [ -z "$DB_PASSWORD" ];
then
	echo "Usage: ./setup.sh DB_USER DB_HOST DB_NAME DB_PASSWORD"
	echo "Hint: ./setup.sh GROUP_NAME 127.0.0.1 GROUP_NAME DB_PASSWORD"

	exit 0
fi

sed -e "s/DB_NAME/$DB_NAME/" -e "s/DB_HOST/$DB_HOST/" -e "s/DB_USER/$DB_USER/" -e "s/DB_PASSWORD/$DB_PASSWORD/" dbconnect_string_template.php > ../lib/dbconnect_string.php

psql "dbname='$DB_NAME' user='$DB_USER' password='$DB_PASSWORD' host='$DB_HOST'" -f schema.sql
