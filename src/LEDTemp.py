import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import numpy, datetime, time


tempsensor='P9_39'
GridLed=numpy.array(['P8_8','P8_7','P8_10','P8_9','P8_12','P8_14','P8_15','P8_17','P8_18'])
#  _______________________________________________________________________
# | BLUE | BLUE | GREEN | GREEN | GREEN | YELLOW | YELLOW |  RED  |  RED  |
# | P8_8 | P8_7 | P8_10 | P8_9  | P8_12 | P8_14  | P8_15  | P8_17 | P8_18 |
#  -----------------------------------------------------------------------
#

def GPIOSetup():
	"""Setting Up all LEDs as GPIO output"""
	for x in range(0, 9):
		GPIO.setup(GridLed[x], GPIO.OUT)

def GPIOTurnOff():
	"""All LEDs turned off"""
	for x in range(0,9):
		GPIO.output(GridLed[x], GPIO.LOW)
	time.sleep(2)


def TempCalc():
	"""Define and print temperature from sensor"""
	#GPIOTurnOff()
	ADC.setup()
	TEMP=(ADC.read(tempsensor) * 1800 - 500) / 10
#print("%f" % ADC.read(tempsensor))
	print("===== tmp = %.2f =====" % TEMP)
	return TEMP

def Thermometer():
	"""Considering the value of TMP sensor, turn on LEDs or not"""
	TEMP=TempCalc()
	if TEMP <= 10:
		GPIO.output(GridLed[0], GPIO.HIGH)
		for x in range(1,9):
			GPIO.output(GridLed[x], GPIO.LOW)
	elif TEMP <= 12:
		for x in range(0,2):
			GPIO.output(GridLed[x], GPIO.HIGH)
		for x in range(2,9):
			GPIO.output(GridLed[x], GPIO.LOW)
	elif TEMP <= 14:
		for x in range(0,3):
			GPIO.output(GridLed[x], GPIO.HIGH)
		for x in range(3,9):
			GPIO.output(GridLed[x], GPIO.LOW)
	elif TEMP <= 16:
		for x in range(0,4):
			GPIO.output(GridLed[x], GPIO.HIGH)
		for x in range(4,9):
			GPIO.output(GridLed[x], GPIO.LOW)
	elif TEMP <= 18:
		for x in range(0,5):
			GPIO.output(GridLed[x], GPIO.HIGH)
		for x in range(5,9):
			GPIO.output(GridLed[x], GPIO.LOW)
	elif TEMP <= 20:
		for x in range(0,6):
			GPIO.output(GridLed[x], GPIO.HIGH)
		for x in range(6,9):
			GPIO.output(GridLed[x], GPIO.LOW)
	elif TEMP <= 22:
		for x in range(0,7):
			GPIO.output(GridLed[x], GPIO.HIGH)
		for x in range(7,9):
			GPIO.output(GridLed[x], GPIO.LOW)
	elif TEMP <= 24:
		for x in range(0,8):
			GPIO.output(GridLed[x], GPIO.HIGH)	
		for x in range(8,9):
			GPIO.output(GridLed[x], GPIO.LOW)	
	else:
		for x in range(0,9):
			GPIO.output(GridLed[x], GPIO.HIGH)

def TempLogging():
	"""Log all temperature every half hour, in TempLog.log"""
	#GPIOTurnOff()
	TEMP=TempCalc()
	date=time.strftime("%a %b  %-d %H:%M:%S CEST %Y")
	now=datetime.datetime.now()
	LimitHour=now.replace(hour=23, minute=27)
	FILE=open("TempLog.log",'a')
	FILE.write(date)
	FILE.write('\t')
	FILE.write("TEMPERATURE = ")
	FILE.write(str(TEMP))
	FILE.write('\n')

	if LimitHour<now:
		FILE.write('\n')
	FILE.close()

	F=open("DataFile.dat",'a')
	F.write(time.strftime("%H.%M"))
	F.write('\t')
	F.write(str(TEMP))
	F.write('\n')
	F.close()


def DateCalc():
	"""define if now() is between xx:28 and xx:31. If so, log it"""
	now=datetime.datetime.now()
	LogUPtimehalf=now.replace(minute=31)
	LogDOWNtimehalf=now.replace(minute=28)
	LogUPtimeNewHour=now.replace(minute=03)
	LogDOWNtimeNewHour=now.replace(minute=00)
	if (LogDOWNtimehalf<now and now<LogUPtimehalf) or (LogDOWNtimeNewHour<now and now<LogUPtimeNewHour):
		TempLogging()

def webServerRequest():
	"""WebServer takes its info from this request file"""
	TEMP=TempCalc()
	F=open("/var/www/request.txt",'w')
	F.write("date :\t")
        F.write(time.strftime("%d:%m:%y--%H:%M"))
        F.write('\t')
	F.write("temperature :\t")
        F.write(str(TEMP))
        F.write('\n')
        F.close()



if __name__ == '__main__':
	"""Infinite loop calculating temp and assigning LEDs every two minutes"""
	while True:
		GPIOSetup()
		Thermometer()
		print time.strftime("%d:%m:%y--%H:%M")
		DateCalc()
		webServerRequest()
		time.sleep(120)	
