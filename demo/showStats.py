import string
import mysql.connector
import os
import time
import sys
import select

if (len(sys.argv) == 0) or (len(sys.argv) == 1):
	print "showStats.py -n <number of servers>"
	sys.exit(2)

def printStats(statsInsert, statsSelect, statsRowsPlayers, statsRowsScrores):
	
	os.system('clear')
	print '%-20s%-25s%-25s' % ('Server', 'INSERTs', 'SELECTs')
	print '%-20s%-25s%-25s' % ('-----------', '----------', '----------')
	
	for i in range(len(statsInsert)):
		print '%-20s%-25s%-25s' % (i+1, statsInsert[i], statsSelect[i])
	
	print ""
	
	if len(statsRowsPlayers) != 0:
		print '%-20s%-28s%-28s' % ('Server', 'Rows in players', 'Rows in scores')
		print '%-20s%-28s%-28s' % ('-----------', '----------------------', '----------------------')

		for i in range(len(statsRowsPlayers)):
			print '%-20s%-28s%-28s' % (i+1, statsRowsPlayers[i], statsRowsScrores[i])
		
		print ""
	
	print "Press [Enter] to exit"	

def collectStats():
	statsSelect = list();
	statsInsert = list();
	statsRowsPlayers = list();
	statsRowsScrores = list();
	mysqlPort = 3307

	for _ in range (int(sys.argv[2])):
		conn = mysql.connector.connect(
			user='root', password='', host='127.0.0.1', port=mysqlPort
		)
		
		cur = conn.cursor()
		cur.execute("select VARIABLE_NAME, VARIABLE_VALUE from information_schema.GLOBAL_STATUS "
			"where VARIABLE_NAME = 'Com_insert' "
				"OR VARIABLE_NAME = 'Com_select'"
		)
		
		for row in cur:
			if row[0] == 'COM_INSERT':
				statsInsert.append(row[1]);
			if row[0] == 'COM_SELECT':
				statsSelect.append(row[1]);
		
		cur.execute("select TABLE_NAME, TABLE_ROWS from information_schema.TABLES "
			"where TABLE_SCHEMA='fabric_demo' "
					"and TABLE_NAME='players' "
					"or TABLE_NAME='scores'"
		)
		
		for row in cur:
			if row[0] == 'players':
				statsRowsPlayers.append(row[1]);
			if row[0] == 'scores':
				statsRowsScrores.append(row[1]);
		
		mysqlPort+=1
		
		conn.close()
		
	printStats(statsInsert, statsSelect, statsRowsPlayers, statsRowsScrores)

while True:
	collectStats()
	time.sleep(0.5)

	if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		line = raw_input()
		sys.exit()