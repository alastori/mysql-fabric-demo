import string
import random
import mysql.connector
from mysql.connector import fabric
import os
import time
import sys
import select
#import itertools

def lookupRandmonPlayer(conn):
	conn.reset_properties()
	conn.set_property(group="my_group",
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
	conn.set_property(group="my_group",
		mode=fabric.MODE_READONLY,
	)

	cur = conn.cursor()
	
	cur.execute(
		"select playerName , players.playerID, truncate(sum(score),2) as playerSum from scores join players on players.playerID = scores.playerID group by playerID order by playerSum desc limit 10",
	)

	playersTopScore = cur.fetchall();
	
	cur.execute(
		"select playerName , players.playerID, count(scores.score) as playerGames from scores join players on players.playerID = scores.playerID group by playerID order by playerGames desc limit 10",
	)

	playersTopActivity = cur.fetchall();
	
	os.system('clear')
	print '%-43s%-38s' % ('      Top scores', '      Most active')
	print '%-14s%-9s%-20s%-14s%-9s%-15s' % ('Name', 'ID', 'Score', 'Name', 'ID', 'Games')
	print '%-14s%-9s%-20s%-14s%-9s%-15s' % ('-----------', '---', '--------', '-----------', '---', '----')
	
	for i in range(10):
		print '%-14s%-9s%-20s%-14s%-9s%-15s' % (playersTopScore[i][0], playersTopScore[i][1], playersTopScore[i][2], playersTopActivity[i][0], playersTopActivity[i][1], playersTopActivity[i][2])
	
	print ""
	print "Press [Enter] to exit"
	

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