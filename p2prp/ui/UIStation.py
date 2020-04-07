import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext

root = None
logt, inp = None, None
# rtwidget = {}

def submitCommand(e):
	# inp = rtwidget['inp']
	# rtwidget['inp'].delete(0, 'end')
	if not inp.get():
		return
	
	logt.configure(state='normal')
	logt.insert('end', inp.get() + '\n')
	logt.configure(state='disabled')
	inp.delete(0, 'end')
	
	return

def hostConsole():
	global root
	global logt, inp
	# global rtwidget
	
	root = tk.Tk()
	root.title('P2PRP')
	
	logt = tk.scrolledtext.ScrolledText(root, state='disabled', bg='#eeeeee')
	logt.grid(row=0, column=0)
	
	inp = tk.Entry(root, font=tkfont.Font(family='Consolas', size=14))
	inp.grid(row=1, column=0, sticky='nsew')
	inp.focus_set()
	
	# rtwidget['logt'] = logt
	# rtwidget['inp'] = inp
	
	root.bind('<Return>', submitCommand)
	
	return root