import os
def function(path):
	#dirs = os.listdir('/Users/dr/Downloads/part_gene_result/')
	dirs = os.listdir(path)
	out = open('ans.txt', 'w')
	
	for d in dirs:
		if not d.endswith('.out'):
			continue
		text = open(path + '/' +d, 'r')
		lines = 0
		ans = ''
		while True:
			line = text.readline()
			lines = lines + 1
			if not line:
				break
			if (lines == 22) and (line[0] == '*'):
				break
			if (lines == 23):
				j = 0
				over = False
				for i in line:
					if (ans != '') and (i == ' '):
						break
					if (j > 69) and ((i.isdigit()) or ( (over == True) and (i == '.'))):
						ans = ans + i
						over = True
	
					j = j+1		
				break
	
		if ans == '':
			print d + '\t' + '0'
			print >> out, d + '\t' + '0'
		elif lines == 23:
			print d + '\t' + ans
			print >> out, d + '\t' + ans	

	return 'success'

if __name__ == '__main__':
	function('part_gene_result')