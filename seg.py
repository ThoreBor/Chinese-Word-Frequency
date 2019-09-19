import jieba
import time
from progressbar import *
import pickle
import re

def getChinese(context):
		filtrate = re.compile(u'[^\u4E00-\u9FA5]') # non-Chinese unicode range
		context = filtrate.sub(r'', context) # remove all non-Chinese characters
		return context

lc = 0
line_count = 0
file = input("File: ")
chinese = open(file, "rb")
for line in chinese:
	line_count = line_count + 1
chinese.close()
print(file, " has", line_count, " lines.")


value = []
unique = []
times_in_text = []
widgets = [FormatLabel(''), ' ', progressbar.Bar('=', '[', ']'),' ', Percentage(),' ', ETA()]
bar = ProgressBar(maxval=line_count, widgets=widgets)
bar.start()

with open(file, encoding="utf-8", errors='ignore') as wiki:
	for article in wiki:
		bar.update(lc)
		widgets[0] = FormatLabel('Article: '+str("{:,}".format(lc))+"/"+ str("{:,}".format(line_count)))
		data = ""

		unique_once = []
		value_once = []
		lc = lc + 1

		article = getChinese(str(article))
		seg_list = jieba.cut(article, cut_all=False)
		seg_list =  "/".join(seg_list)
		data = seg_list.split("/")
		unique_once = list(dict.fromkeys(data))
		
		for i in unique_once:
			value_once.append(data.count(i))
			
		for i in unique_once:
			if i in unique:
				index = unique.index(i)
				
				pre = int(value[index])
				pre_text = int(times_in_text[index])
				
				value[index] = data.count(i) + pre
				times_in_text[index] = pre_text + 1


			
			else:
				unique.append(i)
				value.append(data.count(i))
				times_in_text.append(1)

bar.finish()
wiki.close()
print("Creating files...")

#WORD FREQUENCY#

# value, unique = zip(*sorted(zip(value, unique)))
# value, unique = (list(t) for t in zip(*sorted(zip(value, unique))))


sorted_lists = sorted(zip(value, unique, times_in_text), reverse=True, key=lambda x: x[0])
value, unique, times_in_text = [[x[i] for x in sorted_lists] for i in range(3)]

counter = 0
f = open("Words.txt", "w", encoding="utf-8")
# unique3 = unique[::-1]
# value3 = value[::-1]

unique3 = unique
value3 = value
times_in_text3 = times_in_text
for i in unique3:  
	f.write(str(counter)+": "+i+" ("+str(value3[counter])+", "+str(times_in_text3[counter])+"/"+str(line_count)+")"+"\n")
	counter = counter+1

with open("value_data.txt","wb") as vd:
	pickle.dump(value3, vd)
with open("unique_data.txt","wb") as ud:
	pickle.dump(unique3, ud)

d = open("data.txt","w", encoding="utf-8")	
d.write(str(value3) + "\n" + str(unique3))	
d.close()
print("Done!")