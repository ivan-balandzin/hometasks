import configparser, psutil, schedule, json, datetime, time, os.path, re

# Including configuration file
config = configparser.ConfigParser()
config.read('config3.ini')
output_type = config.get('common', 'type')
interval = config.get('common', 'interval')


# Converting PSUTIL into DICTIONARIES
def makedict(p):
	val = list(p)
	key = p._fields
	result_dict = dict(zip(key, val))
	return result_dict


# Definition of text file function
def ft(file="output.txt"):
	global ss
	print("Writing text snapshot {}:".format(ss))  # Writing info in console
	ts = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')
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
	print ("Done! Now timeout " + interval + "m")


# Definition of json file function
def fj(file="output.json"):
	global ss
	print("Writing json snapshot {}:".format(ss))  # Writing info in console
	ts = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
	f_json = open(file, "a+")
	f_json.write("__________________________________")
	f_json.write("\nSnapshot{0}:{1}\n".format(ss, ts))
	f_json.write("4 core CPU usage\n")
	json.dump(psutil.cpu_percent(percpu=True), f_json, indent=4)
	f_json.write("\nVirtual memory usage\n")
	json.dump(makedict(psutil.virtual_memory()), f_json, indent=4)
	f_json.write("\nDisk usage\n")
	json.dump(makedict(psutil.disk_io_counters(perdisk=False)), f_json, indent=4)
	json.dump(makedict(psutil.disk_usage('/')), f_json, indent=4)
	f_json.write("\nNetwork\n")
	json.dump(psutil.net_io_counters(pernic=True), f_json, indent=4)
	f_json.write("\n\n")
	f_json.close()
	ss += 1
	print ("Done! Now timeout " + interval + "m")


if output_type == "txt":
	#This part of code checks if txt output file exists. 
	#If it is - takes the number of previously done snapshot
	#and makes the next snapshot with the next number.
	#If file don't exist - starting from the 1-st number.
	if os.path.isfile("output.txt") == True:
		fl = open("output.txt", "r").read()
		ss=int(re.compile(r'Snapshot(\d+)').findall(fl)[-1])+1
	else:
		ss=1
	# Writing in console info about choosed parameters, defined in config file.
    	print('Configuration:\nOutput:' + output_type + '\nInterval:' + interval + 'm')
    	schedule.every(int(interval)).minutes.do(ft)
    	ft() #Run execution only first time without timeout, defined in config.


elif output_type == "json":
	#This part of code checks if json output file exists. 
	#If it is - takes the number of previously done snapshot
	#and makes the next snapshot with the next number.
	#If file don't exist - starting from the 1-st number.
	if os.path.isfile("output.json") == True:
		fl = open("output.json", "r").read()
		ss=int(re.compile(r'Snapshot(\d+)').findall(fl)[-1])+1
	else:
		ss=1
	# Writing in console info about choosed parameters, defined in config file.
    	print('Configuration:\nOutput:' + output_type + '\nInterval:' + interval + 'm')
    	schedule.every(int(interval)).minutes.do(fj)
    	fj() #Run execution only first time without timeout, defined in config.
else:
	print("Configuration:\nUnknown type of output")
	quit()
while True:
	schedule.run_pending()
	time.sleep(100)
