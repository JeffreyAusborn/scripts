#!/usr/bin/python
from sshtunnel import SSHTunnelForwarder
import MySQLdb
import getpass
import csv
import sys


def getOrders(host, username, password):
    with SSHTunnelForwarder((host, 22), ssh_password=password, ssh_username=username, remote_bind_address=('127.0.0.1', 3306)) as server:
        orderDict = {}
        orderCur = connectRoot(server, host)
        orderCur.execute("SELECT m.uuid, o.uuid FROM orders.orders o join meta.merchant m on m.id = o.merchant_id WHERE o.merchant_id > 0")
        for row in orderCur.fetchall():
            if not row[0] in orderDict:
                orderDict[row[0]] = []
            orderDict[row[0]].append(row[1])
        with open('orders.csv', 'w') as csvfile:
            fieldnames = ['mId', 'orderId']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k in orderDict:
                writer.writerow({'mId': k, 'orderId': ''})
                for i in range(0, len(orderDict[k])):
                    writer.writerow({'mId': '', 'orderId': orderDict[k][i]})


def getMerchants(host, username, password):
    with SSHTunnelForwarder((host, 22), ssh_password=password, ssh_username=username, remote_bind_address=('127.0.0.1', 3306)) as server:
        merchantDict = {}
        metaCur = connectRoot(server, host)
        metaCur.execute("SELECT uuid FROM meta.merchant WHERE id > 0")
        for row in metaCur.fetchall():
            if not row[0] in merchantDict:
                merchantDict[row[0]] = None
        with open('merchants.csv', 'w') as csvfile:
            fieldnames = ['mId']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k in merchantDict:
                writer.writerow({'mId': k})


def getAccessTokens(host, username, password):
    with SSHTunnelForwarder((host, 22), ssh_password=password, ssh_username=username, remote_bind_address=('127.0.0.1', 3306)) as server:
        accessDict = {}
        metaCur = connectRoot(server, host)
        metaCur.execute("SELECT m.uuid, hex(at.uuid) from meta.authtoken at join meta.merchant m on at.merchant_id = m.id where at.account_id is null and at.permissions = 8190 and at.device_id is null and at.deleted_time is null and m.id > 0")
        for row in metaCur.fetchall():
            if not row[0] in accessDict:
                accessDict[row[0]] = []
            accessDict[row[0]].append(row[1])
        with open('access.csv', 'w') as csvfile:
            fieldnames = ['mId', 'access']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k in accessDict:
                writer.writerow({'mId': k, 'access': ''})
                for i in range(0, len(accessDict[k])):
                    writer.writerow({'mId': '', 'access': accessDict[k][i]})


def connectRoot(server, host):
    if 'dev1.dev.clover.com' == host:
        conn = MySQLdb.connect(host='127.0.0.1', port=server.local_bind_port, user='root', passwd='test123')
    else:
        conn = MySQLdb.connect(host='127.0.0.1', port=server.local_bind_port, user='root', passwd='')
    cursor = conn.cursor()
    return cursor


def main():
    username = raw_input('Ldap_Username: ')
    password = getpass.getpass('Ldap_Password: ')
    host = sys.argv[1]
    getAccessTokens(host, username, password)


main()
