import WIFI_CONFIG
from network_manager import NetworkManager
import time
import uasyncio
import time
import ntptime
from picographics import PicoGraphics, DISPLAY_INKY_PACK
from pimoroni import Button


"""
Displays the number days between the current and future date.
Uses the WiFi to set the system date/time.
"""


button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

graphics = PicoGraphics(DISPLAY_INKY_PACK)
graphics.set_font("bitmap8")

WIDTH, HEIGHT = graphics.get_bounds()

def status_handler(mode, status, ip):
    graphics.set_update_speed(2)
    graphics.set_pen(15)
    graphics.clear()
    graphics.set_pen(0)
    graphics.text("Network: {}".format(WIFI_CONFIG.SSID), 10, 10, scale=2)
    status_text = "Connecting..."
    if status is not None:
        if status:
            status_text = "Connection successful!"
        else:
            status_text = "Connection failed!"

    graphics.text(status_text, 10, 30, scale=2)
    graphics.text("IP: {}".format(ip), 10, 60, scale=2)
    graphics.update()


network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)

# Calculate the number of days from the current date to d1
def days_till(d1):
    d1 += (1, 0, 0, 0, 0)
    return time.mktime(d1) // (24*3600) - time.mktime(time.localtime()) //(24*3600)

def update():
    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))

    graphics.set_update_speed(1)
    graphics.set_pen(15)
    graphics.clear()
    graphics.set_pen(0)

    # Update the system date/time
    ntptime.settime()
    t = time.localtime()
    date1 = (2023, 10, 30)
    days_b = days_till(date1)
 
    graphics.text("Days Remaining: {}".format(days_b), 10, 70, scale=2)

    graphics.update()


# Run continuously.
# Be friendly to the API you're using!
while True:
    update()

    while not button_a.is_pressed:
        time.sleep(0.1)
