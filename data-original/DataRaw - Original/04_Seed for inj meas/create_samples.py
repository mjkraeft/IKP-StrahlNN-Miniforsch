import numpy as np
import matplotlib.pyplot as plt
#from epics import caget

def caget(name):
	print("caget in diagnostics mode")
	return 0

def create_workpoints(n_samples=100000,sigma=2):

	element_list = [

	{"name":"I0SH02:outCur","min_I":-6.5,"max_I":6.5,"range_I":0.5},
	{"name":"I0SV02:outCur","min_I":-6.5,"max_I":6.5,"range_I":0.55},

	{"name":"I0SH03:outCur","min_I":-2,"max_I":2,"range_I":0.75},
	{"name":"I0SV03:outCur","min_I":-2,"max_I":2,"range_I":1},

	{"name":"I0LE01:outCur","min_I":-7,"max_I":7,"range_I":2.5},

	{"name":"I0QU01:outCur","min_I":-7,"max_I":7,"range_I":1},
	{"name":"I0QU03:outCur","min_I":-7,"max_I":7,"range_I":1}

	]

	# log element list


	# create workpoints
	wps = []
	for element in element_list:
		wps.append(np.random.normal(caget(element["name"]), element["range_I"]/sigma, n_samples))
	# transpose
	wps_t = list(map(list, zip(*wps)))
	# delete workpoints out of range
	wps_out_of_range=[]
	for wp in wps_t:
		for i_element in range(len(element_list)):
			if wp[i_element]<element_list[i_element]["min_I"] or wp[i_element]>element_list[i_element]["max_I"]:
				wps_out_of_range.append(wp)

	for wp_out_of_range in wps_out_of_range:
		try:
			wps_t.remove(wp_out_of_range)
		except:
			pass
	# print some statistics
	print("samples created",len(wps[0]))
	print("samples kept", len(wps_t))
	print("samples out of range", len(wps_out_of_range))
	print("ratio samples lost:",round(len(wps_out_of_range)/len(wps_t)*100,2),"%")

	# save list
	#https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html
	with open("element_list.txt", "ab") as element_list_txt:
		for entry in element_list:
			np.savetxt(element_list_txt,[[entry["name"]]], fmt='%s')
	np.savetxt("workpoints.txt",wps_t)
	# visualize
	# retranspose filtered list
	wps = list(map(list, zip(*wps_t)))
	plt.figure(figsize=(9,9))
	for i_element in range(len(element_list)):
		name = element_list[i_element]["name"]
		mean = round(caget(element_list[i_element]["name"]),4)
		std = round(element_list[i_element]["range_I"]/sigma,4)
		plt.hist(wps[i_element],100,density=True,label=f"{name}, $I={mean}$, $\sigma={std} $",alpha=0.5)
	plt.title("Samples generated: "+str(len(wps_t)) + " ("+str(round(len(wps_out_of_range)/len(wps_t)*100,2))+"% lost)")
	plt.xlabel("$I$ in nA")
	plt.ylabel("$\#$ of samples")
	plt.legend()
	plt.savefig("sample_distribution.png",dpi=300)
	plt.show()

	#test
	#print(np.loadtxt("workpoints.txt"))

create_workpoints()

