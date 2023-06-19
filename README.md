picoWClock
========================
Instructions to build a pico-based digital table clock showing the 
  + time
  + date 
  + day of the week and
  + temperature (disabled by default).

The clock is the second iteration of my original [picoClock](https://github.com/chriskalv/picoClock), which made use of a RTC module. This version here is able to use the Pico W's WiFi chip to connect to the internet and pull time data from there. The code is entirely micropython-based. Assembly of the device is really easy and even solder-free in case you have a pre-soldered Raspberry Pi Pico W.
<br></br>
| Assembled picoWClock   |
| ------------- |
| [![](https://i.imgur.com/3OQnNtv.jpg?raw=true)](https://i.imgur.com/3OQnNtv.jpg)   |

## Functionality
+ Button A: Adjust brightness (down).
+ Button B: Switch language of the displayed day of the week (German, English, Spanish and French are available).
+ Button X: Adjust brightness (up).
+ Button Y: Show/hide seconds in the time display.

## Hardware
+ [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w)
+ [Pimoroni Pico Display 2.0](https://shop.pimoroni.com/products/pico-display-pack-2-0?variant=39374122582099)

## Setup
1. Flash the custom Pimoroni Pico W MicroPython build onto the board, which already includes the display driver. You can find it [here](https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.20.2). Future releases will probably also work, but I cannot give any guarantees. For this build, v1.20.2 was used.
    - Download the `pimoroni-picow-v[...]-micropython.uf2` file.
    - Push and hold the BOOTSEL button while you plug your Pico into the USB port of your computer. Once plugged in, release the button.
    - The Pico will mount as a mass storage device called _RPI-RP2_.
    - Drag and drop the downloaded file into the _RPI-RP2_ volume.
    
2. Download and install [Thonny](https://thonny.org/), open it, click _Run_ --> _Select interpreter_ and choose _MicroPython (Raspberry Pi Pico)_. This will establish a shell connection to your device.
3. Copy `main.py` over to your device.
4. Check out the **Global Settings** section in the top part of `main.py`. There, you should enter the WiFi SSID, Password and country code of the WiFi you want to connect to from your Pico W. You can also choose to to display "Happy B-Day" instead of the day of the week on one day of the year.

## Case
I did not make a specific case for this build, but [this one](https://www.printables.com/de/model/237722-raspberry-pi-pico-rtc-display-case) from another build uses the same hardware and should fit fairly well.
