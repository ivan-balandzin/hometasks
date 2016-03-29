import configparser, psutil, schedule, json, datetime, time, os.path, re, logging, logging.config

# Including configuration file
config = configparser.ConfigParser()
config.read('config5.ini')
output_type = config.get('common', 'type')
interval = config.get('common', 'interval')
log_level = config.get('common', 'level')

#Logging settings
handler = logging.FileHandler('Task5.log')
logger = logging.getLogger()
formatter = logging.Formatter('%(levelname)-10s %(asctime)-2s %(name)-10s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_level)
#First message with current level of logging
logger.info("Logging {} level messages".format(log_level))


if output_type == "txt":
	#This part of code checks if txt output file exists. 
	#If it is - takes the number of previously done snapshot
	#and makes the next snapshot with the next number.
	#If file don't exist - starting from the 1-st number.
	if os.path.isfile("output.txt") == True:
		logger.info("output.txt file exists, searching for snapshot №")
		fl = open("output.txt", "r").read()
		ss = int(re.compile(r'Snapshot(\d+)').findall(fl)[-1])+1
		logger.info("Snapshot № {0} found, using № {1}".format(ss-1, ss))
	else:
		logger.info("No output.txt files found, using snapshot №1")
		ss = 1
	
elif output_type == "json":
	#This part of code checks if json output file exists. 
	#If it is - takes the number of previously done snapshot
	#and makes the next snapshot with the next number.
	#If file don't exist - starting from the 1-st number.
	if os.path.isfile("output.json") == True:
		logger.info("output.json file exists, searching for snapshot №")
		fl = open("output.json", "r").read()
		ss = int(re.compile(r'Snapshot(\d+)').findall(fl)[-1])+1
		logger.info("Snapshot № {0} found, using № {1}".format(ss-1, ss))
	else:
		logger.info("No output.json file found, using snapshot №1")
		ss = 1
else:
	print("Configuration:	denied\nUnknown type of output. 'txt' or 'json' are expected, '{}' given".format(output_type))
	logger.error("Unknown type of output. 'txt' or 'json' are expected, '{}' given".format(output_type))
	quit()


# Writing in console info about choosed parameters, defined in config file.
print('Configuration:	allowed\nOutput:		' + output_type + '\nInterval:	' + interval + 's')



#Decoration
def tracer(dec_f):
	def wrapper(file):
		dec_f(file)
	return wrapper




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
class ft_class(parent):
	@tracer
	# Definition of text file function
	def ft(self, file = "output.txt"):
		global ss
		logger.info("Startig write snapshot {} in output.txt file".format(ss))
		ts=super(ft_class,self).timestamp
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
		logger.info("Writing in output.txt file has finished")
		print("Done! Now timeout " + interval + "s")





#Json type class
class fj_class(parent):
	@tracer
	# Definition of json file function
	def fj(self, file = "output.json"):
		global ss
		logger.info("Startig write snapshot {} in output.json file".format(ss))
		ts=super(fj_class,self).timestamp
		print("\nWriting json snapshot {}:".format(ss))  # Writing info in console
		f_json = open(file, "a+")
		f_json.write('\n{{"Snapshot{0}": "{1}",\n'.format(ss, ts))
		f_json.write('"4 core CPU usage":\n')
		json.dump(psutil.cpu_percent(percpu=True), f_json, indent=4)
		f_json.write(",")
		f_json.write('\n"Virtual memory usage":\n')
		json.dump(super(fj_class, self).makedict(psutil.virtual_memory()), f_json, indent=4)
		f_json.write(',\n"Disk usage":\n')
		json.dump(super(fj_class, self).makedict(psutil.disk_io_counters(perdisk=False)), f_json, indent=4)
		f_json.write(',\n"Disk IO":\n')
		json.dump(super(fj_class, self).makedict(psutil.disk_usage('/')), f_json, indent=4)
		f_json.write(',\n"Network":\n')
		json.dump(psutil.net_io_counters(pernic=True), f_json, indent=4)
		f_json.write("}\n\n")
		f_json.close()
		ss += 1
		logger.info("Writing in output.json file has finished")
		print("Done! Now timeout " + interval + "s")



def run():
	if output_type == "txt":
	    	text_function.ft()
	
	
	else:
	    	json_function.fj()


text_function=ft_class()
json_function=fj_class()


try:
	logger.info("Starting main process")
	run()
	logger.info("Main process execution has finished successfully")
except Exception as exc:
	logging.exception("Can't execute run() function {}".format(exc))


try:
	logger.info("Starting schedule process")
	schedule.every(int(interval)).seconds.do(run)
except Exception as exc:
	logging.exception("Can't execute scheduling {}".format(exc))


while True:
	schedule.run_pending()
	time.sleep(1)
