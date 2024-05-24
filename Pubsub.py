# Example of subscribing to an Adafruit IO group
# and publishing to the feeds within it

# Author: Brent Rubell for Adafruit Industries, 2018

# Import standard python modules.
import sys
import time
import serial

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient


ADAFRUIT_IO_USERNAME = "Gakotto"
ADAFRUIT_IO_KEY      = "aio_THjB48u8JMFXwLbpDETsH82duMrv"

feedbtn1 = "estado"
feedservo1 = "servo_1"
feedservo2 = "servo_2"
feedservo3 = "servo_3"
feedservo4 = "servo_4"
feedtexto = "texto"

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to topic changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Esperando datos...')
    # Subscribe to changes on a group, group_name
    client.subscribe(feedbtn1)
    client.subscribe(feedservo1)
    client.subscribe(feedservo2)
    client.subscribe(feedservo3)
    client.subscribe(feedservo4)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed topic has a new value.
    # The topic_id parameter identifies the topic, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

    if (feed_id == feedbtn1):
        if (payload == '1'):
            print("Cambiado a siguiente estado.")
            arduino.write(bytes('1\n', 'utf-    8'))
        if (payload == '2'):
            print("Posicion 1.")
            arduino.write(bytes('2\n', 'utf-8'))
        if (payload == '3'):
            print("Posicion 2")
            arduino.write(bytes('3\n', 'utf-8'))
    #if (feed_id == feedbtn4):
        if (payload == '4'):
            print("Posicion 3")
            arduino.write(bytes('4\n', 'utf-8'))
    #if (feed_id == feedbtn5):
        if (payload == '5'):
            print("Posicion 4")
            arduino.write(bytes('5\n', 'utf-8'))
        if (payload == '10'):
            print("Secuencia 1")
            arduino.write(bytes('6\n', 'utf-8'))
        if (payload == '11'):
            print("Secuencia 2")
            arduino.write(bytes('7\n', 'utf-8'))
    if (feed_id == feedservo1):
        print("Servo 1")
        print('6')
        print(payload + '\n')
        #arduino.write(bytes('6', 'utf-8'))
        #time.sleep(1)
        arduino.write(bytes('6' + payload + 'F', 'utf-8'))
    if (feed_id == feedservo2):
        print("Servo 2")
        print('7')
        print(payload + '\n')
        #arduino.write(bytes('7', 'utf-8'))
        #time.sleep(1)
        arduino.write(bytes('7' + payload + 'F', 'utf-8'))
    if (feed_id == feedservo3):
        print("Servo 3")
        print('8')
        print(payload + '\n')
        #arduino.write(bytes('8', 'utf-8'))
        #time.sleep(1)
        arduino.write(bytes('8' + payload + 'F', 'utf-8'))
    if (feed_id == feedservo4):
        print("Servo 4")
        print('9')
        print(payload + '\n')
        #arduino.write(bytes('9', 'utf-8'))
        #time.sleep(1)
        arduino.write(bytes('9' + payload + 'F', 'utf-8'))

try:
    # Create an MQTT client instance.
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    client.on_connect    = connected
    client.on_disconnect = disconnected
    client.on_message    = message

    # Connect to the Adafruit IO server.
    client.connect()

    # Now the program needs to use a client loop function to ensure messages are
    # sent and received.  There are a few options for driving the message loop,
    # depending on what your program needs to do.

    # The first option is to run a thread in the background so you can continue
    # doing things in your program.
    client.loop_background()

    arduino = serial.Serial(port='COM4', baudrate = 9600, timeout = 0.1)

    # Now send new values every 5 seconds.
    #print('Publishing a new message every 5 seconds (press Ctrl-C to quit)...')
    while True:
        mensaje = arduino.readline().decode('utf-8')
        if (mensaje == 'Modo Manual\n'):
            print("Modo Manual")
            client.publish(feedtexto, "Modo: Manual")
        if (mensaje == 'Modo EEPROM\n'):
            print("Modo EEPROM")
            client.publish(feedtexto, "Modo: EEPROM")
        if (mensaje == 'Modo UART\n'):
            print("Modo UART")
            client.publish(feedtexto, "Modo: UART")
        if (mensaje == 'estado3\n'):
            print("estado 3")
            client.publish(feedtexto, "Modo UART")
        time.sleep(3)

except KeyboardInterrupt:
    print("Programa terminado.")
    if arduino.is_open:
        arduino.close()
    sys.exit(1)