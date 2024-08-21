import numpy as np
import matplotlib.pyplot as plt
from epics import caget, caput
import epics
import time
import os
import cv2
import time
import scipy as sp
import math
import statistics

from sklearn.linear_model import LinearRegression
from tqdm import tqdm
from simple_pid import PID

###################################################################################

# Manual choices / settings required

target_um_per_pixel_x = 1#87.336245
target_um_per_pixel_y = 1#87.336245

path_frames = "LiveBilder"

###################################################################################

def label_samples(element_list,target,mode="stat",i_wps=4):

	# Workpoint id
	i = 0
	# load samples
	wps = np.loadtxt("workpoints.txt")
	wps = list(wps)
	background = read_background_image(target)
	# check if samples have been evaluated already, e.g. load results and compare
	try:
		input_eval = np.loadtxt("input.txt")
		input_eval = list(input_eval)
		print(len(input_eval),"workpoints have been evaluated and will be skipped")
		for wp_i in tqdm(range(len(wps))):
			wp_i = len(wps)-1-wp_i # reverse
			for wp in input_eval:
				if collections.Counter(wp) == collections.Counter(wps[wp_i]):
					wps.pop(wp_i)
					i = i+1
		print(i,"workpoints have been skipped")
	except Exception as e:
		print("Could not load already evaluated workpoint, arent there any?", e)

	# timestamp
	time_start=time.time()

	with open("output.txt", "ab") as data_txt:
		for i in range(i_wps):
			wp = wps[i]
			print("\nWP: ",i,wp)
			# set magnet currents
			for i_element in range(len(element_list)):
				epics.caput(element_list[i_element]["name"],wp[i_element])
				#print("caput",element_list[i_element]["name"],wp[i_element])
			# wait
			int_ok=int(input("Is the beam on target? (1:yes, 0:no)\n"))
			# check cup position
			if False:#epics.caget("I0F1:position")==2 or epics.caget("I0F2:position")==2:
				np.savetxt(data_txt,[time.time()-time.start(),"cup in"])
				data_txt.write(b"\n")
				print("Cup in, pausing data mining...")
				while(epics.caget("I0F1:position")==2 or epics.caget("I0F2:position")==2):
					time.sleep(1)
				print("Cup is out of beamline, continue mining...")
				time.sleep(3)
				np.savetxt(data_txt,[time.time()-time.start(),"cup out"])
				data_txt.write(b"\n")
				continue
			# evaluate camera image
			cam_param = eval_newest_image(path_frames,background,mode=mode)
			#cam_param = [[0,1,2,3,4],[0,1,2,3,4]]
			x_pos = cam_param[0][0]
			y_pos = cam_param[1][0]
			x_sig = cam_param[0][1]
			y_sig = cam_param[1][1]
			# andere parameter für strom/gaus rekonstruktion
			x_amp = cam_param[0][2]
			x_off = cam_param[0][3]
			x_int = cam_param[0][4]
			y_amp = cam_param[1][2]
			y_off = cam_param[1][3]
			y_int = cam_param[1][4]

			# log results, tag if intensity to small, time, cup in/out, 
			print([[time.time()-time_start, x_pos, x_sig, x_amp, x_off, y_pos, y_sig, y_amp, y_off, x_int, int_ok]])
			np.savetxt(data_txt,[[time.time()-time_start, x_pos, x_sig, x_amp, x_off, y_pos, y_sig, y_amp, y_off, x_int, int_ok,i]])

	# analyze samples
	data=[]
	with open("output.txt","r") as file:
		for line in file.readlines():
			line = line.replace("True","1")
			line = line.replace("False","0")
			line = line.replace("\n","")
			#line = line.replace(" ","")
			line = line.split(" ")
			line = [float(x) for x in line]
			# shift and scale
			data.append(line)
	data = list(map(list, zip(*data)))

	data_beam = []
	data_no_beam = []

	for i in range(len(data[0])):
		if data[10][i]==1:
			data_beam.append(data[9][i])
		else:
			data_no_beam.append(data[9][i])

	plt.plot(data_beam,".",label=f"data_beam ({round(len(data_beam)/i_wps*100,2)}%)")
	plt.plot(data_no_beam,".",label=f"data_no_beam ({round(len(data_no_beam)/i_wps*100,2)}%)")
	plt.xlabel("# Measurement")
	plt.ylabel("Intensity in a.u.")
	plt.legend()
	plt.savefig("Intensity_statistics.png",dpi=300)
	plt.show()
	plt.clf()


# Read last image
def read_newest_image(path):
	filenames = []
	i = 0
	while filenames == []: # check if this works until one gets an image
		filenames = os.listdir(path)
		if i == 0 and filenames == []:
			print("Waiting for a camera image...")
		if filenames ==[]:
			time.sleep(0.0001)
		#if i>10000:
		#	print("Waited to long, therefore exited")
		#	exit()
		i+=1
	# Read last image
	filenames.sort()
	filename = filenames[-1]
	img = None
	try:
		while img==None:
			img = cv2.imread(os.path.join(path,filename),cv2.IMREAD_GRAYSCALE)
	except:
		pass
	return filenames, img

