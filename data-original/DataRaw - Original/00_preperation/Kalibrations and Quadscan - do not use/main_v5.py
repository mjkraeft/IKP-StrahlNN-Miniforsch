# 	Import

# From FFT Master
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import cv2
import time
import scipy as sp
import time
import math
import epics
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


# Kalibration of Steerer
def calibrate_steerer(steerer,I_min,I_max,n_steps,target,meas_time_per_step=1):

	# Prepare
	background = read_background_image(target)
	I_setpoints = [I_min + (I_max-I_min)/(n_steps)*x for x in range(n_steps+1)]
	# Create folder
	try:
		os.mkdir("Calibration")
	except:
		print("Directory Calibration exists.")
	try:
		os.mkdir(os.path.join("Calibration",steerer))
	except:
		print(f"Directory {steerer} exists.")
	# Logging
	filename = os.path.join("Calibration",steerer,f"{steerer}_{time.time_ns()}.npy")
	with open(filename, 'wb') as f:
		time_start = time.time()
		# Start measurement
		for I_setpoint in I_setpoints:
			epics.caput(f"{steerer}:outCur",I_setpoint) 
			print(steerer,I_setpoint)
			print("Waiting for current to change...")
			time.sleep(2)
			delete_all_images(path_frames)
			time_setpoint = time.time()
			while(time.time()-time_setpoint<meas_time_per_step):
				center_sigma = eval_newest_image(path_frames,background)
				np.save(f, np.array([I_setpoint,time.time()-time_start,center_sigma[0][0],center_sigma[0][1],center_sigma[1][0],center_sigma[1][1]]))

	# Visualize and save calibration
	# Load data
	data = []
	with open(filename, 'rb') as f:
		try:
			while True:
				data.append(np.load(f,allow_pickle=True))
		except:
			pass
	data = np.transpose(data)
	I = data[0]
	timestamps = data[1]
	x = data[2]
	sig_x = data[3]
	y = data[4]
	sig_y = data[5]

	# Evaluate
	x_mean = []
	x_std = []
	y_mean = []
	y_std = []
	for I_setpoint in I_setpoints:
		x_temp = []
		y_temp = []
		for i in range(0,len(x)):
			if round(I[i],6)==round(I_setpoint,6):
				x_temp.append(x[i])
				y_temp.append(y[i])
		x_mean_value = sum(x_temp)/len(x_temp)
		x_mean.append(x_mean_value)
		x_std.append(math.sqrt(sum([(i-x_mean_value)**2 for i in x_temp]))/len(x_temp))
		y_mean_value = sum(y_temp)/len(y_temp)
		y_mean.append(y_mean_value)
		y_std.append(math.sqrt(sum([(i-y_mean_value)**2 for i in y_temp]))/len(y_temp))

	# Regression
	model_x = LinearRegression().fit(np.array(x_mean).reshape((-1, 1)), np.array(I_setpoints))
	print(f"Model_x -   slope: {model_x.coef_[0]}, intercept: {model_x.intercept_}")
	model_y = LinearRegression().fit(np.array(y_mean).reshape((-1, 1)), np.array(I_setpoints))
	print(f"Model_y -   slope: {model_y.coef_[0]}, intercept: {model_y.intercept_}")

	# Save regression parameters
	with open(os.path.join("Calibration",steerer,f"{steerer}_x_slope.txt"), 'w') as f:
		f.write(str(model_x.coef_[0]))
	with open(os.path.join("Calibration",steerer,f"{steerer}_x_intercept.txt"), 'w') as f:
		f.write(str(model_x.intercept_))
	with open(os.path.join("Calibration",steerer,f"{steerer}_y_slope.txt"), 'w') as f:
		f.write(str(model_y.coef_[0]))
	with open(os.path.join("Calibration",steerer,f"{steerer}_y_intercept.txt"), 'w') as f:
		f.write(str(model_y.intercept_))

	# Plot
	#x
	fig, axs = plt.subplots(2, 2, sharex=False, sharey=False,figsize=(12, 12))
	axs[0][0].set_xlabel('position in um')
	axs[0][0].set_ylabel('I in A')
	markers, caps, bars = axs[0][0].errorbar(x_mean, I_setpoints,xerr=x_std,ecolor='lime',color='green',label="x data")
	[bar.set_alpha(0.5) for bar in bars]
	[cap.set_alpha(0.5) for cap in caps]
	axs[0][0].plot(x_mean,model_x.predict(np.array(x_mean).reshape((-1, 1))),color = "black", label = "x fit")
	axs[0][0].legend()
	#y
	axs[0][1].set_xlabel('position in um')
	axs[0][1].set_ylabel('I in A')
	markers, caps, bars = axs[0][1].errorbar(y_mean, I_setpoints,xerr=y_std,ecolor='aqua',color='blue',label="y data")
	[bar.set_alpha(0.5) for bar in bars]
	[cap.set_alpha(0.5) for cap in caps]
	axs[0][1].plot(y_mean,model_y.predict(np.array(y_mean).reshape((-1, 1))),color = "black", label = "y fit")
	axs[0][1].legend()
	# time plot
	axs[1][0].set_xlabel('t in s')
	axs[1][0].set_ylabel('position in um')
	axs[1][0].plot(timestamps,x,color='green',label="x")
	axs[1][0].legend()

	axs[1][1].set_xlabel('t in s')
	axs[1][1].set_ylabel('position in um')
	axs[1][1].plot(timestamps,y,color='blue',label="y")
	axs[1][1].legend()
	plt.savefig(os.path.join("Calibration",steerer,f"{steerer}_{time.time_ns()}.png"),dpi=300)
	#plt.show()

