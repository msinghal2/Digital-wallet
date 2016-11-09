#!/usr/bin/env python

#import csv																											#If using csv reader module
import sys
import time

inputFile = sys.argv[1]
streamFile = sys.argv[2]
outFile1 = sys.argv[3]
outFile2 = sys.argv[4]
outFile3 = sys.argv[5]

def feature1(sId1, sId2, trans) :
	"Checks for 1st degree relation"
	deg1=0
	if sId2 in trans[sId1] or sId1 in trans[sId2]:
		deg1=1
		return deg1
	return 0
		
def feature2(sId1, sId2, trans) :
	"Checks for 2nd degree relation"
	deg2=0
	for b in trans[sId1]:
		if sId2 in trans[b]:
			deg2=1
			return deg2
	return 0
	
def feature3(sId1, sId2, trans) :
	"Checks for 3rd and 4th degree relation"
	deg3=0
	deg4=0
	for b in trans[sId1]:
		for k in trans[b]:
			if sId2 in trans[k]:
				deg3=1
				return deg3
	
	for b in trans[sId1]:
		for k in trans[b]:
			for i in trans[k]:
				if sId2 in trans[i]:
					deg4=1
					return deg4
	return 0

start_timetot = time.time() 																						#Total program execution start time
start_time = time.time()																							#Transaction history data structure creation start time			

#------------Creating transaction history data structure-----------------#
with open(inputFile, 'rt', encoding = "utf-8") as f:																#Encoding can be changed depending on file
	header = f.readline().split(', ')																				#Takes the 1st row of csv for header
	#reader = csv.reader(f)																							#If using csv module
	trans = {}																										#Dictionary data structure for transaction between 2 id's
	for row in f:
		tempList = row.split(', ')
		if (len(tempList)<4) : continue																				#If row contains less data than number of headers i.e. short data, then skip that row
		id1 = tempList[1]
		id2 = tempList[2]
		
		#id1 = row.split(', ')[1]																					#Without using the above check
		#id2 = row.split(', ')[2]
		
		if id1 in trans and id2 not in trans[id1]:																	#Checks if key exists already and if value does not exist at that key
			trans[id1].add(id2)																						#If key exists but not value then, adds new value. Otherwise,
		else:																										#Adds new key, value
			trans[id1] = set()																						#Dictionary key = id, value = (set of id's)
			trans[id1].add(id2)
		if id2 in trans and id1 not in trans[id2]:
			trans[id2].add(id1)
		else:
			trans[id2] = set()
			trans[id2].add(id1)

	#print (trans)																									#Print out "Transaction history data structure"	

print("Time for creating transaction dictionary : %s seconds" %(time.time()-start_time))
																										
fstart_time = time.time()																							#Feature allocation start time

#-------------Feature allocation for new transactions and writing output to file-------------#
with open(streamFile, 'rt', encoding = "utf-8") as q, open(outFile1, 'w') as r, open(outFile2, 'w') as s, open(outFile3, 'w') as t:
	sHeader = q.readline().split(', ')																				#Takes the 1st row of csv for header
	#sReader = csv.reader(q)																						#If using csv module
	linenum=1																										#To check which lines in stream payment data were short
	count=0																											#To count the total number of short rows
	for sRow in q:
		linenum+=1
		stempList = sRow.split(', ')
		if (len(stempList)<4) :																						#If row contains less data than number of headers i.e. short data, then skip that row
			#print ("line skipped %s" %linenum) 
			count+=1
			continue																								
		sId1 = stempList[1]
		sId2 = stempList[2]

		#sId1 = sRow.split(', ')[1]																					#Without using the above check for short row data
		#sId2 = sRow.split(', ')[2]
		
		f1=0
		f2=0
		f3=0
		
		if sId1 in trans and sId2 in trans:																			#Check both id's have had at least 1 past transaction
		
			#time_f1 = time.time()
			f1 = feature1(sId1, sId2, trans)																		#1st degree relation - feature1
			#print("Time for feature1 : %s" %(time.time()-time_f1))
			if (f1):
				r.write('trusted\n')
				s.write('trusted\n')
				t.write('trusted\n')
				continue
				
			#time_f2 = time.time()	
			f2 = feature2(sId1, sId2, trans)																		#2nd degree relation - feature2			
			#print("Time for feature2 : %s" %(time.time()-time_f2))			
			if (f2):
				
				#trans[sId1].add(sId2)																				#To add streamed payment to "Transaction history data structure" 
				#trans[sId2].add(sId1)
				
				r.write('unverified\n')
				s.write('trusted\n')
				t.write('trusted\n')
				continue
				
			#time_f3 = time.time()
			f3 = feature3(sId1, sId2, trans)																		#3rd and 4th degree relation - feature3
			#print("Time for feature3 : %s" %(time.time()-time_f3))
			if (f3):
				
				#trans[sId1].add(sId2)																				#To add streamed payment to "Transaction history data structure"
				#trans[sId2].add(sId1)
				
				r.write('unverified\n')
				s.write('unverified\n')
				t.write('trusted\n')
				continue
				
			r.write('unverified\n')																					#Beyond 4th degree relation
			s.write('unverified\n')
			t.write('unverified\n')
				
		else:																										#If either id does not exist in "Transaction history data structure"
			r.write('unverified\n')
			s.write('unverified\n')
			t.write('unverified\n')
			
#			if(sId1 not in trans) : 																				#To add streamed payment id's to "Transaction history data structure"
#				trans[sId1] = set()
#				trans[sId1].add(sId2)
#			else: 
#				trans[sId1].add(sId2)
#			if(sId2 not in trans) : 
#				trans[sId2] = set()
#				trans[sId2].add(sId1)
#			else: 
#				trans[sId2].add(sId1)
			
	
	#print("Total skipped lines %s" %count)

print("Total Time for writing features in file : %s seconds" %(time.time()-fstart_time))

print("Total Time for program execution : %s seconds" %(time.time()-start_timetot))
			
	
	

	