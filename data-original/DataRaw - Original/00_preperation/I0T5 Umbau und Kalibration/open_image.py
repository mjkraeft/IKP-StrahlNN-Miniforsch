import cv2
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename

image = cv2.imread(askopenfilename(initialdir  = "."),cv2.IMREAD_GRAYSCALE)
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.show()
