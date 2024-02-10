import paho.mqtt.client as paho
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import yaml
import time

# Attempt to open and load the configuration file
try:
    with open('mqtt_config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        print(f'Loaded config!')
except IOError:
    print("missing mqtt_config.yaml file, please create one.")
    exit()

class MQTTListener():
    def __init__(self):
        self.client = paho.Client(config['CLIENT_NAME'], clean_session=True, reconnect_on_failure=True)
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.scroller = ScrollingText()
        self.config = config

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f'Subscribed: {str(mid)} {str(granted_qos)}')

    def on_message(self, client, userdata, msg):
        payload = yaml.load(msg.payload.decode("utf-8"), Loader=yaml.FullLoader)
        print("msg.topic "+ str(msg.qos)+ " " +payload["text"])
        self.scroller.scroll_text(payload['text'], payload['color'])
    
    def start(self):
        self.client.connect(config['BROKER_IP'], config['BROKER_PORT'])
        self.client.subscribe(config['TOPIC'], qos=config['QOS'])
        self.client.loop_forever()

class ScrollingText():
    def __init__(self):
        # Set up the LED matrix properties
        options = RGBMatrixOptions()
        options.rows = config['ROWS']
        options.cols = config['COLUMNS']
        options.chain_length = config['CHAIN_LENGTH']
        options.parallel = config['PARALLEL_CHAINS']
        options.pwm_bits = config['PWM_BITS']
        options.pwm_lsb_nanoseconds = config['PWM_LSB_NANOSECONDS']
        options.brightness = config['BRIGHTNESS']
        options.scan_mode = config['SCAN_MODE']
        options.multiplexing = config['MULTIPLEXING']
        options.row_address_type = config['ROW_ADDRESS_TYPE']
        options.disable_hardware_pulsing = config['DISABLE_HARDWARE_PULSING']
        options.gpio_slowdown = config['SLOWDOWN_GPIO']
        options.hardware_mapping = config['HARDWARE_MAPPING']
        options.limit_refresh_rate_hz = config['LIMIT_REFRESH_RATE_HZ']
        self.matrix = RGBMatrix(options = options)
    
    def scroll_text(self, text: None, color: tuple):
        self.matrix.Clear()
        
        #creates the canvas and loads the text properties
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(config['FONT'])
        textColor = graphics.Color(color[0], color[1], color[2])
        pos = canvas.width
        
        # Loop through rendering the text
        while pos + len(text) * 7 > 0:
            canvas.Clear()
            length = graphics.DrawText(canvas, font, pos, 10, textColor, text)
            pos -= 1 # Move left change for speed
            time.sleep(0.05) # scroll smoothness
            canvas = self.matrix.SwapOnVSync(canvas)

mqtt_listenter = MQTTListener()
mqtt_listenter.start()