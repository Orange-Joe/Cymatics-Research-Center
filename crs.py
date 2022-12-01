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
[X] Exit Program  
    
Choose a [Hotkey] or press [C] to run commands."""

def menu():
    global project, medium, start, end, dur, split_files, record_video, camera
    while True:
        print(menu_ui)
        inp = repr(readchar.readchar())
        if inp.lower() == "'p'":
            project = input("Enter new project name: ")
            command = f"mkdir /home/guest/{project}"
            os.system(command)
            os.chdir(f"/home/guest/{project}")
            custom_project = True
        elif inp.lower() == "'m'":
            medium = input("Enter new medium name: ")
        elif inp.lower() == "'s'":
            start = int(input("Choose starting frequency: "))
        elif inp.lower() == "'f'":
            end = int(input("Choose final frequency: "))
        elif inp.lower() == "'d'":
            dur = int(input("Choose duration per frequency: "))
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
        elif inp.lower() == "'x'":
            quit()
        elif inp.lower() == "'c'":
            run_commands()
        os.system('clear')

def multi_frequency(start, end, dur):
    if custom_project is False:
        if os.getcwd() != f'/home/guest/{project}':
            print(f'we are currently not in the {project} directory')
            cur_dir = os.listdir('/home/guest')
            if project not in cur_dir:
                print(f'the {project} is no in /home/guest')
                command = f"mkdir /home/guest/{project}"
                os.system(command)
                os.chdir(f"/home/guest/{project}")
            elif project in cur_dir:
                os.chdir(f'/home/guest/{project}')
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
    while os.path.exists(f"/home/guest/{project}/{file_name}"):
        file_iterator += 1
        constructor = file_name.split()
        constructor[-1] = f"#{str(file_iterator)}"
        file_name = " ".join(constructor)
    return file_name

def run_commands():
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

os.system('clear')
menu()
