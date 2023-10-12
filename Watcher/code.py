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
import supervisor
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

class Sensor:
    def __init__(self, i2c, setup_func, items):
        self.i2c = i2c
        self.setup_func = setup_func
        self.items = items  # This will be a list of SensorItem instances.
        self.instance = self.setup_func(self.i2c)

class SensorItem:
    def __init__(self, mqtt_topic, read_func):
        self.accumulated_value = 0
        self.read_func = read_func
        self.mqtt_topic = mqtt_topic

def init():
    global sensors
    global sampleTime
    global mqttClient
    global io
    global feed_names
    
    sampleTime = config['sampleTime']
    wifi.radio.connect(secrets['ssid'], secrets['password'])
    pool = socketpool.SocketPool(wifi.radio)
    
    if (config['useSD']):
        import sdcardio
        import storage
        spi = busio.SPI(board.GP2, board.GP4, board.GP3)  # SCK, MISO (RX), MOSI (TX)
        cs = digitalio.DigitalInOut(board.GP5)  # CS
        sdcard = sdcardio.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
    
    if (config['useMQTT']):
        mqttTopic = config['mqttTopic']
        mqttBrokerIp = config['mqttBrokerIp']
        mqttBrokerPort = config['mqttBrokerPort']

        mqttClient = MQTT.MQTT(
            broker=mqttBrokerIp,
            port=mqttBrokerPort,
            socket_pool=pool,
        )

        mqttClient.will_set(mqttTopic, "OFFLINE", 1)
        mqttClient.connect(keep_alive = sampleTime * 2 + 5)
        
    if (config['useAdafruitIO']):
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        io = IO_HTTP(secrets['aio_username'], secrets['aio_key'], requests)
        
        try:
            aio_feed_7341 = io.get_feed("pi7341")
        except AdafruitIO_RequestError:
            aio_feed_7341 = io.create_new_feed("pi7341")
            
        feed_names = [aio_feed_7341]

    i2c0 = busio.I2C(board.GP1, board.GP0, frequency=100000)
    #i2c1 = busio.I2C(board.GP3, board.GP2, frequency=100000)
    
    sensors = []

    if (config['useAS7341']):
        import adafruit_as7341
        as7341_setup_func = lambda i2c: adafruit_as7341.AS7341(i2c)
        as7341_items = [
            SensorItem(read_func=lambda sensor: sensor.channel_clear, mqtt_topic=f"{mqttTopic}/7341/clear"),
            SensorItem(read_func=lambda sensor: sensor.channel_nir, mqtt_topic=f"{mqttTopic}/7341/nir"),
            SensorItem(read_func=lambda sensor: sensor.channel_415nm, mqtt_topic=f"{mqttTopic}/7341/415"),
            SensorItem(read_func=lambda sensor: sensor.channel_445nm, mqtt_topic=f"{mqttTopic}/7341/445"),
            SensorItem(read_func=lambda sensor: sensor.channel_480nm, mqtt_topic=f"{mqttTopic}/7341/480"),
            SensorItem(read_func=lambda sensor: sensor.channel_515nm, mqtt_topic=f"{mqttTopic}/7341/515"),
            SensorItem(read_func=lambda sensor: sensor.channel_555nm, mqtt_topic=f"{mqttTopic}/7341/555"),
            SensorItem(read_func=lambda sensor: sensor.channel_590nm, mqtt_topic=f"{mqttTopic}/7341/590"),
            SensorItem(read_func=lambda sensor: sensor.channel_630nm, mqtt_topic=f"{mqttTopic}/7341/630"),    SensorItem(read_func=lambda sensor: sensor.channel_680nm, mqtt_topic=f"{mqttTopic}/7341/680"),
        ]
        as7341_sensor = Sensor(i2c=i2c0, setup_func=as7341_setup_func, items=as7341_items)        
        sensors.append(as7341_sensor)

    if (config['useLTR390']):
        import adafruit_ltr390
        ltr390_setup_func = lambda i2c: adafruit_ltr390.LTR390(i2c)
        ltr390_items = [
            SensorItem(read_func=lambda sensor: sensor.uvs, mqtt_topic=f"{mqttTopic}/390/uv"),
            SensorItem(read_func=lambda sensor: sensor.light, mqtt_topic=f"{mqttTopic}/390/light"),
        ]
        ltr390_sensor = Sensor(i2c=i2c0, setup_func=ltr390_setup_func, items=ltr390_items)
        sensors.append(ltr390_sensor)
        
    if (config['useMMC5603']):
        import adafruit_mmc56x3
        mmc5603_setup_func = lambda i2c: adafruit_mmc56x3.MMC5603(i2c)
        mmc5603_items = [
            SensorItem(read_func=lambda sensor: sensor.magnetic[0], mqtt_topic=f"{mqttTopic}/5603/x"),
            SensorItem(read_func=lambda sensor: sensor.magnetic[1], mqtt_topic=f"{mqttTopic}/5603/y"),
            SensorItem(read_func=lambda sensor: sensor.magnetic[2], mqtt_topic=f"{mqttTopic}/5603/z"),
            SensorItem(read_func=lambda sensor: sensor.temperature, mqtt_topic=f"{mqttTopic}/5603/temperature"),
        ]
        mmc5603_sensor = Sensor(i2c=i2c0, setup_func=mmc5603_setup_func, items=mmc5603_items)
        sensors.append(mmc5603_sensor)

    if (config['useSHTC3']):
        import adafruit_shtc3
        shtc3_setup_func = lambda i2c: adafruit_shtc3.SHTC3(i2c)
        shtc3_items = [
            SensorItem(read_func=lambda sensor: sensor.temperature, mqtt_topic=f"{mqttTopic}/shtc3/temperature"),
            SensorItem(read_func=lambda sensor: sensor.relative_humidity, mqtt_topic=f"{mqttTopic}/shtc3/humidity"),
        ]
        shtc3_sensor = Sensor(i2c=i2c0, setup_func=shtc3_setup_func, items=shtc3_items)
        sensors.append(shtc3_sensor)


def log_to_sd(data):
    with open("/sd/log.txt", "a") as f:
        f.write(data + "\n")

def resetVariables():
    global count
    global lastSendTime
    
    for sensor in sensors:
        for item in sensor.items:
            item.accumulated_value = 0    
    
    count = 0
    lastSendTime = time.time()

init()
resetVariables()

try:
    while True:

        count += 1
        
        for sensor in sensors:
            for item in sensor.items:
                item.accumulated_value += item.read_func(sensor.instance)

        if ((time.time() - lastSendTime) > sampleTime):
            if(count > 0):
#                if (config['useAdafruitIO']):
#                    print(f"sending {value_7341_clear}")
#                    for z in range(1):
#                        io.send_data(feed_names[z]["key"], value_7341_clear) 
                
                if (config['useSD']):
                    log_data = ""
                    for sensor in sensors:
                        for item in sensor.items:
                            value = item.accumulated_value / count
                            log_data += f"{item.mqtt_topic}: {value}, "
                    log_to_sd(log_data.rstrip(", "))
                if (config['useMQTT']):
                    for sensor in sensors:
                        for item in sensor.items:
                            value = item.accumulated_value / count
                            mqttClient.publish(item.mqtt_topic, value)
                            
        time.sleep(.5)
except Exception as e:
    print(f"Caught exception: Type: {type(e)} Args: {e.args} Msg: {e}")
    try:
        mqttClient.publish(f"light1/error", e)
    except Exception as f:
        print(f"Caught another exception: {f}")
    supervisor.reload()
