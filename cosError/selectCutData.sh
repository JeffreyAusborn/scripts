#!/bin/bash
CUTDATE=$1
DATESTAMP=$2
echo "DASHBOARD HARVEST: Selecting Data"
#SQL="SELECT * FROM server_errors WHERE server_error_date = '2018-03-22'"
SQL="SELECT * FROM server_error_cut_dates WHERE title = '$CUTDATE Cut';"
CUT_EXISTS="$(echo "$SQL" | sqlite3 /var/www/html/dashboard/dashboard.db)"

if [ -z "${CUT_EXISTS}" ]; then
    echo "New Cut"
    SQL="INSERT INTO server_error_cut_dates (server_error_date, title) VALUES ('$DATESTAMP','$CUTDATE Cut');"
    echo $SQL | sqlite3 /var/www/html/dashboard/dashboard.db
else
    echo "Cherry Pick"
    SQL="INSERT INTO server_error_cut_dates (server_error_date, title) VALUES ('$DATESTAMP','$CUTDATE Cherry');"
    echo $SQL | sqlite3 /var/www/html/dashboard/dashboard.db
fi
