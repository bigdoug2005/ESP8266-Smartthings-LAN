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
display_h = 32
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
if not wlan.isconnected():
	print('Connecting to Network...')
	wlan.connect(ssid, PW)
	while not wlan.isconnected():
		pass
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
rect_w = int(ADC_Val/1024*128)
display.fill_rect(rect_w,16,128,16,0)
display.fill_rect(0,16,rect_w,16,1)
display.show()
######Send Data to SmartThings######
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
data_list = '{"state":' + str(ADC_Val) + ',"name":"' + str(mac) + '"}'
length = len(data_list)
header_list = {'Content-type': 'text/html','Content-Length': str(length)}
r = urequests.post("http://192.168.1.116:39500", data = data_list, headers = header_list)
print('Data sent to smartthings')
#####Wait (for development purposes) before going to sleep####
utime.sleep(5)  
display.fill(0)
display.show()
t = 25
while t >= 1:
	display.fill(0)
	display.text("Sleep In", 0, 0)
	display.text(str(t), 0, 8)
	display.show()
	t=t-1
	utime.sleep(1)  
display.fill(0)
display.text("Sleeping", 0, 0)
display.show()
########Sleep############
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 60000) # set RTC.ALARM0 to fire after 30 seconds (waking the device)
machine.deepsleep() # put the device to sleep
