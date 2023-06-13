import tkinter as tk
from tkinter import filedialog
import os
from tkinter import filedialog
from record_panel import RecorderWindow
from pathlib import Path
import threading
from tkinter import messagebox
class AudioRecorderApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x300")
        self.window.title("Audio Recorder")
        
        # self.label_config_panel = tk.Label(self.window, text="Config Panel",font=("Arial", 12))
        # self.label_config_panel.pack(pady=10)
        
        self.label_speaker_id = tk.Label(self.window, text="Enter Speaker ID:",font=("Arial", 15))
        self.label_speaker_id.pack(pady=10)
        validate_func = self.window.register(self.validate_input)
        self.entry_speaker_id = tk.Entry(self.window,validate="key",validatecommand=(validate_func, '%P'))
        self.entry_speaker_id.pack()
        
        
        label_gender = tk.Label(self.window, text="Select Gender:",font=("Arial", 15))
        label_gender.pack(pady=10)

        self.selected_gender = tk.IntVar()

        male_button = tk.Radiobutton(self.window, text="Male",font=("Arial", 15), variable=self.selected_gender,command=self.selected_gen, value=1)#, command=self.show_selected_gender)
        male_button.pack()

        female_button = tk.Radiobutton(self.window, text="Female", font=("Arial", 15),variable=self.selected_gender,command=self.selected_gen, value=2)#, command=self.show_selected_gender)
        female_button.pack()
        self.gender = -1
        
        self.sentence_sheet_path = None
        self.browse_frame = tk.Frame(self.window)
        self.browse_frame.pack()
        self.browse_label = tk.Label(self.browse_frame)
        self.browse_label.pack(side=tk.TOP)
        self.button_browse = tk.Button(self.browse_label, text='Browse',command = self.browse_file)
        self.button_browse.pack(side=tk.TOP)
        
        self.submit_frame = tk.Frame(self.window)  # Create a frame to hold the label and button
        self.submit_frame.pack()
        self.submit_label = tk.Label(self.submit_frame)
        self.submit_label.pack(side=tk.TOP)
        
        
        self.button_submit = tk.Button(self.submit_frame, text="Submit", command=self.button_click)
        self.button_submit.pack(side=tk.TOP)
        global new_window_label
        new_window_label = self.submit_label

    def validate_input(self,text):
        if text.isdigit() or text == "":
            return True
        else:
            return False

    def selected_gen(self):
        self.gender = self.selected_gender.get()
        if self.gender == 1:
            new_window_label.config(text="Selected gender: Male",font=("Arial",15))
        elif self.gender == 2:
            new_window_label.config(text="Selected gender: Female",font=("Arial",15))

        
    def button_click(self):
        #Validation check:
        if self.entry_speaker_id.get() == "":
            messagebox = tk.Toplevel(self.window)
            messagebox.title("Error")
            
            label = tk.Label(messagebox, text="Please Enter Speaker ID", padx=20, pady=20,font=("Arial",15))
            label.pack()
            while self.entry_speaker_id.get() == "":
                self.window.wait_window()
            # self.enter_speaker_id
        if self.gender ==-1:
            messagebox = tk.Toplevel(self.window)
            messagebox.title("Error")
            
            label = tk.Label(messagebox, text="Please select gender", padx=20, pady=20,font=("Arial",15))
            label.pack()
    
            while self.gender == -1:
                self.window.wait_window()
            self.selected_gen() 
        self.button_submit.pack_forget()
        speaker_id = self.entry_speaker_id.get()
        saved_path = self.create_folder_for_speaker_id(speaker_id)
        self.save_speaker_info(saved_path,speaker_id)
        self.window.withdraw()
        self.show_new_window(saved_path,speaker_id)
    
    def run(self):
        self.window.mainloop()
    
    def show_new_window(self,saved_path,speaker_id):
        global new_window
        new_window = tk.Toplevel(self.window)
        new_window.geometry("750x400")
        new_window.title("Record Panel")

        self.submit_frame = tk.Frame(new_window)  # Create a frame to hold the label and button
        self.submit_frame.pack()
        self.submit_label = tk.Label(self.submit_frame,font=("Arial", 17))
        self.submit_label.pack(side=tk.BOTTOM)
        self.submit_label.config(text="Set Speaker ID " + speaker_id+ "\n Saved in path: " + str(saved_path))
        return_button = tk.Button(new_window, text="Return", command=self.return_to_main)
        return_button.pack(side=tk.BOTTOM)
        return_button.pack(pady=10)
        RecorderWindow(new_window,saved_path,speaker_id,self.sentence_sheet_path)
        
    
    def return_to_main(self):
        self.submit_frame = tk.Frame(self.window)  # Create a frame to hold the label and button
        self.submit_frame.pack()
        
        self.submit_label = tk.Label(self.submit_frame)
        self.submit_label.pack(side=tk.LEFT)
        
        self.button_submit = tk.Button(self.submit_frame, text="Submit", command=self.button_click,font=("Arial",15))
        self.button_submit.pack(side=tk.LEFT)
        new_window.destroy()
        self.window.deiconify()
        
    def save_speaker_info(self,path:Path,id_number):
        gender = self.selected_gender.get()
        if gender == 1:
            g = "Male"
        else:
            g = "Female"
        # Save the speaker ID to a text file
        with open(path/("speaker_"+id_number+".txt"), "w") as file:
            file.write(id_number+"\n")
            file.write(g+"\n")
            if self.sentence_sheet_path is not None:
                file.write(self.sentence_sheet_path.name)
        

    def create_folder_for_speaker_id(self,id_number):
        # file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        # if file_path:
        #     self.submit_label.config(text="File saved as: " + file_path)
        # else:
        #     self.submit_label.config(text="File not saved")
        current_folder = os.getcwd()
    
        # saving_path = current_folder+"/"+id_number
        saving_path = Path(current_folder)/str(id_number)
        if not os.path.exists(saving_path):
            os.mkdir(saving_path)
        # else:
        #     self.submit_label.config(text="Recording Speaker ID")
        return saving_path
    
    def browse_file(self):
        # Open a file dialog to select a file
        file_path = filedialog.askopenfilename()
        
        # Print the selected file path
        # logging.debug("Selected File:", file_path)
        self.sentence_sheet_path = Path(file_path)
        
# Create an instance of the AudioRecorderApp class and run the application
app = AudioRecorderApp()
app.run()
