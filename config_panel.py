import tkinter as tk
import os
from tkinter import filedialog
class AudioRecorderApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.title("Audio Recorder")
        
        self.label_config_panel = tk.Label(self.window, text="Config Panel")
        self.label_config_panel.pack(pady=10)
        
        self.label_speaker_id = tk.Label(self.window, text="Enter Speaker ID:")
        self.label_speaker_id.pack(pady=10)
        
        self.entry_speaker_id = tk.Entry(self.window)
        self.entry_speaker_id.pack()
        
        self.submit_frame = tk.Frame(self.window)  # Create a frame to hold the label and button
        self.submit_frame.pack()
        
        self.submit_label = tk.Label(self.submit_frame)
        self.submit_label.pack(side=tk.LEFT)
        
        self.button_submit = tk.Button(self.submit_frame, text="Submit", command=self.button_click)
        self.button_submit.pack(side=tk.LEFT)
        
    def button_click(self):
        self.button_submit.pack_forget()
        speaker_id = self.entry_speaker_id.get()
        self.submit_label.config(text="Recording Speaker ID " + speaker_id)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.submit_label.config(text="File saved as: " + file_path)
        else:
            self.submit_label.config(text="File not saved")
            
        if not os.path.exists(__file__):
                os.mkdir(__file__)
        
        # Save the speaker ID to a text file
        with open("speaker_"+speaker_id+".txt", "w") as file:
            file.write(speaker_id)
    
    def run(self):
        self.window.mainloop()

# Create an instance of the AudioRecorderApp class and run the application
app = AudioRecorderApp()
app.run()
