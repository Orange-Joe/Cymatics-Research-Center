import pysine
import os
import readchar
import subprocess
import pysine
import time
from datetime import datetime


current_datetime = datetime.now()
project = f"{str(current_datetime.year)}-{str(current_datetime.month)}-{str(current_datetime.day)}"
custom_project = False
safety_confirmed = False
medium = "Water"
start = 40
end = 40
dur = 5
split_files = False
record_video = True
camera = '/dev/video0'
affirmative = ["'y'", "'t'"] # keypress affirmatives
negative = ["'n'", "'f'"] # keypress negatives
user = os.getlogin()



def menu():
    global project, medium, start, end, dur, split_files, record_video, camera, menu_ui
    while True:
        print(f"""Cymatics Research Station 
[P] Project: {project} 
[M] Medium: {medium}    
[S] Starting Fequency: {start}  
[F] Final Frequency: {end}
[D] Duration Per Frequency: {dur}
[R] Record Video: {record_video}      
[/] Split Video Files: {split_files}
[O] Open Project Directory
[L] Launch VLC
[K] Kill VLC
[W] Scroll Wheel
[X] Exit 
    
Choose a [Hotkey] or press [C] to run commands.""")
        inp = repr(readchar.readchar())
        if inp.lower() == "'p'":
            project = input("Enter new project name: ")
            command = f"mkdir /home/{user}/{project}"
            os.system(command)
            os.chdir(f"/home/{user}/{project}")
            custom_project = True
        elif inp.lower() == "'m'":
            medium = input("Enter new medium name: ")
        elif inp.lower() == "'s'":
            start = scroll_wheel('Choose starting frequency: ', start)
        elif inp.lower() == "'f'":
            end = scroll_wheel('Choose Final Frequency: ', end)
        elif inp.lower() == "'d'":
            dur = scroll_wheel('Choose duration per frequency: ', dur)
        elif inp.lower() == "'r'":
            print("Record video? [y/n] ")
            inp = repr(readchar.readchar())
            if inp.lower() in affirmative:
                record_video = True
            elif inp.lower() in negative: 
                record_video =  False
        elif inp.lower() == "'/'":
            print("Split videos? [y/n] ")
            inp = repr(readchar.readchar())
            if inp.lower() in affirmative:
                split_files = True
            elif inp.lower() in negative: 
                split_files =  False
        elif inp.lower() == "'o'":
            os.system('xdg-open . && exit')
        elif inp.lower() == "'l'":
            command = f"gnome-terminal -- cvlc v4l2://{camera}"
            subprocess.Popen(command, shell=True)         
        elif inp.lower() == "'k'":
            os.system('pkill vlc')
        elif inp.lower() == "'w'":
            scroll_wheel('This is a demo of the scroll wheel. Choose your variable: ', dur)
        elif inp.lower() == "'x'":
            quit()
        elif inp.lower() == "'c'":
            run_commands()
        os.system('clear')

def multi_frequency(start, end, dur):
    if custom_project is False:
        if os.getcwd() != f'/home/{user}/{project}':
            print(f'we are currently not in the {project} directory')
            cur_dir = os.listdir(f'/home/{user}')
            if project not in cur_dir:
                print(f'the {project} is no in /home/{user}')
                command = f"mkdir /home/{user}/{project}"
                os.system(command)
                os.chdir(f"/home/{user}/{project}")
            elif project in cur_dir:
                os.chdir(f'/home/{user}/{project}')
    if start == end:
        file_name = f"{medium} {start} Hz {dur} Seconds.avi #1"
    elif split_files is False:
        if start < end:
            total_dur = abs(dur*(start-end)-dur)
        elif start > end:
            total_dur = abs(dur*(start-end)+dur)
        file_name = f"{medium} {start} to {end} Hz {total_dur} Seconds.avi #1"
    print(f"Writing files to {os.getcwd()}")
    if split_files is False:
        if record_video is True:
            file_name = file_name_creator(start, end, file_name)
            vlc_cmd = f"cvlc v4l2://{camera} --sout='#transcode{{fps=60,scale=1.0,acodec=vorb,ab=90,channels=1,samplerate=22050}}:duplicate{{dst=display,dst=standard{{access= file,mux=avi,dst={file_name}}}}}'"  
            subprocess.Popen(vlc_cmd, shell=True)
        time.sleep(2) # sleep for a moment to let VLC load
        while True:
            print(f"[+] Playing {start} Hz for {dur} seconds.")
            pysine.sine(frequency=start, duration=dur)
            if start < end:
                start += 1
            elif start > end:
                start -= 1
            elif start == end:
                if record_video is True:
                    os.system('pkill vlc') # not elegant.
                    time.sleep(1)
                break
    elif split_files is True:
        while True:
            if record_video is True:
                file_name = f"{medium} {start} Hz {dur} Seconds.avi #1"
                file_name = file_name_creator(start, end, file_name)
                vlc_cmd = f"cvlc v4l2://{camera} --sout='#transcode{{fps=60,scale=1.0,acodec=vorb,ab=90,channels=1,samplerate=22050}}:duplicate{{dst=display,dst=standard{{access=file,mux=avi,dst={file_name}}}}}'"  
                subprocess.Popen(vlc_cmd, shell=True)
            time.sleep(2)   
            print(f"[+] Playing {start} Hz for {dur} seconds.")
            pysine.sine(frequency=start, duration=dur) 
            if start < end:
                start += 1
            elif start > end:
                start -= 1
            elif start == end:
                if record_video is True:
                    os.system('pkill vlc')
                    time.sleep(1)
                break                
            if record_video is True:
                os.system('pkill vlc')
                time.sleep(1)
            
