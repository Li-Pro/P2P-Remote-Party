import pyautogui as pagui
import io

def toStr(*args, delim=' '):
	return str(delim.join(map(str, [*args])))

def screenShot():
	img = pagui.screenshot()
	
	buf = io.BytesIO()
	img.save(buf, format='PNG')
	return buf.getvalue()

def getScrRes():
	return pagui.size()