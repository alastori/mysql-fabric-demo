import string
import random
import mysql.connector
from mysql.connector import fabric
import os
import time
import sys
import select

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

def printResults(conn):
	playerID = lookupRandmonPlayer(conn)
	conn.reset_properties()
	conn.set_property(tables=["fabric_demo.scores"], key=playerID,
		mode=fabric.MODE_READONLY, scope=fabric.SCOPE_LOCAL)
	cur = conn.cursor()
	
	cur.execute(
		"SELECT count(*) FROM scores WHERE playerID = %s",
			(playerID,),
	)

	playerActivity = cur.fetchone();
	
	if playerActivity[0] != 0:
		cur.execute(
		"SELECT sum(score) FROM scores WHERE playerID = %s",
			(playerID,),
		)
		playerSum = cur.fetchone()
		
		print "Player", playerID, "has a total score of %.2f" % playerSum[0], "in total", playerActivity[0], "games. Press [Enter] to exit."
	else:
		print "Player", playerID, "has a no games yet. Press [Enter] to exit."


os.system('clear')
conn = mysql.connector.connect(
	fabric={"host" : "localhost", "port" : 32274,"username": "admin", "password" : "admin"},
	database="fabric_demo", user="web", password="web", autocommit=True, buffered=True,
)

while True:
	printResults(conn)
	time.sleep(0.5)

	if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		line = raw_input()
		conn.close()
		sys.exit()