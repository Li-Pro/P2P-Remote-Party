import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext

import pyautogui as pagui

import PIL
from PIL import Image, ImageTk

import queue, threading, io

class LoggerConsole:
	def __init__(self):
		root = tk.Tk()
		
		logfnt = tkfont.Font(family='Consolas', size=14)
		
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		
		logt = tk.scrolledtext.ScrolledText(root, state='disabled', bg='#eeeeee', font=logfnt)
		logt.grid(row=0, column=0, sticky='nsew')
		
		inp = tk.Entry(root, font=logfnt)
		inp.grid(row=1, column=0, sticky='nsew')
		
		self.root = root
		self.logt = logt
		self.inp = inp
		
		self.msgQueue = queue.Queue()
	
	def addLog(self, msg):
		self.msgQueue.put(msg)
	
	def addWarning(self, msg):
		self.msgQueue.put(msg)
	
	def addError(self, msg):
		self.msgQueue.put(msg)
	
	def scheduleUpdate(self):
		self.root.after(10, self.updateLogger)
	
	def updateLogger(self):
		root, logt, qu = self.root, self.logt, self.msgQueue
		
		while not qu.empty():
			msg = qu.get()
			
			logt.configure(state='normal')
			logt.insert('end', str(msg) + '\n')
			logt.configure(state='disabled')
		
		root.after(10, self.updateLogger)

class StreamWindow:
	def __init__(self, parent):
		root = tk.Toplevel(parent)
		
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		
		img = tk.Label(root)
		img.grid(row=0, column=0, sticky='nsew')
		
		self.root = root
		self.img = img
		
		self.imglock = threading.Lock()
	
	def setImage(self, osize, data):
		with self.imglock:
			# image = PIL.Image.frombytes('RGBA', osize, data)
			image = PIL.Image.open(io.BytesIO(data))
			# image.thumbnail((osize[0]//2, osize[1]//2), PIL.Image.ANTIALIAS)
			
			size = pagui.size()
			nsize = min(osize[0]//size[0], osize[1]//size[1]) * size
			
			image.thumbnail(nsize, PIL.Image.ANTIALIAS)
			
			photo = PIL.ImageTk.PhotoImage(image)
			
			self.img.configure(image=photo)
			self.img.image = photo
			
	
	def withdraw(self):
		self.root.withdraw()
	
	def deiconify(self):
		self.root.deiconify()

def hostStreamWidget(parent):
	window = StreamWindow(parent)
	window.root.title('P2PRP Stream')
	window.root.wm_attributes('-fullscreen', 'true')
	
	return window

def hostConsole():
	console = LoggerConsole()
	
	console.root.title('P2PRP')
	console.inp.focus_set()
	
	return console