'''
    Cycflix.py
    This script opens up Netflix on a PC, signs the user in(if sign details were saved),
    asks the user to input details for a Spinning workout and once the user chooses something to 
    watch, the workout starts. The PC is connected to an arduino reading in the speed from an stationary
    exercise bike, if the speed goes too low, Netflix will be paused until they return to that speed
    Written By Ronan Byrne, last updated 06/07/2017
    Blog: https://roboroblog.wordpress.com/
    Instructables Post:
    
'''

#!/usr/bin/env python
import time, serial
import serial.tools.list_ports as list_ports
from tkinter import *
from selenium import webdriver as wd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# If the X button is pressed, exit application
def window_exit():
    global driver, win, ser
    if driver:
        driver.quit()
    if win:
        win.destroy()
    if ser:
        ser.close()
    exit()

# Function for getting exercise info
def exercise_info():
    def button_press():
        global work_time, rest_time, sets, time_pause, work_nom_speed, rest_nom_speed
        work_time = int(float(e1.get())*60.0)
        rest_time = int(float(e2.get())*60.0)
        sets = int(e3.get())
        time_pause = int(float(e4.get())*60.0)
        work_nom_speed = float(e5.get())
        rest_nom_speed = float(e6.get())
        win.destroy()
    global win
    win = Tk()
    win.wm_title("Exercise Info")
    Label(text="Active Time(min)").grid(row=1, column=1)
    e1 = Entry(bd=5)
    e1.insert(END, 15)
    e1.grid(row=1, column=2)
    Label(text="Rest Time(min)").grid(row=2, column=1)
    e2 = Entry(bd=5)
    e2.insert(END,5)
    e2.grid(row=2, column=2)
    Label(text="Sets").grid(row=3, column=1)
    e3 = Entry(bd=5)
    e3.insert(END,3)
    e3.grid(row=3, column=2)
    Label(text="Time until pause(min)").grid(row=4, column=1)
    e4 = Entry(bd=5)
    e4.insert(END,1)
    e4.grid(row=4, column=2)
    Label(text="Working Nominal Speed(Km)").grid(row=5, column=1)
    e5 = Entry(bd=5)
    e5.insert(END,30)
    e5.grid(row=5, column=2)
    Label(text="Resting Nominal Speed(Km)").grid(row=6, column=1)
    e6 = Entry(bd=5)
    e6.insert(END, 15)
    e6.grid(row=6, column=2)
    Button(win, text="OK", command=button_press).grid(row=7, column=1, columnspan=2)
    e1.focus_set()
    win.wm_protocol("WM_DELETE_WINDOW", window_exit)
    win.mainloop()


# Pop up window with timeout
def pop_up(title, message, timeout):
    global win

    # Open new window or Toplevel
    try:
        win.state() # win.state returns error if there is no window open
        pop = Toplevel(win)
        pop_is_tk = False
    except Exception as E:
        pop = Tk()
        pop_is_tk = True
    pop.wm_title(title)
    Label(pop,text=message).grid(row=1,column=1)
    Button(pop, text="OK", command=pop.destroy).grid(row=2, column=1, columnspan=1)
    if timeout is not None:
        pop.after(int(timeout*1000.0), pop.destroy)
    if pop_is_tk:
        pop.mainloop()

# Sign into neflix with login.txt or manual input
def sign_in():
    # Function for Manually logging into Netflix
    def manual_login():

        def button_press():
            global email, password
            email = e1.get()
            password = e2.get()
            # Save details if checked
            if save_details:
                email_pass = open('login.txt', 'w+')
                email_pass.write(email + "\n" + password)
                email_pass.close()
            win.destroy()

        global win
        win = Tk()
        win.wm_title("Netflix Details")
        Label(text="Email").grid(row=1, column=1)
        e1 = Entry(bd=5)
        e1.grid(row=1, column=2)
        Label(text="Password").grid(row=2, column=1)
        e2 = Entry(bd=5)
        e2.grid(row=2, column=2)
        save_details = IntVar()
        Checkbutton(text="Save Details", variable=save_details).grid(row=3, column=1, columnspan=2)
        Button(win, text="OK", command=button_press).grid(row=4, column=1, columnspan=2)
        e1.focus_set()
        win.wm_protocol("WM_DELETE_WINDOW", window_exit)
        win.mainloop()

    # Try to find and click sign in button
    try:
        sign_in_butt = driver.find_element_by_link_text('Sign In')
        sign_in_butt.click()
        signing_in = 1
    except Exception as E:
        print('Already signed in')
    if signing_in:
        # Try to open "login.txt" and read in email and password
        try:
            global email, password
            time.sleep(2)
            email_pass = open('login.txt', 'r')
            email = email_pass.readline()
            password = email_pass.readline()
            email_pass.close()
        except Exception as E:
            print('please enter login info manually')
            manual_login()
        while signing_in:
            email_box = driver.find_element_by_name('email')
            email_box.clear()
            email_box.send_keys(email)
            password_box = driver.find_element_by_name('password')
            password_box.clear()
            password_box.send_keys(password)
            driver.find_element_by_css_selector(".login-button").click()
            time.sleep(5)
            if driver.current_url.find('browse') != -1:
                signing_in = False
            else:
                manual_login()

# Let User choose Serial port
def serial_port():
    def ok():
        global ser, port
        port = var.get()
        port = port.split(' - ')
        bracket = '(\''
        port_str_index = port[0].find(bracket)
        if port_str_index != -1:
            port[0] = (port[0])[port_str_index + 2:]
        ser = serial.Serial(port[0], 115200)
        win.destroy()

    global win
    win = Tk()
    win.wm_title('Choose a Serial Port')
    var = StringVar(win)
    var.set("Select the port your Arduino is connected to")
    ports = list(list_ports.comports())
    option = OptionMenu(win, var, ports)
    option.pack(side='left')
    button = Button(win, text="OK", command=ok)
    button.pack()
    win.wm_protocol("WM_DELETE_WINDOW", window_exit)
    win.mainloop()