# Read background image
def read_background_image(target):
	img = cv2.imread(os.path.join("background",f"{target}.png"),cv2.IMREAD_GRAYSCALE)
	return img

# eval an image
def eval_image(img,background,mode="gaus"):

	# background substraction
	img = cv2.subtract(img,background)

	# median filter
	img = cv2.medianBlur(img, 3)

	# rotate image
	img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

	# projection
	image_array = np.asarray(img,dtype='float32')
	horiz_projection = np.sum(image_array,0)
	vert_projection = np.sum(image_array,1)
	if mode=="int":
		return np.sum(horiz_projection)

	# gaus fit for x and y
	center_sigma = []
	amplitudes = []
	for i in range(2):
		# x
		if i == 0:
			input_data = horiz_projection
			target_um_per_pixel = target_um_per_pixel_x
		# y
		if i == 1:
			input_data = vert_projection
			target_um_per_pixel = target_um_per_pixel_y

		x_data = np.linspace(0, target_um_per_pixel * len(input_data), len(input_data))
		# weighted arithmetic mean
		mean = sum(x_data * input_data) / sum(input_data)
		# start values
		center_guess = x_data[input_data.tolist().index(max(input_data))]
		amplitude_guess = max(input_data)
		sigma_guess = np.sqrt(sum(input_data * (x_data - mean)**2) / sum(input_data))
		offset_guess = min(input_data)
		lower_bounds = [1, x_data[0], 0.001, -10**10]
		upper_bounds = [10**10, x_data[-1], x_data[-1]-x_data[0], 10**10]
		# popt, pcov
		fitparams, cov_matrix = sp.optimize.curve_fit(gauss,
											x_data,
											input_data,
											p0=(amplitude_guess, center_guess, sigma_guess, offset_guess),
											bounds=(lower_bounds, upper_bounds))
		# Errors
		#perr = np.sqrt(np.diag(cov_matrix))
		#np.savetxt(output_filename, [(fitparams[0], fitparams[1], perr[1], fitparams[2], perr[2], fitparams[3])] ,
		#			header='amp\t center center_fit_error sigma\t sigma_fit_error offset',fmt='%1.2f',delimiter='\t')
		if mode == "gaus":
			center_sigma.append([fitparams[1], fitparams[2], fitparams[0], fitparams[3], np.sum(input_data)]) #[x_pos,x_sig,x_amp,x_off,x_intens]
		if mode == "stat":
			center_sigma.append([mean, sigma_guess, fitparams[0], fitparams[3], np.sum(input_data)])

	return center_sigma # [[x_pos,x_sig,x_amp,x_off,x_intens],[y_pos,y_sig,y_amp,y_off,y_intens]]

# eval last image, delete them afterwards
def eval_newest_image(path_frames,background,delete=True,mode="gaus"):

	# Read last image
	filenames, img = read_newest_image(path_frames)
	# Eval image
	center_sigma = eval_image(img,background,mode=mode)

	# Delete all read images
	if delete:
		for filename in filenames:
			try:
				os.remove(os.path.join(path_frames,filename))  
			except:
				pass # not a problem, delete it in next run

	# Save info how many images were lost (#deleted-1)
	#skipped_images = len(filenames)-1
	#if skipped_images > 1:
	#	print("Skipped images because cam is faster than python script:	",skipped_images)

	return center_sigma

# Delete all images
def delete_all_images(path):
	print("Deleting existing images...")
	filenames = os.listdir(path)
	for filename in filenames:
		try:
			os.remove(os.path.join(path,filename))
		except:
			print("Retrying to delete all images...")
			time.sleep(0.1)
			delete_all_images(path)


# Gaus fit
def gauss(x, amplitude, center, sigma, offset):
	return amplitude * np.exp(-0.5 * (x - center)**2 / (sigma)**2) + offset


# Main
def main():
	element_list = [

	{"name":"I0SH02:outCur","min_I":-6.5,"max_I":6.5,"range_I":0.5},
	{"name":"I0SV02:outCur","min_I":-6.5,"max_I":6.5,"range_I":0.5},

	{"name":"I0SH03:outCur","min_I":-2,"max_I":2,"range_I":0.7},
	{"name":"I0SV03:outCur","min_I":-2,"max_I":2,"range_I":0.7},

	{"name":"I0LE01:outCur","min_I":-7,"max_I":7,"range_I":2},

	{"name":"I0QU01:outCur","min_I":-7,"max_I":7,"range_I":1},
	{"name":"I0QU03:outCur","min_I":-7,"max_I":7,"range_I":1}

	]

	label_samples(element_list,"I0T5",mode="stat",i_wps=100)


main()