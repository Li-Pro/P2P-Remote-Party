import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext

# root = None
# logt, inp = None, None

# def submitCommand(e):
	# if not inp.get():
		# return
	
	# logt.configure(state='normal')
	# logt.insert('end', inp.get() + '\n')
	# logt.configure(state='disabled')
	# inp.delete(0, 'end')
	
	# return

class LoggerConsole:
	def __init__(self):
		root = tk.Tk()
		
		logt = tk.scrolledtext.ScrolledText(root, state='disabled', bg='#eeeeee')
		logt.grid(row=0, column=0)
		
		inp = tk.Entry(root, font=tkfont.Font(family='Consolas', size=14))
		inp.grid(row=1, column=0, sticky='nsew')
		
		self.root, self.logt, self.inp = root, logt, inp

def hostConsole():
	# global root
	# global logt, inp
	
	console = LoggerConsole()
	
	console.root.title('P2PRP')
	console.inp.focus_set()
	
	# root.bind('<Return>', submitCommand)
	
	return console