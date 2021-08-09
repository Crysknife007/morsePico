# One Button Morse Code - HID USB Keyboard 
# Using CircuitPython and Raspberry Pi Pico
# Gboard definitons included for special characters
# 08.08.2021 Spike Snell 

# Import the required abilities
from time import sleep
from board import LED, GP10, GP15
from digitalio import DigitalInOut, Direction, Pull
from usb_hid import devices
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from pwmio import PWMOut

# Define the dit max length
dit = 13

# Define the multiplyer for character timeout
mult = 3

# Define the volume
vol = 55555

# Define the frequency
freq = 4444

# Set buzzer mute to false by default
# Entering SHIFT ( ....-. ) twice in a row toggles this value
mute = False

# Set auto spacing to false by default
# Entering SHIFT ( ....-. ) and then SPACE ( ..-- ) toggles auto entry of space
autoSpace = False

# Set last key printable flag to false by default
lastKeyPrintable = False

# Define the keyboard
keyboard = Keyboard(devices)

# Define the keyboard layout
kl = KeyboardLayoutUS(keyboard)

# Define the board LED
led = DigitalInOut(LED)

# Set up the LED as an output
led.direction = Direction.OUTPUT

# Define the button 
button = DigitalInOut(GP10)

# Set the button as a pull up input
button.switch_to_input(pull=Pull.UP)

# Define the buzzer
buzzer = PWMOut(GP15, frequency=freq, duty_cycle=0)

# Morse code character dictionary
MorseCodes = {
    'a'  : '.-',
    'b'  : '-...',
    'c'  : '-.-.',
    'd'  : '-..',
    'e'  : '.',
    'f'  : '..-.',
    'g'  : '--.',
    'h'  : '....',
    'i'  : '..',
    'j'  : '.---',
    'k'  : '-.-',
    'l'  : '.-..',
    'm'  : '--',
    'n'  : '-.',
    'o'  : '---',
    'p'  : '.--.',
    'q'  : '--.-',
    'r'  : '.-.',
    's'  : '...',
    't'  : '-',
    'u'  : '..-',
    'v'  : '...-',
    'w'  : '.--',
    'x'  : '-..-',
    'y'  : '-.--',
    'z'  : '--..',
    '0'  : '-----',
    '1'  : '.----',
    '2'  : '..---',
    '3'  : '...--',
    '4'  : '....-',
    '5'  : '.....',
    '6'  : '-....',
    '7'  : '--...',
    '8'  : '---..',
    '9'  : '----.',
    '.'  : '.-.-.-',
    ','  : '--..--',
    '?'  : '..--..', 
    '\'' : '.----.', 
    '!'  : '-.-.--',
    '/'  : '-..-.',
    '('  : '-.--.',
    ')'  : '-.--.-',
    '&'  : '.-...',
    ':'  : '---...',
    ';'  : '-.-.-.',
    '='  : '-...-',
    '+'  : '.-.-.',
    '-'  : '-....-',
    '_'  : '..--.-',
    '@'  : '.--.-.',
    '"'  : '.-..-.',
    '*'  : '...-.',
    '\\' : '-.-.-',
    '%'  : '---.-',
    '#'  : '--.-.',
    '|'  : '--.-.-',
    '^'  : '......',
    '~'  : '.---..',
    '`'  : '-..-.-',
    '$'  : '...-..',
    '['  : '.--..',
    ']'  : '.--..-',
    '{'  : '.--.-',
    '}'  : '.--.--',
    '<'  : '-.---',
    '>'  : '-.----',
    ' '  : '..--',
    '\n' : '.-.-',
    '\b' : '----'
}

# Lookup the right character in the dictionary
def keycodeLookup(keystring):

    # For every item in the dictionary
    for c in MorseCodes:

        # If this is the keycode we are looking for
        if MorseCodes[c] == keystring:

            # Return the matching keycode
            return c

    # If we don't find anything return an empty string
    return ''

# Monitor the button and output characters forever
while True:

    # Initilize the time count
    TimeCount = 0

    # Initilize letter lookup delay count
    DelayCount = 0

    # Initialize the current letter string
    CurrentKey = ''

    # Initialize the shift mode
    shiftMode = False

    # Loop forever
    while True:

        # Button pressed
        if button.value == False:

            # Reset the delay count
            DelayCount = 0

            # Add 1 to the time count
            TimeCount += 1

            # Turn on the LED
            led.value = True

            # As long as the buzzer is not muted
            if mute == False:

                # Turn on the buzzer
                buzzer.duty_cycle = vol

        # Button not pressed
        else:

            # Set the LED to off
            led.value = False
 
            # Turn off the buzzer
            buzzer.duty_cycle = 0

            # If our time count is greater than zero
            if TimeCount > 0:

                # If our time count is less than or equal to our dit length
                if TimeCount <= dit:

                    # Add a dit to our current key
                    CurrentKey = CurrentKey + '.'

                # Else if our time count is greater than the dit length
                elif TimeCount > dit:

                    # Add a dah to our current key
                    CurrentKey = CurrentKey + '-'
            
            # Reset our time count to 0
            TimeCount = 0

            # Add one to our delay count
            DelayCount += 1

            # Else if our delay count is greater than our dit length times the multipler
            if DelayCount > dit * mult:

                # As long as the current key is not an empty string
                if CurrentKey != '':
                   
                    # Lookup the current key
                    key = keycodeLookup(CurrentKey)

                    # If the current key entered was a shift
                    if CurrentKey == '....-.':

                        # Set last key printable flag back to false
                        lastKeyPrintable = False

                        # If shift was entered a second time 
                        if shiftMode == True:
                        
                            # Toggle the buzzer mute
                            mute = not mute

                            # Set shift mode to false
                            shiftMode = False

                        # Else set shift mode to true
                        else: 

                            # Set shift mode to true
                            shiftMode = True

                    # If the current key entered was space
                    if CurrentKey == '..--':

                        # If we are already in shift mode
                        if shiftMode == True:
                        
                            # Toggle auto space
                            autoSpace = not autoSpace

                    # If we actually found the key in our dictionary
                    if key != '':
                       
                        # If we are not in shift mode
                        if shiftMode == False:

                            # Write the current key on the us layout
                            kl.write(key)

                            # Check to see if we can set last char printable flag
                            if ( ( key != ' ' ) and ( key != '\n' ) and ( key != '\b' ) ):
                            
                                # Set last key printable flag to true
                                lastKeyPrintable = True

                        # Else we are in shift mode
                        else:

                            # Set shift mode to false
                            shiftMode = False

                            # Check to see if we can set last char printable flag
                            if ( ( key != ' ' ) and ( key != '\n' ) and ( key != '\b' ) ):

                                # Write the current key uppercased on the us layout
                                kl.write(key.upper())
                                
                                # Set last key printable flag to true
                                lastKeyPrintable = True

                    # Set the current letter back to an empty string    
                    CurrentKey = ''

                # If we need to enter a space here
                if DelayCount > ( dit * mult ) * 3:

                    # If auto spacing is true and the last key was printable
                    if ( ( autoSpace == True ) and ( lastKeyPrintable == True ) ) :

                        # Write a space to the screen
                        kl.write(' ')

                        # Set last key printable flag back to false
                        lastKeyPrintable = False

        # Sleep one unit of time            
        sleep(0.01)
