import os
import sys
import select
import string
import random
import mysql.connector
from mysql.connector import fabric
import collections

def initialize():
	conn = mysql.connector.connect(
		fabric={"host" : "localhost", "port" : 32274,"username": "admin", "password" : "admin"},
		user="web", password="web", autocommit=True, buffered=True,
	)

	conn.set_property(group="group_id-global", mode=fabric.MODE_READWRITE)
	cur = conn.cursor()
	
	if (sys.argv[len(sys.argv)-1] == "-i"):
		cur.execute("DROP DATABASE IF EXISTS fabric_demo")
		print "Dropped database and starting from scratch"
	
	cur.execute("CREATE DATABASE IF NOT EXISTS fabric_demo")
	cur.execute("USE fabric_demo")
	cur.execute(
		"CREATE TABLE IF NOT EXISTS players ("
			"playerID int(10) unsigned NOT NULL AUTO_INCREMENT,"
			"playerName varchar(10) DEFAULT '0',"
				"PRIMARY KEY (playerID)"
		")"
	)
	cur.execute(
		"CREATE TABLE IF NOT EXISTS scores ("
			"scoreID int(10) unsigned NOT NULL AUTO_INCREMENT,"
			"playerID int(10) unsigned NOT NULL DEFAULT '0',"
			"score float NOT NULL DEFAULT '0',"
				"PRIMARY KEY (scoreID, playerID)"
		")"
	)
	conn.close()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def new_players(conn):
	conn.reset_properties()
	conn.set_property(tables=["fabric_demo.scores"], 
		mode=fabric.MODE_READWRITE,
		scope=fabric.SCOPE_GLOBAL,
	)
	cur = conn.cursor()

	for i in range (0,100):
		cur.execute(
			"INSERT INTO players (playerName) VALUES (%s)",
			(id_generator(10),),
		)

def lookupRandmonPlayer(conn):
	conn.reset_properties()
	conn.set_property(tables=["fabric_demo.scores"],
		scope=fabric.SCOPE_GLOBAL,
		mode=fabric.MODE_READONLY,
	)
	cur = conn.cursor()
	cur.execute(
		"SELECT playerID FROM players "
		"ORDER BY rand() "
		"LIMIT 1 "
	)
	
	playerID = cur.fetchone()
	return playerID[0]

def add_scroe(conn):
	playerID = lookupRandmonPlayer(conn)

	conn.reset_properties()
	conn.set_property(tables=["fabric_demo.scores"], key=playerID,
		mode=fabric.MODE_READWRITE, scope=fabric.SCOPE_LOCAL)
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO scores (playerID, score) VALUES (%s, %s)",
		(playerID, random.uniform(0,10))
	)

os.system('clear')
print "Initialising...."

initialize()

# Address of the Fabric, not the host we are going to connect to.
conn = mysql.connector.connect(
	fabric={"host" : "localhost", "port" : 32274,"username": "admin", "password" : "admin"},
	database="fabric_demo", user="web", password="web", autocommit=True, buffered=True,
)

new_players(conn)

loopCount = 0
syms = collections.deque(['\\', '|', '/', '-'])
bs = '\b'

while True:
	add_scroe(conn)
	
	if loopCount % 500 == 0:
		print "Added", loopCount, "scores... Press [Enter] to stop."
	loopCount += 1

	sys.stdout.write("%s\b" % syms[0])
	sys.stdout.flush()
	syms.rotate(1)
	
	if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		line = raw_input()
		conn.close()
		sys.exit()