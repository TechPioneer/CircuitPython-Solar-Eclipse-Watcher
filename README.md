# Eclipse Sensor Pack

## The October 2023 Solar Eclipse

On October 14th 2023, an annular eclipse will occur over a swath of the US, starting at aronud 9:15am PDT
in Eugene, Oregon and ending around 11:45am CDT in Corpus Christi, Texas. You can use
[NASA's Eclipse Explorer](https://svs.gsfc.nasa.gov/webapps/eclipse-explorer/)
to find what the eclipse will be like at your location and when the maximum occulsion will occur.

Unlike a total eclipse, an annular eclipse occurs when the Moon covers the center of the Sun,
leaving a ring-like appearance called the "ring of fire." This happens when the Moon is too
far from Earth to completely cover the Sun's disk.

While the best view will only be visible for those in a narrow band, every US state will
experience at least some solar dimming, so even if you're far from the path of annularity, there
will still be something to see.

For more information on the eclipse, please see NASA's site:
https://science.nasa.gov/eclipses/future-eclipses/eclipse-2023/

## This Project

This project provides Python code intended to work with CircuitPython to collect some potentially interesting
data from the eclipse. It will record the intensity of light at a variety of wavelengths, starting in the infrared,
spanning through the visible spectrum, and ending at UV. It also collects magnometer readings, temperature, and humidity.

If you don't have the same sensors that I do, that's fine, as I've got them all guarded by toggles in the config.py file,
so you can disable any that you don't have. While I was setting this project up, I tested with a variety of other sensors
and I've left those available as options too.

The data is either recorded locally to an SD-card (a work-in-progress), uploaded to [Adafruit IO](https://io.adafruit.com), or uploaded
to the MQTT server of your choice.

Post-eclipse, I'm planning on updating this project with some code to do data analysis. I'm not exactly sure what will be able
to be derived from these sensors, but there will be plenty of data to work with to do some interesting citizen science.
This could also be the basis of an interesting science fair project.

There's another eclipse coming in 2024, so I'm planning on using this as a dry-run for that. After this eclipse, I'll continue
to refine this project so that we'll be able to collect and analyze even more data for that eclipse.

## Parts List

You'll need the following parts:

- [Raspberry Pi Pico W](https://www.adafruit.com/product/5544) Other CircuitPython compatible boards should work, but I haven't tested any.
Since the Pico W doesn't have a Stemma QT plug, you'll need a way to connect it to the sensor breakouts. I chose to use a breadboard with
a Stemma QT to male headers connector. If you're using a board with a Stemma QT plug, then you can skip the next two items.
- [Breadboard](https://www.adafruit.com/product/4539)
- [Stemma QT 4-Pin to Male Headers](https://www.adafruit.com/product/4209)
- [Stemma QT 4-Pin Cable](https://www.adafruit.com/product/4399) for connecting the sensor breakouts together. You'll need several of these (1 per breakout).
- [AS7341 10-Channel Light Sensor Breakout](https://www.adafruit.com/product/4698) This sensor covers the spectrum from infrared through visible light.
- [LTR390 UV Light Sensor Breakout](https://www.adafruit.com/product/4831) This sensor covers the UV end of the spectrum.
- [SHTC3 Temperature and Humidity Breakout](https://www.adafruit.com/product/4636) This sensor measures temperature and humidity.
- [MMC5603 Magnetometer Breakout](https://www.adafruit.com/product/5579) This sensor measure magnetic fields.
- [Swirly](https://www.adafruit.com/product/5774) This is optional, but it's a nice platform for mounting everything.
- [Nylon M2.5 screws](https://www.adafruit.com/product/3658) If you're using the Swirly, then you'll need these to screw the breakouts to it.
- [Neutral Density (ND9) Filter](https://www.amazon.com/Lighting-Neutral-Density-Flashlight-Photography/dp/B08818V6Y2) Direct sunlight is too much for the AS7341 and LTR390 to read directly, so you'll need some ND9 to attenuate it. ND9 blocks light fairly evenly across the infrared through UV spectrum and it blocks 7/8's of the light coming in.

## Setting up the hardware

TODO

## Setting up the code

**Install CircuitPython**
TODO

**Grab the libs**
TODO

**Fill in secrets.py**
TODO

**Configure config.py**
TODO

## Safety Warnings

You know the drill:

- Don't look directly at the Sun, even during an eclipse, unless you're wearing appropriate safety glasses. "Appropriate" means eclipse glasses and nothing else. Sunglasses are not sufficient and will likely result in vision damage.
- Wear your sunscreen.
- Eat your vegetables.

[Eclipse Glasses](https://www.amazon.com/gp/product/B0C2Y3SFVS/)

## 
