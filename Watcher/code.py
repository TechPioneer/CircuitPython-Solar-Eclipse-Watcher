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
import supervisor
import adafruit_requests
import adafruit_mmc56x3
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

if (config['useSHTC3']):
    import adafruit_shtc3

def init():
    global as7341
    global ltr390
    global mmc5603
    
    global mqttTopic7341
    global mqttTopic390
    global mqttTopic5603
    global mqttTopicSHTC3
    global sampleTime
    global mqttClient
    global io
    global feed_names
    
    i2c0 = busio.I2C(board.GP1, board.GP0, frequency=100000)
    #i2c1 = busio.I2C(board.GP3, board.GP2, frequency=100000)

    if (config['useAS7341']):
        as7341 = adafruit_as7341.AS7341(i2c0)

    if (config['useLTR390']):
        ltr390 = adafruit_ltr390.LTR390(i2c0)
        
    if (config['useMMC5603']):
        mmc5603 = adafruit_mmc56x3.MMC5603(i2c0)

    if (config['useSHTC3']):
        global shtc3
        shtc3 = adafruit_shtc3.SHTC3(i2c0)

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
        mqttTopic5603 = f"{mqttTopic}/5603"
        if (config['useSHTC3']):
            mqttTopicSHTC3 = f"{mqttTopic}/shtc3"

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
    
    global value_5603_x
    global value_5603_y
    global value_5603_z
    global value_5603_temperature
    
    global value_shtc3_temperature
    global value_shtc3_humidity

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
    
    value_5603_x = 0
    value_5603_y = 0
    value_5603_z = 0
    value_5603_temperature = 0
    
    value_shtc3_temperature = 0
    value_shtc3_humidity = 0
    
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

        if (config['useMMC5603']):
            x, y, z = mmc5603.magnetic
            value_5603_x += x
            value_5603_y += y
            value_5603_z += z
            value_5603_temperature += mmc5603.temperature

        if (config['useSHTC3']):
            value_shtc3_temperature += shtc3.temperature
            value_shtc3_humidity += shtc3.relative_humidity

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

                    if (config['useMMC5603']):
                        mqttClient.publish(f"{mqttTopic5603}/x", value_5603_x/count)
                        mqttClient.publish(f"{mqttTopic5603}/y", value_5603_y/count)
                        mqttClient.publish(f"{mqttTopic5603}/z", value_5603_z/count)
                        mqttClient.publish(f"{mqttTopic5603}/temperature", value_5603_temperature/count)

                    if (config['useSHTC3']):
                        mqttClient.publish(f"{mqttTopicSHTC3}/temperature", value_shtc3_temperature/count)
                        mqttClient.publish(f"{mqttTopicSHTC3}/humidity", value_shtc3_humidity/count)

                resetVariables()

        time.sleep(.5)
except Exception as e:
    print(f"Caught exception: Type: {type(e)} Args: {e.args} Msg: {e}")
    try:
        mqttClient.publish(f"light1/error", e)
    except Exception as f:
        print(f"Caught another exception: {f}")
    supervisor.reload()
