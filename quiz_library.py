import libxml2
import sys

'''
purpose
	store the information from an answer element
'''
class Answer:
	def __init__(self, index, path, result, answer, time):
		self.index = index
		self.path = path
		self.result = result
		self.answer = answer
		self.time = time

'''
purpose
	Store the information from a display element.
'''
class Display:
	def __init__(self, index, path, time):
		self.index = index
		self.path = path
		self.time = time

'''
purpose
	Extract the information from log_file and return it as a list
	of answer and display objects.
preconditions
	log_file is the name of a legal, readable quiz log XML file
'''
def load_quiz_log(log_file):

	# Prepare the xml file for reading
	parse_tree = libxml2.parseFile(log_file)
	context = parse_tree.xpathNewContext()
	root = parse_tree.getRootElement()

	# Iterate through each child node in the xml file
	nodeType = root.children
	nodes = [ ]
	while nodeType is not None:
		if (nodeType.name != "text"):
			ret = None			
			values = [ ]
			child = nodeType.children
			# List the content blocks attached to each child node
			while child is not None:
				if ((child.content != "\n") and (child.content != "\n\t")):
					if (child.content != ""):
						values.append(child.content)
					else:
						values.append(None)
				child = child.next
			# Create a corresponding instance, and pass the value list as parameters
			if nodeType.name == "answer":
				ret = Answer(*values)
			elif nodeType.name == "display":
				ret = Display(*values)
			nodes.append(ret)
		nodeType = nodeType.next
	return nodes
'''
purpose
	Return the number of distinct questions in log_list.
preconditions
	log_list was returned by load_quiz_log
'''
def compute_question_count(log_list):

	seen = []
	for x in log_list:
		# Track each question, and mark any newly seen questions into the ouput list
		if isinstance(x, Answer):
			index = x.index
			repeated = False
			for n in seen:
				if (n == index):
					repeated = True
					break
			if (repeated == False):
				seen.append(index)

	return len(seen)

'''
purpose
	Extract the list of marks.
	For each index value, use the result from the last non-empty answer,
	or 0 if there are no non-empty results.
preconditions
	log_list was returned by load_quiz_log
'''
def compute_mark_list(log_list):
	
	# Initialize an empty list of corresponding size
	ret = [0]*compute_question_count(log_list)

	# Iterate through each answer element, and determine what the last recorded result was
	for x in log_list:
		if isinstance(x, Answer):
			if (x.result != None):
				ret[int(x.index)] = int(x.result)

	return ret
