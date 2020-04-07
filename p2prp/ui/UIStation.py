import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext

import queue

class LoggerConsole:
	def __init__(self):
		root = tk.Tk()
		
		logt = tk.scrolledtext.ScrolledText(root, state='disabled', bg='#eeeeee')
		logt.grid(row=0, column=0)
		
		inp = tk.Entry(root, font=tkfont.Font(family='Consolas', size=14))
		inp.grid(row=1, column=0, sticky='nsew')
		
		self.root = root
		self.logt = logt
		self.inp = inp
		
		self.msgQueue = queue.Queue()
	
	def addLog(self, msg):
		self.msgQueue.put(msg)
	
	def scheduleUpdate(self):
		self.root.after(10, self.updateLogger)
	
	def updateLogger(self):
		root, logt, qu = self.root, self.logt, self.msgQueue
		
		# if not qu.empty():
		while not qu.empty():
			msg = qu.get()
			
			logt.configure(state='normal')
			logt.insert('end', str(msg) + '\n')
			logt.configure(state='disabled')
		
		root.after(10, self.updateLogger)

def hostConsole():
	console = LoggerConsole()
	
	console.root.title('P2PRP')
	console.inp.focus_set()
	
	return console