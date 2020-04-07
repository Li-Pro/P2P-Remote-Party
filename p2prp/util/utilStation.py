
def toStr(*args, delim=' '):
	return str(delim.join(map(str, [*args])))