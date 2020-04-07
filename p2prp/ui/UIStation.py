import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext

class LoggerConsole:
	def __init__(self):
		root = tk.Tk()
		
		logt = tk.scrolledtext.ScrolledText(root, state='disabled', bg='#eeeeee')
		logt.grid(row=0, column=0)
		
		inp = tk.Entry(root, font=tkfont.Font(family='Consolas', size=14))
		inp.grid(row=1, column=0, sticky='nsew')
		
		self.root, self.logt, self.inp = root, logt, inp

def hostConsole():
	console = LoggerConsole()
	
	console.root.title('P2PRP')
	console.inp.focus_set()
	
	return console