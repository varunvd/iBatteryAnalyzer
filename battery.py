#!/usr/bin/env python
import sqlite3
import subprocess
import datetime
from pync import Notifier
from time import sleep
class battery:
	def add_current_status(self):
		direct_output = subprocess.check_output('pmset -g batt', shell=True)
		(b,d)=direct_output.split('%')
		(d,percentage)=b.split('InternalBattery-0\t')
		time_current = datetime.datetime.now()
		time_current=str(time_current)
		count=0
		for row in c.execute('SELECT * FROM battery'):
			count=count+1
		c.execute("INSERT INTO battery VALUES(?,? ,?)",(count+1,time_current,percentage))
		conn.commit()
	def compare_values(self,flag):
		current=datetime.datetime.now()
		count=0
		for row in c.execute('SELECT * FROM battery'):
			count=count+1
		if count==0:
			Notifier.notify("No values to compare")
			return
		direct_output = subprocess.check_output('pmset -g batt', shell=True)
		(b,d)=direct_output.split('%')
		(d,percentage)=b.split('InternalBattery-0\t')
		if flag==1:
			c.execute("INSERT INTO battery VALUES(?,? ,?)",(count+1,str(current),percentage))
			conn.commit()
		raw=c.execute("SELECT date,status FROM  battery WHERE  sl=?",(str(count)))
		for i in raw:
			print ''
		that_time=str(i[0])
		that_time=datetime.datetime.strptime(that_time, "%Y-%m-%d %H:%M:%S.%f")
		that_percentage=i[1]
		direct_output = subprocess.check_output('pmset -g batt', shell=True)
		(b,d)=direct_output.split('%')
		(d,percentage)=b.split('InternalBattery-0\t')
		difference_in_percentage=int(percentage)-int(that_percentage)
		difference_in_time=current-that_time
		difference_in_time=str(difference_in_time)
		Notifier.notify("Difference in battery percentage = {}\nDifference in time = {}".format(difference_in_percentage, difference_in_time))
	def clear_all_contents(self):
		c.execute('DELETE FROM battery')
		conn.commit()
if __name__ == '__main__':
	conn=sqlite3.connect('Battery.db')
	c=conn.cursor()
	t=battery()
	value=raw_input( "1 - Add the current status of the battery into the database\n2 - Compare the value of the battery\n3 - Provide the feedback about the battery usage every 10minutes\n4 - Clear the entire database\n5 - Any other key to exit\n")
	if value =='1':
		t.add_current_status()
	elif value == '2':
		t.compare_values(0)
	elif value == '3':
		for i in range(1,10000):
			sleep(600)
			t.compare_values(1)
	elif value=='4':
		t.clear_all_contents()
	else:
		conn.close()
		exit
	conn.close()
