import configparser, psutil, schedule, json, datetime, time, os.path, re

# Including configuration file
config = configparser.ConfigParser()
config.read('config4.ini')
output_type = config.get('common', 'type')
interval = config.get('common', 'interval')




if output_type == "txt":
	#This part of code checks if txt output file exists. 
	#If it is - takes the number of previously done snapshot
	#and makes the next snapshot with the next number.
	#If file don't exist - starting from the 1-st number.
	if os.path.isfile("output.txt") == True:
		fl = open("output.txt", "r").read()
		ss = int(re.compile(r'Snapshot(\d+)').findall(fl)[-1])+1
	else:
		ss = 1
	
elif output_type == "json":
	#This part of code checks if json output file exists. 
	#If it is - takes the number of previously done snapshot
	#and makes the next snapshot with the next number.
	#If file don't exist - starting from the 1-st number.
	if os.path.isfile("output.json") == True:
		fl = open("output.json", "r").read()
		ss = int(re.compile(r'Snapshot(\d+)').findall(fl)[-1])+1
	else:
		ss = 1
else:
	print("Configuration:	denied\nUnknown type of output")
	quit()

# Writing in console info about choosed parameters, defined in config file.
print('Configuration:	allowed\nOutput:		' + output_type + '\nInterval:	' + interval + 'm')



#Parent (inheritant) class
class parent(object):
	# Converting PSUTIL into DICTIONARIES
	def makedict(self, p):
		val = list(p)
		key = p._fields
		result_dict = dict(zip(key, val))
		return result_dict
	#Timestamp and it's formatting
	timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')





#Text type class
class ft_cl(parent):
	# Definition of text file function
	def ft(self, file = "output.txt"):
		global ss
		ts=super(ft_cl,self).timestamp
		print("\nWriting text snapshot {}:".format(ss))  # Writing info in console
		f_text = open(file, "a+")
		f_text.write("__________________________________")
		f_text.write("\nSnapshot{0}:{1}\n".format(ss, ts))
		f_text.write("\n_____CPU______\n 4 core CPU usage {0} percent\n".format(psutil.cpu_percent(percpu=True)))
		f_text.write("\n___VIRT_MEM___\n total {0} bytes \n available {1} bytes \n used {2} bytes \n".format(psutil.virtual_memory()[0], psutil.virtual_memory()[1], psutil.virtual_memory()[4]))
		f_text.write("\n__DISK_USAGE__\n read cout {0} \n write count {1}\n read {2} bytes \n write {3} bytes \n disk usage {4} \n".format(psutil.disk_io_counters(perdisk=False)[0], psutil.disk_io_counters(perdisk=False)[1], psutil.disk_io_counters(perdisk=False)[2], psutil.disk_io_counters(perdisk=False)[3], psutil.disk_usage('/')))
		f_text.write("\n____NETWORK___\n info: {}\n".format(psutil.net_io_counters(pernic=True)))
		f_text.write("\n")
		f_text.close()
		ss += 1
		print("Done! Now timeout " + interval + "m")





#Json type class
class fj_cl(parent):
	# Definition of json file function
	def fj(self, file = "output.json"):
		global ss
		ts=super(fj_cl,self).timestamp
		print("\nWriting json snapshot {}:".format(ss))  # Writing info in console
		f_json = open(file, "a+")
		f_json.write("__________________________________")
		f_json.write("\nSnapshot{0}:{1}\n".format(ss, ts))
		f_json.write("4 core CPU usage\n")
		json.dump(psutil.cpu_percent(percpu=True), f_json, indent=4)
		f_json.write("\nVirtual memory usage\n")
		json.dump(super(fj_cl, self).makedict(psutil.virtual_memory()), f_json, indent=4)
		f_json.write("\nDisk usage\n")
		json.dump(super(fj_cl, self).makedict(psutil.disk_io_counters(perdisk=False)), f_json, indent=4)
		json.dump(super(fj_cl, self).makedict(psutil.disk_usage('/')), f_json, indent=4)
		f_json.write("\nNetwork\n")
		json.dump(psutil.net_io_counters(pernic=True), f_json, indent=4)
		f_json.write("\n\n")
		f_json.close()
		ss += 1
		print("Done! Now timeout " + interval + "m")



def run():
	if output_type == "txt":
	    	text_function.ft()
	
	
	elif output_type == "json":
	    	json_function.fj()
	else:
		print("Configuration:\nUnknown type of output")
		quit()

text_function=ft_cl()
json_function=fj_cl()


run()
schedule.every(int(interval)).minutes.do(run)

while True:
	schedule.run_pending()
	time.sleep(100)
