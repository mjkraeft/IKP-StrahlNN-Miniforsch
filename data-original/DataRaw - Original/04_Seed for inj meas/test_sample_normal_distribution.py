import numpy as np
import matplotlib.pyplot as plt

# I0
n_initial = 100000

labels_of_magnets = ["I0SH03","I0SV03","I0QU01","I0QU02","I0QU03","I0SH04","I0SV04","I0LE01"]
limits_of_magnets = [[-5,5],[-5,5],[-7,7],[-7,7],[-7,7],[-5,5],[-5,5],[-4,4]]
values_of_magnets = []
values_of_magnets.append(np.random.normal(1, 0.5, n_initial))
values_of_magnets.append(np.random.normal(-2, 0.5, n_initial))

values_of_magnets.append(np.random.normal(0.5, 2, n_initial))
values_of_magnets.append(np.random.normal(0, 2, n_initial))
values_of_magnets.append(np.random.normal(-3, 2, n_initial))

values_of_magnets.append(np.random.normal(-1.5, 1, n_initial))
values_of_magnets.append(np.random.normal(2, 1, n_initial))

values_of_magnets.append(np.random.normal(0, 1.5, n_initial))

workpoints = list(map(list, zip(*values_of_magnets)))

old_length = len(workpoints)
for i in range(old_length):
	i = old_length-i-1
	for magnet in range(len(labels_of_magnets)):
		if workpoints[i][magnet]<limits_of_magnets[magnet][0] or workpoints[i][magnet]>limits_of_magnets[magnet][1]:
			workpoints.remove(workpoints[i])
			continue

print("Already here")

values_of_magnets = list(map(list, zip(*workpoints)))
for i in range(len(labels_of_magnets)):
	print("name, len, min, max",labels_of_magnets[i],limits_of_magnets[i],len(values_of_magnets[i]),min(values_of_magnets[i]),max(values_of_magnets[i]))
print("Old/New length WPs",old_length,len(workpoints),f"{100-len(workpoints)/old_length*100:.2f}% lost")

for i in range(len(labels_of_magnets)):
	plt.hist(values_of_magnets[i], 100, density=True,label=labels_of_magnets[i],alpha=0.5)
plt.legend()
plt.show()