# Quad scan
def quad_scan(quad,I_min,I_max,n_steps,target,meas_time_per_step=1):

	# Prepare
	background = read_background_image(target)
	I_setpoints = [I_min + (I_max-I_min)/(n_steps)*x for x in range(n_steps+1)]
	# Create folder
	try:
		os.mkdir("Calibration")
	except:
		print("Directory Calibration exists.")
	try:
		os.mkdir(os.path.join("Calibration",quad))
	except:
		print(f"Directory {quad} exists.")
	# Logging
	filename = os.path.join("Calibration",quad,f"{quad}_{time.time_ns()}.npy")
	with open(filename, 'wb') as f:
		np.save(f, np.array(["Time, setpoint, position"]))
		time_start = time.time()
		# Start measurement
		for I_setpoint in I_setpoints:
			epics.caput(f"{quad}:outCur",I_setpoint) 
			print(quad,I_setpoint)
			print("Waiting for current to change...")
			time.sleep(2)
			delete_all_images(path_frames)
			time_setpoint = time.time()
			while(time.time()-time_setpoint<meas_time_per_step):
				center_sigma = eval_newest_image(path_frames,background)
				np.save(f, np.array([I_setpoint,time.time()-time_start,center_sigma[0][0],center_sigma[0][1],center_sigma[1][0],center_sigma[1][1]]))

	# Visualize and save calibration
	# Load data
	data = []
	with open(filename, 'rb') as f:
		try:
			while True:
				data.append(np.load(f,allow_pickle=True))
		except:
			pass
	parameters = data[0]
	data = np.transpose(data[1:])
	I = data[0]
	timestamps = data[1]
	#x = data[2]
	sig_x = data[3]
	#y = data[4]
	sig_y = data[5]

	x=sig_x
	y=sig_y

	# Evaluate
	x_mean = []
	x_std = []
	y_mean = []
	y_std = []
	for I_setpoint in I_setpoints:
		x_temp = []
		y_temp = []
		for i in range(0,len(x)):
			if round(I[i],6)==round(I_setpoint,6):
				x_temp.append(x[i])
				y_temp.append(y[i])
		x_mean_value = sum(x_temp)/len(x_temp)
		x_mean.append(x_mean_value)
		x_std.append(math.sqrt(sum([(i-x_mean_value)**2 for i in x_temp]))/len(x_temp))
		y_mean_value = sum(y_temp)/len(y_temp)
		y_mean.append(y_mean_value)
		y_std.append(math.sqrt(sum([(i-y_mean_value)**2 for i in y_temp]))/len(y_temp))

	# Plot
	#x
	fig, axs = plt.subplots(2, 2, sharex=False, sharey=False,figsize=(12, 12))
	axs[0][0].set_xlabel('width in pixel')
	axs[0][0].set_ylabel('I in A')
	markers, caps, bars = axs[0][0].errorbar(x_mean, I_setpoints,xerr=x_std,ecolor='lime',color='green',label="x data")
	[bar.set_alpha(0.5) for bar in bars]
	[cap.set_alpha(0.5) for cap in caps]
	#axs[0][0].plot(x_mean,model_x.predict(np.array(x_mean).reshape((-1, 1))),color = "black", label = "x fit")
	axs[0][0].legend()
	#y
	axs[0][1].set_xlabel('width in pixel')
	axs[0][1].set_ylabel('I in A')
	markers, caps, bars = axs[0][1].errorbar(y_mean, I_setpoints,xerr=y_std,ecolor='aqua',color='blue',label="y data")
	[bar.set_alpha(0.5) for bar in bars]
	[cap.set_alpha(0.5) for cap in caps]
	#axs[0][1].plot(y_mean,model_y.predict(np.array(y_mean).reshape((-1, 1))),color = "black", label = "y fit")
	axs[0][1].legend()
	# time plot
	axs[1][0].set_xlabel('t in s')
	axs[1][0].set_ylabel('width in pixel')
	axs[1][0].plot(timestamps,x,color='green',label="x")
	axs[1][0].legend()

	axs[1][1].set_xlabel('t in pixel')
	axs[1][1].set_ylabel('width in um')
	axs[1][1].plot(timestamps,y,color='blue',label="y")
	axs[1][1].legend()
	plt.savefig(os.path.join("Calibration",quad,f"{quad}_{time.time_ns()}.png"),dpi=300)
	#plt.show()

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
			center_sigma.append([fitparams[1], fitparams[2], fitparams[0], fitparams[3], np.sum(horiz_projection)]) #[x_pos,x_sig,x_amp,x_off,x_intens]
		if mode == "stat":
			center_sigma.append([mean, sigma_guess, fitparams[0], fitparams[3], np.sum(horiz_projection)])

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
			time.sleep(0.01)
			delete_all_images(path)


