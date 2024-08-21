import numpy as np
import matplotlib.pyplot as plt
import time
import epics

import os
import sys
import cv2
import time
import scipy as sp
import time
import math
import statistics
import collections
from tqdm import tqdm

###################################################################################

# Manual choices / settings required

target_um_per_pixel_x = 1#87.336245
target_um_per_pixel_y = 1#87.336245

###################################################################################

def data_mining(element_list,t_sample=None,int_limit=None,mode=None):
	# Workpoint id
	i = 0
	# load samples
	wps = np.loadtxt("workpoints.txt")
	wps = list(wps)
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

	# preperation
	path_frames = "live_frames"
	background = read_background_image("I0T5")
	# timestamp
	time_start=time.time()

	# start mining
	with open("output.txt", "ab") as data_txt:
		with open("input.txt", "ab") as input_txt:
			for wp in wps:
				i = i+1
				print("\nWP: ",i,wp)
				# set magnet currents
				for i_element in range(len(element_list)):
					epics.caput(element_list[i_element]["name"],wp[i_element])
					#print("caput",element_list[i_element]["name"],wp[i_element])
				# wait
				time.sleep(t_sample)
				# check cup position
				if epics.caget("I0F1:position")==2:
					np.savetxt(data_txt,[time.time()-time_start,"cup in"], fmt="%s")
					data_txt.write(b"\n")
					print("Cup in, pausing data mining...")
					while(epics.caget("I0F1:position")==2):
						time.sleep(1)
					print("Cup is out of beamline, continue mining...")
					time.sleep(3)
					np.savetxt(data_txt,[time.time()-time_start,"cup out"], fmt="%s")
					data_txt.write(b"\n")
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
				# check camera intensity
				if x_int < int_limit and x_amp <10000:
					int_ok = 0
				else:
					int_ok = 1
				#print("Int_ok", int_ok)
				#print("x_amp",x_amp)
				#print("x_int",x_int)
				print("On target: ",bool(int_ok))
				# log results, tag if intensity to small, time, cup in/out, 
				np.savetxt(data_txt,[[time.time()-time_start, x_pos, x_sig, x_amp, x_off, y_pos, y_sig, y_amp, y_off, x_int, int_limit, int_ok]])
				np.savetxt(input_txt,[wp])

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

	# element list from creat_samples
	element_list = [
	{"name":"I0SH02:outCur","min_I":-6.5,"max_I":6.5,"range_I":0.5},
	{"name":"I0SV02:outCur","min_I":-6.5,"max_I":6.5,"range_I":0.55},

	{"name":"I0SH03:outCur","min_I":-2,"max_I":2,"range_I":0.75},
	{"name":"I0SV03:outCur","min_I":-2,"max_I":2,"range_I":1},

	{"name":"I0LE01:outCur","min_I":-7,"max_I":7,"range_I":2.5},

	{"name":"I0QU01:outCur","min_I":-7,"max_I":7,"range_I":1},
	{"name":"I0QU03:outCur","min_I":-7,"max_I":7,"range_I":1}

	]

	data_mining(element_list,t_sample=2,int_limit=600000,mode="gaus")

main()