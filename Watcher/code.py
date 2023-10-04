import time
import wifi
import socketpool
import board
from secrets import secrets
from config import config
from digitalio import DigitalInOut, Direction, Pull
import digitalio
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time
import ssl
import busio
import analogio
import adafruit_as7341
import adafruit_ltr390
import adafruit_apds9960.apds9960
import adafruit_ltr329_ltr303 as adafruit_ltr329
import adafruit_tsl2591
import supervisor
import adafruit_requests
import adafruit_mmc56x3
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

def init():
    global as7341
    global ltr390
    global ltr329
    global apds9960
    global tsl2591
    global mqttTopic7341
    global mqttTopic390
    global mqttTopic9960
    global mqttTopic329
    global mqttTopic2591
    global sampleTime
    global mqttClient
    global io
    global feed_names
    
    i2c0 = busio.I2C(board.GP1, board.GP0, frequency=100000)
    i2c1 = busio.I2C(board.GP3, board.GP2, frequency=100000)

    if (config['useAS7341']):
        as7341 = adafruit_as7341.AS7341(i2c0)

    if (config['useLTR390']):
        ltr390 = adafruit_ltr390.LTR390(i2c0)
        
    if (config['useLTR329']):
        ltr329 = adafruit_ltr329.LTR329(i2c0)

    if (config['useAPDS9960']):
        apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c1)
        apds9960.enable_color = True

    if (config['useTSL2591']):
        tsl2591 = adafruit_tsl2591.TSL2591(i2c1)
        tsl2591.gain = adafruit_tsl2591.GAIN_LOW
        
    if (config['useMMC5603']):
        mmc5603 = adafruit_mmc56x3.MMC5603(i2c0)

    sampleTime = config['sampleTime']
    wifi.radio.connect(secrets['ssid'], secrets['password'])
    pool = socketpool.SocketPool(wifi.radio)
    
    if (config['useAdafruitIO']):
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        io = IO_HTTP(secrets['aio_username'], secrets['aio_key'], requests)
        
        try:
            aio_feed_7341 = io.get_feed("pi7341")
        except AdafruitIO_RequestError:
            aio_feed_7341 = io.create_new_feed("pi7341")
            
        feed_names = [aio_feed_7341]

    if (config['useMQTT']):
        mqttTopic = config['mqttTopic']
        mqttBrokerIp = config['mqttBrokerIp']
        mqttBrokerPort = config['mqttBrokerPort']

        mqttTopic7341 = f"{mqttTopic}/7341"
        mqttTopic390 = f"{mqttTopic}/390"
        mqttTopic9960 = f"{mqttTopic}/9960"
        mqttTopic329 = f"{mqttTopic}/329"
        mqttTopic2591 = f"{mqttTopic}/2591"
        mqttTopic5603 = f"{mqttTopic}/5603"

        mqttClient = MQTT.MQTT(
            broker=mqttBrokerIp,
            port=mqttBrokerPort,
            socket_pool=pool,
        )

        mqttClient.will_set(mqttTopic, "OFFLINE", 1)
        mqttClient.connect(keep_alive = sampleTime * 2 + 5)

def resetVariables():
    global count
    global lastSendTime
    global value_7341_415
    global value_7341_445
    global value_7341_480
    global value_7341_515
    global value_7341_555
    global value_7341_590
    global value_7341_630
    global value_7341_680
    global value_7341_clear
    global value_7341_nir
    
    global value_390_light
    global value_390_uv
    
    global value_9960_red
    global value_9960_green
    global value_9960_blue
    global value_9960_clear
    
    global value_329_full
    global value_329_ir
    
    global value_2591_visible
    global value_2591_infrared
    global value_2591_full
    
    global value_5603_x
    global value_5603_y
    global value_5603_z

    value_7341_415 = 0
    value_7341_445 = 0
    value_7341_480 = 0
    value_7341_515 = 0
    value_7341_555 = 0
    value_7341_590 = 0
    value_7341_630 = 0
    value_7341_680 = 0
    value_7341_clear = 0
    value_7341_nir = 0
    
    value_390_light = 0
    value_390_uv = 0
    
    value_9960_red = 0
    value_9960_green = 0
    value_9960_blue = 0
    value_9960_clear = 0
    
    value_329_full = 0
    value_329_ir = 0
    
    value_2591_visible = 0
    value_2591_infrared = 0
    value_2591_full = 0
    
    value_5603_x = 0
    value_5603_y = 0
    value_5603_z = 0
    
    count = 0
    lastSendTime = time.time()

init()
resetVariables()