# Gaus fit

def gauss(x, amplitude, center, sigma, offset):
	return amplitude * np.exp(-0.5 * (x - center)**2 / (sigma)**2) + offset

def ausschlag(steerer_x,steerer_y,value_x,value_y):
	print("Moving steerer to custom position...")
	epics.caput(steerer_x+":outCur",value_x)
	epics.caput(steerer_y+":outCur",value_y)
	time.sleep(5)

# Main

def main():

	quad_scan("I0QU01",-1,1,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0QU01:outCur",0)
	calibrate_steerer("I0SH02",-0.5,0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SH02:outCur",0)
	calibrate_steerer("I0SV02",-0.5,0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SV02:outCur",0)
	calibrate_steerer("I0SH03",-0.5,0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SH03:outCur",0)
	calibrate_steerer("I0SV03",-0.5,0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SV03:outCur",0)
	quad_scan("I0QU03",-1,1,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0QU03:outCur",0)
	quad_scan("I0LE01",-3.5,3.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0LE01:outCur",0)

	quad_scan("I0QU01",1,-1,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0QU01:outCur",0)
	calibrate_steerer("I0SH02",0.5,-0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SH02:outCur",0)
	calibrate_steerer("I0SV02",0.5,-0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SV02:outCur",0)
	calibrate_steerer("I0SH03",0.5,-0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SH03:outCur",0)
	calibrate_steerer("I0SV03",0.5,-0.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0SV03:outCur",0)
	quad_scan("I0QU03",1,-1,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0QU03:outCur",0)
	quad_scan("I0LE01",3.5,-3.5,50,"I0T5",meas_time_per_step=5)
	epics.caput("I0LE01:outCur",0)

main()