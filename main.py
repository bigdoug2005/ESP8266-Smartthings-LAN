import machine
import utime
import network
import ssd1306
import urequests
import ubinascii
from machine import ADC
from machine import I2C, Pin

ssid = 'YourSSID'
PW = 'YourPassword'


###Check if we woke from sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
####Set up I2C and Display#####
i2c = I2C(-1, Pin(5), Pin(4))
display_w = 128
display_h = 64
display_addr = 0x3C
display = ssd1306.SSD1306_I2C(display_w, display_h, i2c, display_addr)
display.fill(0)
display.show()

display.text("Connecting To:", 0, 0)
display.text(ssid,0,8)
display.show()

#####Disable Access Point#####
ap_if = network.WLAN(network.AP_IF) 
ap_if.active(False)					

#######Conenct to Network#####
wlan = network.WLAN(network.STA_IF) #Connect to Wifi
wlan.active(True)
wifi_timeout = 0
if not wlan.isconnected():
	print('Connecting to Network...')
	wlan.connect(ssid, PW)
	while not wlan.isconnected():
		wifi_timeout = wifi_timeout + 1
		if wifi_timeout == 15:
			print('Unable To Connect. Rebooting')
			machine.reset()
		utime.sleep(1)
		
print('Network Config:', wlan.ifconfig())
a,b,c,d=wlan.ifconfig()				#Get IP address
##########Flash LED##########
pin = machine.Pin(2, machine.Pin.OUT)
pin.on()
utime.sleep_ms(500)
pin.off()
utime.sleep_ms(500)
pin.on()
utime.sleep_ms(500)
pin.off()
#########Display IP Address####
display.fill(0)
display.show()
display.text("Network Address", 0, 0)
display.text(a, 0, 8)
display.show()
######Sample ADC###########
adc = ADC(0)
ADC_Val = adc.read()
print('ADC Value: ' + str(ADC_Val))

######Map ADC counts to percent###########
if ADC_Val < 438:
	percent_humidity = 100
else:
	percent_humidity = int(14224800000*ADC_Val**(-3.088158))
print('Humidity Reading: ' + str(percent_humidity))	
######Draw bar graph of humidity sensed###
rect_w = int(percent_humidity/100*display_w)
display.fill_rect(0,16,display_w,16,0)
display.fill_rect(0,16,rect_w,16,1)
display.show()

######Send Data to SmartThings######
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
data_list = '{"state":' + str(percent_humidity) + ',"name":"' + str(mac) + '"}'
length = len(data_list)
header_list = {'Content-type': 'text/html','Content-Length': str(length)}
r = urequests.post("http://192.168.1.116:39500", data = data_list, headers = header_list)
print('Data sent to Smartthings')
#####Wait (for development purposes) before going to sleep####
print('Preparing to sleep')	
utime.sleep(5)  
display.fill(0)
display.show()
t = 25
while t >= 1:
	display.fill(0)
	display.text("Sleep In " + str(t), 0, 0)
	display.text("Humidity: " +str(percent_humidity) + "%", 0, 8)
	display.show()
	t=t-1
	utime.sleep(1)  
display.fill(0)
display.text("Sleeping", 0, 0)
display.text("Humidity: " +str(percent_humidity) + "%", 0, 8)
display.show()
########Sleep############
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 900000) # set RTC.ALARM0 to fire after 15 minutes (waking the device)
machine.deepsleep() # put the device to sleep
