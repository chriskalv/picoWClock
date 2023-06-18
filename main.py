##################################
##########  PICO W CLOCK #########
############## BY CK #############
##################################

# Libraries for...
# ...Pimoroni Pico display
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
from pimoroni import Button
# ...Pimoroni Pico led
from pimoroni import RGBLED
# ... native Essentials
import machine
import network
import sys
import utime as time
import usocket as socket
import ustruct as struct
# ...garbage collector
import gc
gc.enable()

# --------------------------------
# --------Global settings---------
# Birthday Wish:
birthday_wish_enabled = 1
birthday_month = 12
birthday_day = 5
# WiFi Config:
wlanSSID = 'YOURWIFISSIDHERE'
wlanPW = 'YOURPASSWORDHERE'
network.country('XY')
# List of WiFi country codes: https://techhub.hpe.com/eginfolib/networking/docs/routers/msrv5/cr/5200-2344_wlan-cr/content/459293642.htm
# --------------------------------

# Set up global variables for Hardware
# Pimoroni Pico Display
brightness = 0.6
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=0)
width, height = display.get_bounds()
display.set_backlight(brightness)
# Pimoroni Pico led
led = RGBLED(6, 7, 8)
led.set_rgb(0,0,0)
# Pico Status LED
led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
# Language
language = 0
# Display formatting
showseconds = 0
# Colors
black = display.create_pen(0, 0, 0)
white = display.create_pen(255, 255, 255)
orange = display.create_pen(255, 128, 0)
# Buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# Clear the screen once
display.set_pen(black)
display.clear()
display.update()

# NTP Host
NTP_HOST = 'pool.ntp.org'

# Function: Connect to WiFi
def wlanConnect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connect to WiFi')        
        wlan.active(True)
        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            led_onboard.toggle()
            print('.')
            time.sleep(1)
    if wlan.isconnected():       
        print('WiFi Connection established / WiFi Status:', wlan.status())
        led_onboard.on()
    else:
        print('No WiFi Connection')
        led_onboard.off()
        print('WiFi Status:', wlan.status())
        
# Function for checking button B (switch language)
def buttoncheck_b():
    if button_b.read():
        global language
        language += 1
        if language >= 4:
            language = 0
        return language

# Function for checking button A (brightness adjustment down)
def buttoncheck_a():
    if button_a.read():
        global brightness
        brightness -= 0.1
        if brightness <= 0.2:
            brightness = 0.2
        return brightness

# Function for checking Button X (brightness adjustment up)
def buttoncheck_x():
    if button_x.read():
        global brightness
        brightness += 0.1
        if brightness >= 0.8:
            brightness = 0.8
        return brightness

# Function for checking button Y (show/hide seconds)
def buttoncheck_y():
    if button_y.read():
        global showseconds
        showseconds += 1
        if showseconds >= 2:
            showseconds = 0
        return showseconds
    
# Function: Get Time via NTP
def getTimeNTP():
    NTP_DELTA = 2208988800
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    ntp_time = struct.unpack("!I", msg[40:44])[0]
    return time.gmtime(ntp_time - NTP_DELTA)

# Define corridors for daylight savings time (the time is supposed to be altered on the last Sunday of March and the last Sunday of October)
def is_sunday(year, month, day):
    t = (year, month, day, 0, 0, 0, 0, 0)
    return time.localtime(time.mktime(t))[6] == 6
    
def last_sunday_in_month(year, month):
    for day in range(31, 26, -1):
        if is_sunday(year, month, day):
            return day
    return None

# Function: Set RTC time
def setTimeRTC():
    # Get NTP time
    tm = getTimeNTP()
    
    # Check for daylight savings time
    year, month, day, hours, _, _, _, _ = tm
    last_sunday_in_march = last_sunday_in_month(year, 3)
    last_sunday_in_october = last_sunday_in_month(year, 10)

    # Check for "real" date and change accordingly
    if ((month > 3 or (month == 3 and day > last_sunday_in_march)) and (month < 10 or (month == 10 and day <= last_sunday_in_october))):
        hours += 1
        if hours == 24:
            hours = 0
            day += 1
            if (month in [4, 6, 9, 11] and day == 31) or (month in [1, 3, 5, 7, 8, 10, 12] and day == 32) or (month == 2 and day == 29):
                day = 1
                month += 1
                if month == 13:
                    month = 1
                    year += 1
    tm = (year, month, day, hours, tm[4], tm[5], tm[6], tm[7])       
    
    # Set time and add +1 to 'hours' because of GMT+1 timezone
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3] + 1, tm[4], tm[5], 0))

