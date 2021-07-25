# morsePico
One Button Morse Code USB Keyboard

This one button keyboard can output all of the standard letters, numbers, and symbols on a US Layout keyboard.

A physical button is connected between ground and GP10 for input. The built in LED is used to show when the button is being pressed. 

To get the code running circuit python needs to be flashed to the pico. The UF2 firmware I used is included but it is possible that newer releases may continue to work. The uf2 file is placed in the root directory of a mounted pico and then it automatically reboots once it is ready. 

The Adafruit hid library folder then needs to be copied over to the pico, along with code.py which contains the morse code logic. 

Speed settings for the recognized dit length, and the delay between character recognition can be modified as needed. These values are defined near the top of the code. 

A pdf of all the recognized characters is included to assist with memorization. I like to also place this onto the pico's storage as there is plenty of room for it. The main characters are all standard international morse code, but there are many extra ones and the patterns for these have been copied from Google's wonderful Gboard android app. 

Using these additional standard definitions from Gboard all the rest of the standard symbols on a US Layout keyboard can be entered, as well as the Enter, Space, Backspace, and Shift key.

When inputting a Shift key there is no visible output at first, but the Shift key will be applied to the next character typed. This is the standard practice that is also used in Gboard. In this way all of the letters can be capitalized. 

I have found that arcade button's fit very precisely into many prescription medication bottles. Bottles like these can be turned into the entire keying device and provide a comfortable grip. I've filled the rest of the bottle in my keying unit carefully with hot glue to give it a better weight and to keep everything securely in place. Sections of inner tube, athletic tape, or similar can be placed around the bottle to make it even more comfortable to hold for extended periods.  
