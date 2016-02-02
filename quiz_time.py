import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.

	For each log file, compute the total time taken for each question. 

	Write to standard output, the average time spent for each question.
preconditions
	Each command-line argument is the name of a readable and
	legal quiz log file.

	All the log_files have the same number of questions.
'''

# handle command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

# Determine the maximum number of questions evaluated
max_questions = -1
for n in sys.argv[1:]:
	log_list = quiz_library.load_quiz_log(n)
	if (quiz_library.compute_question_count(log_list)>max_questions):
		max_questions=quiz_library.compute_question_count(log_list)
# Create lists of corresponding size, tracking the total time for each question, and the number of students who tried each question
totalTime = [0.0]*max_questions
numPeople = [0.0]*max_questions

for n in sys.argv[1:]:
	# Iterate through each log element in the given log_list, and record the time spent on each question.
	log_list = quiz_library.load_quiz_log(n)
	myTime = [0.0]*quiz_library.compute_question_count(log_list)

	lastIndex = 0
	timeStamp = 0
	firstInstance = True
	for x in log_list:

		if (firstInstance == False):
			# Take the difference between the current time and the previous timestamp
			myTime[lastIndex]+= int(x.time) - timeStamp
		else:
			# Find the first "Display element" and record its start time
			if isinstance(x, quiz_library.Display):
				firstInstance = False

		# Note each time a display element appears, and update the timestamp
		if (firstInstance == False):
			timeStamp = int(x.time)
			lastIndex = int(x.index)

	for x in range(len(myTime)):
		totalTime[x]+=myTime[x]
		numPeople[x]+=1.0

# Take list of <total time spent on each question> 
# and divide each element by the number of people who attempted the question.
# Convert the output to CSV format, and print.
output = ""
for n in range(len(totalTime)):
	output += str(totalTime[n]/numPeople[n])
	if (n!=len(totalTime)-1):
		output += ","
print output

