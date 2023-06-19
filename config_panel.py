import tkinter as tk
import os
from tkinter import filedialog
from record_panel import RecorderWindow
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
        
        
        label_gender = tk.Label(self.window, text="Select Gender:")
        label_gender.pack(pady=10)

        self.selected_gender = tk.IntVar()

        male_button = tk.Radiobutton(self.window, text="Male", variable=self.selected_gender, value=1)#, command=self.show_selected_gender)
        male_button.pack()

        female_button = tk.Radiobutton(self.window, text="Female", variable=self.selected_gender, value=2)#, command=self.show_selected_gender)
        female_button.pack()

        self.submit_frame = tk.Frame(self.window)  # Create a frame to hold the label and button
        self.submit_frame.pack()
        
        self.submit_label = tk.Label(self.submit_frame)
        self.submit_label.pack(side=tk.LEFT)
        
        self.button_submit = tk.Button(self.submit_frame, text="Record", command=self.button_click)
        self.button_submit.pack(side=tk.LEFT)
        
    def button_click(self):
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
        new_window.geometry("900x600")
        new_window.title("Record Panel")
        # Add widgets and customize the new window as needed
        # self.submit_label.config(text="Saved in path: " + saved_path)
        self.submit_frame = tk.Frame(new_window)  # Create a frame to hold the label and button
        self.submit_frame.pack()
        self.submit_label = tk.Label(self.submit_frame)
        self.submit_label.pack(side=tk.BOTTOM)
        self.submit_label.config(text="Recording Speaker ID " + speaker_id+ "\n Saved in path: " + saved_path)
        return_button = tk.Button(new_window, text="Return", command=self.return_to_main)
        return_button.pack(side=tk.BOTTOM)
        return_button.pack(pady=10)
        RecorderWindow(new_window)
        
    
    def return_to_main(self):
        self.submit_frame = tk.Frame(self.window)  # Create a frame to hold the label and button
        self.submit_frame.pack()
        
        self.submit_label = tk.Label(self.submit_frame)
        self.submit_label.pack(side=tk.LEFT)
        
        self.button_submit = tk.Button(self.submit_frame, text="Record", command=self.button_click)
        self.button_submit.pack(side=tk.LEFT)
        new_window.destroy()
        self.window.deiconify()
        
    def save_speaker_info(self,path,id_number):
        gender = self.selected_gender.get()
        if gender == 1:
            g = "Male"
        else:
            g = "Female"
        # Save the speaker ID to a text file
        with open(path+"/speaker_"+id_number+".txt", "w") as file:
            file.write(id_number+"\n")
            file.write(g+"\n")
        
    # def show_selected_gender(self):
    #     gender = self.selected_gender.get()
    #     if gender == 1:
    #         self.submit_label.config(text="Selected gender: Male")
    #     elif gender == 2:
    #         self.submit_label.config(text="Selected gender: Female")

    def create_folder_for_speaker_id(self,id_number):
        # file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        # if file_path:
        #     self.submit_label.config(text="File saved as: " + file_path)
        # else:
        #     self.submit_label.config(text="File not saved")
        current_folder = os.getcwd()
        saving_path = current_folder+"/"+id_number
        if not os.path.exists(saving_path):
            os.mkdir(saving_path)
        # else:
        #     self.submit_label.config(text="Recording Speaker ID")
        return saving_path
        
# Create an instance of the AudioRecorderApp class and run the application
app = AudioRecorderApp()
app.run()
