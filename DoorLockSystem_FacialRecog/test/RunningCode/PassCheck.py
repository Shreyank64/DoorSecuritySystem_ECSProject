#imports for display
import digitalio
import board
import adafruit_character_lcd.character_lcd as characterlcd
import time

#imports for keypad/lock
import RPi.GPIO as GPIO
import time

#setup for lcd
lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D23)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D8)
lcd_d6 = digitalio.DigitalInOut(board.D7)
lcd_d7 = digitalio.DigitalInOut(board.D1)


lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                       lcd_d7, lcd_columns, lcd_rows)

#setup for doorlock

Door_Lock = 21


#setup for keypad
# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

secretCode = "6969"
input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Door_Lock, GPIO.OUT) # to setup door lock
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#displaying input message
lcd.clear()
lcd.message = "Welcome, \nEnter password:"
time.sleep(3)
lcd.clear()

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)


# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def checkSpecialKeys():
    global input
    pressed = False

    GPIO.output(L3, GPIO.HIGH)

    if (GPIO.input(C1) == 1):
        print("Input reset!");
        pressed = True

    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

    if (not pressed and GPIO.input(C3) == 1):
        if input == secretCode:
            lcd.clear()
            lcd.message("Khul jaa sim sim")
            GPIO.output(Door_Lock , GPIO.HIGH)
            time.sleep(5)
            GPIO.output(Door_Lock , GPIO.LOW)

            # TODO: Unlock a door, turn a light on, etc.
        else:
            print("Incorrect input")
            # TODO: Sound an alarm, send an email, etc.
        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        input = ""

    return pressed

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global input
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
        lcd.clear()
        lcd.message = input
        time.sleep(5)        
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
        lcd.clear()
        lcd.message = input
        time.sleep(5)

    if(GPIO.input(C3) == 1):
        input = input + characters[2]
        lcd.message = input
        time.sleep(5)

try:
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        # Otherwise, just read the input
        else:
            if not checkSpecialKeys():
                readLine(L1, ["1","2","3"])
                readLine(L2, ["4","5","6"])
                readLine(L3, ["7","8","9"])
                readLine(L4, ["*","0","#"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")