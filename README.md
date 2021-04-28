# ESP8266-Smartthings-LAN
Create a LAN connected device using ESP8266 (NodeMCU) without requiring any OAuth or MQTT

This is my attempt at building a WiFi device that requires a minimal amount of set up and infrastructure. Tthere is a lot of outdated or wrong information on what is required to get a LAN device to talk to a SmartThings hub. Many implementations require a server of some sort to bridge the gap between the SmartThings cloud and a  WiFi device.

There are three things needed to get this system working.
1. ESP8266 running Micropython. I am using a Wemos D1 mini V2 easily found on ebay. There are multiple guides online that explain how to install micropython on the device. Make sure to clear the flash first.
2. The Device Handler must be added to SmartThings via the SmartThings IDE and published for your hub. This will be the dashboard for the device created.
3. A Smart App must also be added to SmartThings and published for your hub. The Smart App handles incoming LAN requests and updates the device based on the data.
4. A soil moisture sensor. The cheap resistive ones corrode. I use these slightly more expensive capacitive sensors: https://www.digikey.com/products/en?mpart=SEN0193&v=1738

# Some Notes:
The Smart App will automatically create a device based on the MAC address of the ESP8266. Once you have everything working properly, the first time a ESP8266 connects and sends data a new device will appear in your SmartThings "Things". From then on, the Smart App will update that same device when new data arrives. If you have multiple devices it will create a new "Thing" for each device since the MAC address will be unique. This means a single smart app will create and update as many devices as you want. You could even update the Smart App to push data to multiple different device types or combine multiple ESP8266 devices into a single "Thing".

I am using a cheap OLED display based on the ssd1306 driver over I2C. If you do not have a screen connected the micropython main.py script will throw an error. You can comment out all of the display updates to run without a screen.

If you leave sleep enabled you must connect the RST pin to D0

You will need to update the SSID and password in main.py to connect to your wifi network

Use the Python esptool (pip install esptool) to erase flash pip install esptool

I use https://github.com/nodemcu/nodemcu-flasher to flash firmware

I use ESPlorer to test code on the D1 Mini https://esp8266.ru/esplorer/

I use WebREPL to load the main.py onto the D1 mini "import webrepl_setup" in the REPL

Right now there is no way for the SmartHub to talk to the ESP8266. This project would be a good reference for adding that capability https://github.com/hobbzey/Simplest-SmartThings-ESP8266-Blinds note that it uses the Arduino IDE for the ESP8266 instead of Micropython but the concept is similar.
