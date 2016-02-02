import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.

	Accumulate across all the log files the pass ratio for each question.

	A question result is considered a pass if it is not 0 or None
	and fail otherwise.

	The pass ratio for a question is the number of passes
	divided by the number of passes + fails.
preconditions
	Each command-line argument is the name of a
	readable and legal quiz log file.

	All the log_files have the same number of questions.
'''

# check number of command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

passes = []
fails = []

for n in sys.argv[1:]:
	index_ = 0
	# Determine whether the question was passed or failed by the current student
	# And increment the corresponding pass/fail counter
	for x in quiz_library.compute_mark_list(quiz_library.load_quiz_log(n)):
		if (index_+1>len(passes)):
			passes.append(0)
			fails.append(0)
		if (x!=0 and x!=None):
			passes[index_]+=1.0
		else:
			fails[index_]+=1.0
		index_+=1

output = ""
index_ = 0
for n in passes:
	# Calculate the average pass ratio for each question.
	output += str((passes[index_])/(passes[index_]+fails[index_]))
	if (index_!=len(passes)-1):
		output+=","
	index_+=1
	
print output








