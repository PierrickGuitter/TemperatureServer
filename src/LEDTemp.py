'''My very own temperature Server
Copyright 2017, Pierrick Guitter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.'''


import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import numpy, datetime, time


tempsensor='P9_39'
GridLed=numpy.array(['P8_8','P8_7','P8_10','P8_9','P8_12','P8_14','P8_15','P8_17','P8_18'])

'''
  _______________________________________________________________________
 | BLUE | BLUE | GREEN | GREEN | GREEN | YELLOW | YELLOW |  RED  |  RED  |
 | P8_8 | P8_7 | P8_10 | P8_9  | P8_12 | P8_14  | P8_15  | P8_17 | P8_18 |
  -----------------------------------------------------------------------
'''

def GPIOSetup():
	'''Setting Up all LEDs as GPIO output'''
	for x in range(0, 9):
		GPIO.setup(GridLed[x], GPIO.OUT)

def GPIOTurnOff():
	'''All LEDs turned off'''
	for x in range(0,9):
		GPIO.output(GridLed[x], GPIO.LOW)
	time.sleep(2)

def TempCalc():
	'''Define and print temperature from sensor'''
	#GPIOTurnOff()
	ADC.setup()
	TEMP=(ADC.read(tempsensor) * 1800 - 500) / 10
	print("tmp = %.2f" % TEMP)
	return TEMP

def Thermometer():
	'''Considering the value of TMP sensor, turn on LEDs or not'''
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
	'''Log all temperature every half hour, in TempLog.log.
	Give also food to the datafile that help generates a temperature curb every day'''

	#GPIOTurnOff()
	TEMP=TempCalc()
	date=time.strftime("%a %b  %-d %H:%M:%S CEST %Y")
	now=datetime.datetime.now()
	LimitHour=now.replace(hour=23, minute=27)
	
	try:
		with open("TempLog.log",'a') as ExternLog:
			ExternLog.write(date)
			ExternLog.write('\t')
			ExternLog.write("TEMPERATURE = ")
			ExternLog.write(str(TEMP))
			ExternLog.write('\n')
			if LimitHour<now:
				ExternLog.write('\n')
	except IOError:
		print("Opening Templog failed")
		

	try:
		with open("DataFile.dat",'a') as DailyData:
			DailyData.write(time.strftime("%H.%M"))
			DailyData.write('\t')
			DailyData.write(str(TEMP))
			DailyData.write('\n')
	except IOError:
		print("Opening Datafile failed")


def DateCalc():
	'''define if now() is between xx:28 and xx:31. If so, log it'''
	now=datetime.datetime.now()
	LogUPtimehalf=now.replace(minute=31)
	LogDOWNtimehalf=now.replace(minute=28)
	LogUPtimeNewHour=now.replace(minute=03)
	LogDOWNtimeNewHour=now.replace(minute=00)
	if (LogDOWNtimehalf<now and now<LogUPtimehalf) or (LogDOWNtimeNewHour<now and now<LogUPtimeNewHour):
		TempLogging()


def webServerRequest():
	'''WebServer takes its info from this request file'''
	TEMP=TempCalc()
	try:
		with open("/var/www/request.txt",'w') as webTemp:
			webTemp.write("date :\t")
			webTemp.write(time.strftime("%d:%m:%y--%H:%M"))
			webTemp.write('\t')
			webTemp.write("temperature :\t")
			webTemp.write(str(TEMP))
			webTemp.write('\n')
	except IOError:
		print("Opening request.txt failed")


if __name__ == '__main__':
	'''Infinite loop calculating temp, assigning LEDs and logging every two minutes'''
	while True:
		GPIOSetup()
		Thermometer()
		print time.strftime("%d:%m:%y--%H:%M")
		DateCalc()
		webServerRequest()
		time.sleep(120)	
