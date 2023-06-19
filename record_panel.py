import tkinter as tk
import os
import pandas as pd
import numpy as np
import ast
class RecorderWindow:
    def __init__(self,win):
        self.window = win
        current_folder = os.getcwd()
        current_folder = current_folder + "/10_samples.xlsx"
        self.sentences = pd.read_excel(current_folder)
        
        self.current_sentence = 0
        # Specify the column index for the sentences
        column_index = 0  # Replace with the actual column index (starting from 0)

        # Access the sentences from the specified column index
        self.sentences = self.sentences.iloc[:, column_index].tolist()

        
        self.text = tk.Text(self.window, height=2, width=75,font=("Arial",18))
        self.text.pack()
        self.text.insert(tk.END, str(self.current_sentence+1)+") "+self.sentences[self.current_sentence])
        previous_button = tk.Button(self.window, text="Previous", command=self.previous_sentence)
        previous_button.pack(side=tk.LEFT)

        next_button = tk.Button(self.window, text="Next", command=self.next_sentence)
        next_button.pack(side=tk.LEFT)
    
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
        self.text.insert(tk.END, str(self.current_sentence+1)+") "+self.sentences[self.current_sentence])
        