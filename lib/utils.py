

def responseOutput(question):
	response = input(f"{question} (y/n) ")
	if response == "y":
		return True
	return False