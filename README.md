# Cycflix

## About

This project uses an Arduino connected to a stationary exercise bike to control Netflix. Starting the python script
and inputting some information, Firefox will start to stream Netflix and display in realtime for current workout information such as round, speed, nominal speed for this round and time to next round. If the user goes below the nominal speed for too long, Netflix will pause until the user has gotten back up to speed.

## Instructions

Full details can be found on the Instructables post

Install the required python3 packages and the geckodriver for you system

For the geckodriver, download the one for your system from here and extract it and follow below:

For Windows:

Place the geckdriver.exe in the Cycflix folder, you can place it somewhere else and add to your PATH if you like

For Linux:

Place the geckodriver in /usr/local/bin and type 'geckodriver in you terminal to test it if works

After both of them are setup you can do a test of the script, below is the basic flow of the code(pictures for most steps are above, I show the terminal output for the extra info)

1. Run the python script(running the script in your terminal or IDLE will show some extra information)
2. A popup window will show you all the Serial ports connected to your PC, pick the one connected to your Arduino
3. Another window will popup(I went a bit tkinter crazy with the windows :) ) while you PC waits for a message from your Arduino. Press the reset button on the Arduino if you're waiting too long
Firefox will now start and open the sign in page of Neflix(it could take a few seconds for FireFox to start). If you have you login details saved in the "login.txt", you will be signed in automatically but if you don't, you will be prompted to enter you sign in details with the option to save them for next time
4. You will be prompted to enter in the details for for workout such as work time, work speed, sets, time until pause etc
5. Now the script will wait for you to choose a Programme/Movie to watch and your workout will start
6. During the workout you will see a window in the top left corner of your screen with your current round details such as your speed, time to next round, nominal speed and round. When a round ends, you will see a popup with the details for the next round(this closes after 5 seconds automatically).
If you go below the nominal speed for the current round for half the pause time, you will get a warning saying you are going too slow. If you are still going too slow for the whole pause time, Netflix will be pause until you get back up to speed for a few seconds
7. Once your workout if finished, the script will close but Netflix will remain playing

You shouldn't go fullscreen when watching Netflix as you won't be able to see you current round details.

I did most of my development and testing on Linux Mint, but from doing some quick tests on Windows, it all worked fine

## Contributors

Ronan Byrne

## Other Projects

Visit 
   my Blog: 		    https://roboroblog.wordpress.com/
   my Instructables Post:   https://www.instructables.com/id/Cycflix-Exercise-Powered-Entertainment/
   my Youtube:		    https://youtu.be/-nc0irLB-iY