# Connect to WiFi
wlanConnect()

# Set time
setTimeRTC()

# Form human-readable time, date and days of the week
def readable():
    tm = machine.RTC().datetime()
    hours, minutes, seconds = tm[4], tm[5], tm[6]
    year, month, day = tm[0], tm[1], tm[2]
    weekday = tm[3]
    
    # Set language for days of the week
    global language
    if language == 0:
        days = {0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'}
    elif language == 1:
        days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    elif language == 2:
        days = {0: 'Domingo', 1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Sábado', 6: 'Domingo'}
    elif language == 3:
        days = {0: 'Dimanche', 1: 'Lundi', 2: 'Mardi', 3: 'Mercredi', 4: 'Jeudi', 5: 'Vendredi', 6: 'Samedi'}
        
    # Implement a birthday wish
    global birthday_wish_enabled
    if birthday_wish_enabled == 1 and day == birthday_day and month == birthday_month:
        days = {0: 'Happy B-Day!', 1: 'Happy B-Day!', 2: 'Happy B-Day!', 3: 'MHappy B-Day!', 4: 'Happy B-Day!', 5: 'Happy B-Day!', 6: 'Happy B-Day!'}
    else:
        pass
    
    # Return the variables
    return {
        "time_full": f"{hours:02d}:{minutes:02d}:{seconds:02d}",
        "time_short": f"{hours:02d}:{minutes:02d}",
        "date": f"{day:02d}.{month:02d}.{year}",
        "weekday": days[weekday],
    }

while True:
    # Load and specify time variables, set text size variables, and generate x coordinates to center text properly
    # Syntax of dispaly text is display.text(text, x-coordinates, y-coordinates, wordwrap after x pixels, scale, angle, spacing)
    readable_var = readable()
    time_short = readable_var["time_short"]
    time_full = readable_var["time_full"]
    weekday = readable_var["weekday"]
    date = readable_var["date"]
    
    time_short_scale = 14
    time_full_scale = 9
    weekday_scale = 5
    date_scale = 6
    
    time_short_width = display.measure_text(time_short, time_short_scale)
    time_full_width = display.measure_text(time_full, time_full_scale)
    weekday_width = display.measure_text(weekday, weekday_scale)
    date_width = display.measure_text(date, date_scale)
    
    time_short_x = round(160 - (time_short_width // 2))
    if time_short_x < 0:
        time_short_x = 0
    time_full_x = round(160 - (time_full_width // 2))
    if time_full_x < 0:
        time_full_x = 0
    weekday_x = round(160 - (weekday_width // 2 ))
    if weekday_x < 0:
        weekday_x = 0
    date_x = round(160 - (date_width // 2))
    if date_x < 0:
        date_x = 0
    
    # Check all the buttons!
    buttoncheck_a()
    buttoncheck_b()
    buttoncheck_x()
    buttoncheck_y()
    
    # Set display brightness
    display.set_backlight(brightness)

    # Clear the display
    display.set_pen(black)
    display.clear()
    
    # Choose a white color and draw the time
    display.set_pen(white)
    if showseconds == 0:
        display.text(time_short, time_short_x, 18, 320, time_short_scale)
    else:
        display.text(time_full, time_full_x, 48, 320, time_full_scale)
    
    # Choose an orange color and draw the day of the week and the date
    display.set_pen(orange)
    display.text(weekday, weekday_x, 140, 240, weekday_scale)
    display.text(date, date_x, 180, 240, date_scale)
    
    # Update the display and wait one second before executing the script again
    display.update()
    time.sleep(1)
