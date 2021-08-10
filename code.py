# One Button Morse Code - HID USB Keyboard 
# Using CircuitPython and Raspberry Pi Pico
# Gboard definitons included for special characters
# 08.09.2021 Spike Snell 

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

# Set auto spacing to true by default
# Entering SHIFT ( ....-. ) and then SPACE ( ..-- ) toggles autospacing
autoSpace = True

# Set capslock to false by default
# Entering SHIFT ( ....-. ) and then ENTER( .-.- ) toggles capslock
capslock = False

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

# Initilize the time count
TimeCount = 0

# Initilize character lookup delay count
DelayCount = 0

# Initialize the current character string
CurrentKey = ''

# Initialize the shift mode
shiftMode = False

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

# Handle SHIFT shortcuts
def shiftHandler():

    # Use the global values of our flags
    global lastKeyPrintable, shiftMode, mute, autoSpace, capslock, key

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

    # If we are already in shift mode
    if shiftMode == True:

        # If the key entered was SPACE
        if key == ' ':
                        
            # Toggle auto space
            autoSpace = not autoSpace

        # If the key entered was ENTER
        if key == '\n':

            # Toggle capslock
            capslock = not capslock

        # If the key entered was BACKSPACE
        if key == '\b':

            # Press backspace 5 times
            kl.write('\b\b\b\b\b')

        # If the key entered was 1
        if key == '1':

            # Press alt + 1
            keyboard.press(Keycode.ALT, Keycode.ONE)

        # If the key entered was 2
        if key == '2':

            # Press alt + 2
            keyboard.press(Keycode.ALT, Keycode.TWO)

        # If the key entered was 3
        if key == '3':

            # Press alt + 3
            keyboard.press(Keycode.ALT, Keycode.THREE)

        # If the key entered was 4
        if key == '4':

            # Press alt + 4
            keyboard.press(Keycode.ALT, Keycode.FOUR)

        # If the key entered was 5
        if key == '5':

            # Press alt + 5
            keyboard.press(Keycode.ALT, Keycode.FIVE)

        # If the key entered was 6
        if key == '6':

            # Press alt + 6
            keyboard.press(Keycode.ALT, Keycode.SIX)

        # If the key entered was 7
        if key == '7':

            # Press alt + 7
            keyboard.press(Keycode.ALT, Keycode.SEVEN)

        # If the key entered was 8
        if key == '8':

            # Press alt + 8
            keyboard.press(Keycode.ALT, Keycode.EIGHT)

        # If the key entered was 9
        if key == '9':

            # Press alt + 9
            keyboard.press(Keycode.ALT, Keycode.NINE)

        # If the key entered was 0
        if key == '0':

            # Press alt + 0
            keyboard.press(Keycode.ALT, Keycode.ZERO)

        # Release all the keys
        keyboard.release_all();
            
# Loop forever
while True:

    # If the button is pressed
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

    # Else if the button is not pressed
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

                # Run the SHIFT handler
                shiftHandler()

                # If we actually found the key in our dictionary
                if key != '':

                    # Set last key printable flag back to false each time we have a key
                    lastKeyPrintable = False
                       
                    # If we are not in shift mode
                    if shiftMode == False:

                        # If capslock is on uppercase the key
                        if capslock == True:

                            # Uppercase the key
                            key = key.upper()

                        # Write the current key on the us layout
                        kl.write(key)

                        # Check to see if we can set last char printable flag
                        if ( ( key != ' ' )  and 
                             ( key != '\n' ) and 
                             ( key != '\b' ) 
                        ):

                            # Set last key printable flag to true
                            lastKeyPrintable = True

                    # Else we are in shift mode
                    else:

                        # Set shift mode to false
                        shiftMode = False

                        # Check to see if we can set last char printable flag
                        if ( ( key != ' ' )  and 
                             ( key != '\n' ) and 
                             ( key != '\b' ) and
                             ( key != '0' )  and
                             ( key != '1' )  and
                             ( key != '2' )  and
                             ( key != '3' )  and
                             ( key != '4' )  and
                             ( key != '5' )  and
                             ( key != '6' )  and
                             ( key != '7' )  and
                             ( key != '8' )  and
                             ( key != '9' )
                        ):

                            # Write the current key uppercased on the us layout
                            kl.write(key.upper())
                                
                            # Set last key printable flag to true
                            lastKeyPrintable = True

                # Set the current letter back to an empty string    
                CurrentKey = ''

            # After a longer timeout
            if DelayCount > ( dit * mult ) * 3:

                # If auto spacing is true and the last key was printable
                if ( ( autoSpace == True ) and ( lastKeyPrintable == True ) ):

                    # Write a space to the screen
                    kl.write(' ')

                    # Set last key printable flag back to false
                    lastKeyPrintable = False


    # Sleep one unit of time            
    sleep(0.01)