try:
    while True:

        count += 1
        
        if (config['useAS7341']):
            value_7341_415 += as7341.channel_415nm
            value_7341_445 += as7341.channel_445nm
            value_7341_480 += as7341.channel_480nm
            value_7341_515 += as7341.channel_515nm
            value_7341_555 += as7341.channel_555nm
            value_7341_590 += as7341.channel_590nm
            value_7341_630 += as7341.channel_630nm
            value_7341_680 += as7341.channel_680nm
            value_7341_clear += as7341.channel_clear
            value_7341_nir += as7341.channel_nir
        
        if (config['useLTR390']):
            value_390_light += ltr390.uvs
            value_390_uv += ltr390.light

        if (config['useAPDS9960']):
            r, g, b, c = apds9960.color_data
            value_9960_red += r
            value_9960_green += g
            value_9960_blue += b
            value_9960_clear += c
            
        if (config['useLTR329']):
            value_329_full += ltr329.visible_plus_ir_light
            value_329_ir += ltr329.ir_light

        if (config['useTSL2591']):
            value_2591_visible += tsl2591.visible
            value_2591_infrared += tsl2591.infrared
            value_2591_full += tsl2591.full_spectrum

        if (config['useMMC5603']):
            x, y, z = mmc5603.magnetic
            value_5603_x += x
            value_5603_y += y
            value_5603_z += z
            value_5603_temperature += mmc5603.temperature

        if ((time.time() - lastSendTime) > sampleTime):
            if(count > 0):
                if (config['useAdafruitIO']):
                    print(f"sending {value_7341_clear}")
                    for z in range(1):
                        io.send_data(feed_names[z]["key"], value_7341_clear) 
                
                if (config['useMQTT']):
                    if (config['useAS7341']):
                        mqttClient.publish(f"{mqttTopic7341}/415", value_7341_415/count)
                        mqttClient.publish(f"{mqttTopic7341}/445", value_7341_445/count)
                        mqttClient.publish(f"{mqttTopic7341}/480", value_7341_480/count)
                        mqttClient.publish(f"{mqttTopic7341}/515", value_7341_515/count)
                        mqttClient.publish(f"{mqttTopic7341}/555", value_7341_555/count)
                        mqttClient.publish(f"{mqttTopic7341}/590", value_7341_590/count)
                        mqttClient.publish(f"{mqttTopic7341}/630", value_7341_630/count)
                        mqttClient.publish(f"{mqttTopic7341}/680", value_7341_680/count)
                        mqttClient.publish(f"{mqttTopic7341}/clear", value_7341_clear/count)
                        mqttClient.publish(f"{mqttTopic7341}/nir", value_7341_nir/count)

                    if (config['useLTR390']):
                        mqttClient.publish(f"{mqttTopic390}/light", value_390_light/count)
                        mqttClient.publish(f"{mqttTopic390}/uv", value_390_uv/count)

                    if (config['useAPDS9960']):
                        mqttClient.publish(f"{mqttTopic9960}/red", value_9960_red/count)
                        mqttClient.publish(f"{mqttTopic9960}/green", value_9960_green/count)
                        mqttClient.publish(f"{mqttTopic9960}/blue", value_9960_blue/count)
                        mqttClient.publish(f"{mqttTopic9960}/clear", value_9960_clear/count)

                    if (config['useLTR329']):
                        mqttClient.publish(f"{mqttTopic329}/full", value_329_full/count)
                        mqttClient.publish(f"{mqttTopic329}/ir", value_329_ir/count)

                    if (config['useTSL2591']):
                        mqttClient.publish(f"{mqttTopic2591}/visible", value_2591_visible/count)
                        mqttClient.publish(f"{mqttTopic2591}/infrared", value_2591_infrared/count)
                        mqttClient.publish(f"{mqttTopic2591}/full", value_2591_full/count)
                        
                    if (config['useMMC5603']):
                        mqttClient.publish(f"{mqttTopic5603}/x", value_5603_x/count)
                        mqttClient.publish(f"{mqttTopic5603}/y", value_5603_y/count)
                        mqttClient.publish(f"{mqttTopic5603}/z", value_5603_z/count)
                        mqttClient.publish(f"{mqttTopic5603}/temperature", value_5603_temperature/count)

                resetVariables()

        time.sleep(.5)
except Exception as e:
    print(f"Caught exception: Type: {type(e)} Args: {e.args} Msg: {e}")
    try:
        mqttClient.publish(f"light1/error", e)
    except Exception as f:
        print(f"Caught another exception: {f}")
    supervisor.reload()