def range(): # This is a barebones function 
    while True:
        start = int(input("CHOOSE FIRST FREQUENCY (in hertz):"))
        end = int(input("CHOOSE FINAL FREQUENCY (in hertz):"))    
        dur = int(input("CHOOSE DURATION (in seconds):"))
        while start <= end:
            print(f"[*] FREQUENCY: {start} HZ")
            pysine.sine(frequency=start, duration=dur)
            start += 1
            os.system('clear')

def file_name_creator(start,end,file_name): # adds +=1 to the file name until it's unique 
    file_iterator = 1
    while os.path.exists(f"/home/{user}/{project}/{file_name}"):
        file_iterator += 1
        constructor = file_name.split()
        constructor[-1] = f"#{str(file_iterator)}"
        file_name = " ".join(constructor)
    return file_name

def run_commands():
    global camera
    command = input("Enter 'start' to begin test or enter other commands: ")
    if command.lower() == 'start':
        multi_frequency(start, end, dur)
    elif command.lower() == 'camera':
        dev_files = os.listdir('/dev')
        print('Found the following camera devices:')
        for i in dev_files:
            if 'video' in i:
                print(i)
        camera = input('Choose a camera, ex: video0\n')
        camera = f'/dev/{camera}'
    elif command == '':
        pass
    else:
        os.system(command)

def scroll_wheel(option, measure):
    counter = measure
    menu_ui = f"""Cymatics Research Station 
[P] Project: {project} 
[M] Medium: {medium}    
[S] Starting Fequency: {start}  
[F] Final Frequency: {end}
[D] Duration Per Frequency: {dur}
[R] Record Video: {record_video}      
[/] Split Video Files: {split_files}
[O] Open Project Directory
[L] Launch VLC
[K] Kill VLC
[W] Scroll Wheel
[X] Exit 
    
Choose a [Hotkey] or press [C] to run commands.
{option}"""
    up = ["'\\x1b'", "'['", "'A'"]
    down = ["'\\x1b'", "'['", "'B'"]
    numbers = ["'1'", "'2'", "'3'", "'4'", "'5'", "'6'", "'7'", "'8'", "'9'", "'0'"]
    r = []
    first_round = True
    while True:
        os.system('clear')
        print(menu_ui+str(counter)+" Hz")
        inp = repr(readchar.readchar())
        if first_round is False:
            if inp == "'\\n'":
                return counter
        if inp == "'\\x1b'":
            r.append(inp)
            inp = repr(readchar.readchar())
            if inp == "'['":
                r.append(inp)
                inp = repr(readchar.readchar())
                if inp == "'A'":
                    r.append(inp)
                    if r == up*3:
                        counter += 1
                        if len(r) >= 9:
                            r.clear()
                elif inp == "'B'":
                    r.append(inp)   
                    if len(r) >= 9:
                        if r == down*3:
                            counter -= 1
                            r.clear()             
        if inp == "'x'":
            quit()
        if inp == "'c'":
            os.system('clear')
        if inp in numbers:
            inp = inp.strip("''")
            counter = int(inp)
            print(menu_ui+str(counter)+" Hz")
            while inp != "'\\n'":
                os.system('clear')
                print(menu_ui+str(counter)+" Hz")
                inp = repr(readchar.readchar())
                if inp in numbers:
                    inp = inp.strip("''")
                    counter = int(str(counter)+inp)
                elif inp == "'\\x08'":
                    if counter != '':
                        if len(str(counter)) > 1:
                            counter = int(str(counter)[0:-1])
                        if len(str(counter)) == 1:
                            counter = 0
                if inp == "'\\n'":
                    return counter
        first_round = False
                
    return counter

os.system('clear')
menu()