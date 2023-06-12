import tkinter as tk
import os
import pandas as pd
from recorder import Recorder
from threading import Event
import pyaudio
import recorder
import threading
import time
import signal
import random
import datetime
from pathlib import Path
class RecorderWindow:
    def __init__(self,win,saved_path:Path,speaker_id):
        self.saved_path = Path(saved_path)
        self.speaker_id = speaker_id
        self.window = win
        self.current_folder = Path(os.getcwd())
        self.current_folder = self.current_folder/"example.xlsx"
        self.sentences = pd.read_excel(self.current_folder)
        
        self.num_list =  list(range(1, 101)) # list from 1 to 100
        self.shuffled_list = random.sample(self.num_list, len(self.num_list))
        
        self.stored_dict = {i+1: self.shuffled_list.index(self.num_list[i])+1 for i in range(len(self.num_list))}
        
        self.current_sentence = 0
      
        # Split the shuffled list into groups of 20
        groups = [self.shuffled_list[i:i+20] for i in range(0, len(self.shuffled_list), 20)]
        
        
        # Access the sentences from the specified column index
        self.sentences = self.sentences.iloc[:, 0].tolist()

        
        self.text = tk.Text(self.window, height=2, width=75,font=("Arial",18))
        self.text.pack()
        self.text.insert(tk.END, self.sentences[self.current_sentence])
        
        previous_button = tk.Button(self.window, text="Previous", command=self.previous_sentence)
        previous_button.pack(side=tk.LEFT)

        next_button = tk.Button(self.window, text="Next", command=self.next_sentence)
        next_button.pack(side=tk.LEFT)
        
        # self.rec_button = tk.Button(self.window, text="Record",bg="red",activebackground='red', command=self.make_recording)
        # self.rec_button.pack(side=tk.RIGHT)
        
        # self.timer_label = tk.Label(self.window, text="",padx=50, pady=50, bd=0)
        # self.timer_label.pack(side=tk.TOP,pady=25)

        
        self.timerFrame = tk.LabelFrame(self.window, padx=10, pady=10, bd=0)
        self.timerFrame_sen = tk.LabelFrame(self.window, padx=10, pady=10, bd=0)

        self.timerFrameText = tk.Label(self.timerFrame, 
            text="Enter time in seconds for recording",
            font=("Arial", 20, "bold")
        )

        self.sen_num = tk.Label( self.timerFrame_sen, 
            text="Sentence index "+str(self.current_sentence+1),
            font=("Arial", 16)
        )
        self.countdownBox= tk.Entry(self.timerFrame, bd=3)
        self.countdownBox.insert(0,15) # 15 sec defult recording 


        self.rec_button = tk.Button(self.timerFrame, 
            padx=5, 
            pady=5, 
            text="Record", 
            font=("Arial", 20),
            bg="red",activebackground='red',
            command= lambda:self.make_recording()
        )

        self.timerFrame.pack(side=tk.TOP)
        self.timerFrameText.pack(side=tk.TOP)
        self.timerFrame_sen.pack(side=tk.TOP)
        self.sen_num.pack(side=tk.TOP)
        self.countdownBox.pack(side=tk.TOP)
        self.rec_button.pack(side= tk.TOP)
        
        self.completeTimer = tk.Label(self.timerFrame, text=" ")
        self.completeTimer.pack()
        
        global rec_button_chanege
        rec_button_chanege = self.rec_button


    def cd(self,timer_label_obj,ts):
        global completeTimer
        while ts > 0:
            # timer_label_obj.config(text=ts)
            ts-=1
            # timer_label_obj.pack()
            time.sleep(1)
            if ts ==0:
            
                completeTimer = tk.Label(self.timerFrame, text="Time is complete")
                completeTimer.pack()


    def countdown(self,t):
        timer = tk.Label(self.timerFrame)
        ts = int(t)
        th = threading.Thread(target=self.cd,args=[timer,ts])
        th.start()
        # self.make_recording() 
       
    def make_recording(self):
        # self.timer_label.config(text="")
                    
        self.completeTimer.config(text="")
        time.sleep(1)
        
        rec_button_chanege.config(text="Recording...",bg = "green")
        rec_button_chanege.update()
        # self.start_timer()

        p = pyaudio.PyAudio()
        device_dict = recorder.list_input_devices(p)
        print("----------------------record device dict---------------------")
        print(device_dict)
        print("-------------------------------------------------------------")
        # device_index = int(input('device index:'))
        
        #choose default device
        device_index = device_dict['default']
                
        r = recorder.Recorder(p, device_index)
        r.record(int(self.countdownBox.get()),self.saved_path/('sentence_'+str(self.current_sentence+1)+"_"+str(datetime.datetime.now())+".wav"),None)
        

        self.rec_button.config(text="Record", bg="red",activebackground='red',command=self.make_recording)
        self.completeTimer.config(text="Time is complete")
        # completeTimer.pack()
        self.completeTimer.update()


        self.rec_button.update()
        
        # self.timer_label.config(text="")
        # self.rec_button.destroy()
    

        
    def previous_sentence(self):
        if self.current_sentence > 0:
            self.current_sentence -= 1
            self.display_sentence()

    def next_sentence(self):
        self.current_sentence
        if self.current_sentence < len(self.sentences) - 1:
            self.current_sentence += 1
            self.display_sentence()

    def display_sentence(self):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, self.sentences[self.current_sentence])
        
        self.sen_num.config(text="Sentence index "+str(self.current_sentence+1))
