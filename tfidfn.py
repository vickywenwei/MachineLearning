

import csv
import operator

from sklearn.feature_extraction.text import TfidfVectorizer


THRESHOLD = 0.7
filtered_keywords = ['LLC', 'LTD', 'INC', 'CO', 'LP', 'SA', 'NA', 'LIMITED', 'CORPORATION', 'THE', 'INVESTMENT','CAP',
					 'AND', 'LLP', 'CORP', 'CAPITAL', 'MANAGEMENT', 'TRUST', 'FUND', 'COMPANY','BANK','OF','MGMT','LLC1','NYK','LDN','NYC',
					 'HGK','DUB','LON','PAR','AMS','MAN']


def read_names():
	fid = open('./nomura.csv','r')
	reader = csv.reader(fid)
	header = reader.next()

	lst_name = []
	lst_name_original = []
	for row in reader:
		lst_name_original.append(row[0])
		name = row[0].upper()
		name = name.replace('.', ' ')
		for stop in filtered_keywords:
			name = name.replace(stop, '')
		lst_name.append(name)
		
	fid.close()
	return lst_name, lst_name_original


def get_same_list(i, dict_similar, lst_same):
	lst_same.append(i)
	lst_next_simi = dict_similar[i]
	for next_simi in lst_next_simi:
		if next_simi not in lst_same:
			lst_same = get_same_list(next_simi, dict_similar, lst_same)
	return lst_same


def main():
	lst_name, lst_name_original = read_names()
	print len(lst_name)
	print len(lst_name_original)

	vect = TfidfVectorizer(min_df=1)
	tfidf = vect.fit_transform(lst_name)
	
	similarity = (tfidf * tfidf.T).A.tolist()

	print similarity[51][51:54]

	dict_similar = {}
	for i,lst_simi in enumerate(similarity):
		lst_index = [j for j in range(len(lst_simi)) if lst_simi[j] > THRESHOLD]
		dict_similar[i] = lst_index

	fid_w = open('./nomura_new.csv','w')
	writer = csv.writer(fid_w, delimiter=',', quotechar='"')
	writer.writerow(['index','name','standard'])

	lst_saved = []
	for i in range(len(lst_name)):
		if i not in lst_saved:
			lst_same = []
			lst_same = get_same_list(i, dict_similar, lst_same)
			print lst_same

			string_same = lst_name_original[i].upper()
			cc = 1
			for j in lst_same:
				if j not in lst_saved:
					writer.writerow([str(j+1),lst_name_original[j], string_same, str(cc)])
					cc += 1
					lst_saved.append(j)

	fid_w.close()













if __name__ == '__main__':
	main()