# Wait for Arduino to respond
def serial_wait():
    global win, ser
    win = Tk()
    win.title("Waiting for Arduino")
    l1 = Label(win, text="Waiting For Arduino to establish connection")
    l1.pack()
    while True:
        print('looping')
        # Wait for arduino to send 'B\r\n'
        if ser.in_waiting >= 1:
            reciev = ser.readline()
            reciev = reciev.decode("utf-8")
            if reciev == 'B\r\n':
                ser.flush()
                ser.write(1)
                print('recieved B')
                win.destroy()
                break
        win.wm_protocol("WM_DELETE_WINDOW", window_exit)
        win.update_idletasks()
        win.update()

port = None
driver = None
win = None
ser = None
serial_port()   # Opens window with Serial ports
serial_wait()   # Wait for Arduino to respond
print('Starting Firefox, it could take a minute to start')
profile = wd.FirefoxProfile('fire_fox_profile') # Firefox profile with "Play DRM" enabled
driver = wd.Firefox(profile)
actions = ActionChains(driver)
driver.get('http://www.netflix.com/')
email = password = None
sign_in()       # Sign into netflix
watch = False

exercise_info() # Get user to enter info for exercise
pop_up("Choose Something to Watch", "Choose Something to Watch and Your Workout Will Start", 5)

# Wait until they pick something to watch
while not watch:
    if driver.current_url.find('watch') != -1:
        watch = True
        driver.refresh() # Refresh to ensure DRM is setup
        time.sleep(2)
    time.sleep(1)


print('watching something')

pop_up("Workout", "Start peddling for %d seconds above %0.2f Km" %(work_time, work_nom_speed), 5)

# Setup workout variables
count = 0
warning = False
working_out = True
case = "Working"
next_event = "Resting"
next_event_time = rest_time
time_to_event = work_time
time_left = work_time
sets = sets-1
nom_speed = work_nom_speed
delay = 0.5

# Open window in top left with workout info
win = Tk()
win.geometry("200x65+0+0")
Round = StringVar(win)
display_time = StringVar(win)
display_speed = StringVar(win)
display_nom_speed = StringVar(win)
Round.set("Working")
display_time.set("Time Remaining %ds" % time_to_event)
display_speed.set("Current Speed is 0 Km")
display_nom_speed.set("Nominal Speed is %.02fKm" % nom_speed)
win.title("Workout Details")
label1 = Label(win,textvariable=Round)
label1.pack()
label2 = Label(win,textvariable=display_speed)
label2.pack()
label3 = Label(win,textvariable=display_nom_speed)
label4 = Label(win,textvariable=display_time)
label4.pack()
win.wm_protocol("WM_DELETE_WINDOW", window_exit)
win.update_idletasks()
win.update()

time_last_event = time.time()
while working_out:
    # Read in latest speed
    if ser.in_waiting > 0:
        speed =float(ser.readline().decode("utf-8"))
        display_speed.set("Current Speed is %0.2f Km" % speed)
    Round.set(case)
    print("speed %.02f, nom speed %.02f, time left %d, round %s" %(speed,nom_speed, int(time_left), case))

    if case == "Resting" or case == "Working":
        time_left = time_to_event - (time.time() - time_last_event)
        display_time.set("Time Remaining %ds" % int(time_left))
        # If they are cycling too slow
        if speed < nom_speed:
            count = count + 1
            if count >= time_pause /(delay * 2):
                # Give Warning
                if not warning:
                    warning = True
                    count = 0
                    pop_up("Cycling Too Slow", "Netflix will pause if you don't get back up to speed, %.02fKm" % nom_speed, 5)
                # Stop Netflix
                else:
                    actions.send_keys(Keys.SPACE)
                    actions.perform()
                    pop_up("Cycling Too Slow For Too Long",
                            "Netflix will continue to play when you get back up to speed, %.02fKm"% nom_speed, 5)
                    old_case = case
                    count = 0
                    case = "Paused"
        else:
            count = 0
            warning = False

        # Current round has ended
        if time_left <= 0 and case is not "Paused":
            case = next_event
            time_to_event = next_event_time
            time_last_event = time.time()
            if case == "Working":
                pop_up("Workout", "Start peddling for %d seconds above %0.2f Km" % (work_time, work_nom_speed), 5)
                sets = sets - 1
                if sets > 0:
                    next_event = "Resting"
                    next_event_time = rest_time
                else:
                    next_event = "Done"
                nom_speed = work_nom_speed
            elif case == "Resting":
                pop_up("Time to Rest",
                       ("Slow down to %.02f for %d seconds with %d sets left" % (rest_nom_speed, rest_time, sets)), 5)
                next_event = "Working"
                next_event_time = work_time
                nom_speed = rest_nom_speed
            display_nom_speed.set("Nominal Speed %.02fKm" % nom_speed)
    elif case == "Paused":
        if speed >= nom_speed:
            count = count + 1
            # Unpause Netflix after 10 delays
            if count == 10:
                actions.send_keys(Keys.SPACE)
                actions.perform()
                count = 0
                time_last_event = time.time()
                time_next_event = time_left+time_last_event
                case = old_case
    elif case == "Done":
        pop_up("You're Done!", "Congratulations, you're finished you're workout!", 5)
        working_out = False
    # Update workout info window
    win.update_idletasks()
    win.update()
    # Request speed form Arduino
    ser.write(1)
    time.sleep(delay)
# Workout Finished
ser.close()
exit()