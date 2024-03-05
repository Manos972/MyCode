def decorateur_test(func):
	# def wrapper():
	def wrapper(*args, **kargs):
		print(f"Ceci est le debut de la fonction {func.__name__} ")
		# func(*args, **kargs)
		result = func(*args, **kargs)
		print(f"Ceci est la fin de la fonction {func.__name__} ")
		return result
	return wrapper

@decorateur_test
def my_func(a, b, c):
	return print((a * b) + c)
	



if __name__ == '__main__':
	my_func(2,4, 2)
