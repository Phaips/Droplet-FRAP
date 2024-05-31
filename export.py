# !!! Make sure to adjust output_path, n_slices, and the name of the FRAP_data_give_name_here.csv file !!!
# The comments should walk you through each line. 
# This script can be used in Fiji/ImageJ (Jython script) and will export a .csv file with the normalized FRAP intensities in order to plot them nice(r than Fiji) (see plotting.py)
# Select ROI's of the FRAP areas. It is necessary that in your ROI manager every ROI is a FRAP ROI and the last one is the normalization ROI. Press run :)

import java.awt.Color as Color
from ij import WindowManager
from ij.plugin.frame import RoiManager
from ij.process import ImageStatistics
from ij.measure import Measurements
from ij import IJ
from ij.gui import Plot
import math
import csv

# Define the path where the CSV file will be saved!
output_path = "C:/add/path/here/"

# Get ROIs from ROI Manager
roi_manager = RoiManager.getInstance()
roi_list = roi_manager.getRoisAsArray()

# The last ROI is assumed to be the control ROI
roi_norm = roi_list[-1]

# Specify up to what frame to fit and plot. IMPORTANT TO SET THIS!!
n_slices = 153

# Get current image plus and image processor
current_imp = WindowManager.getCurrentImage()
stack = current_imp.getImageStack()
calibration = current_imp.getCalibration()

# Open CSV file for writing at the specified path. GIVE YOUR DESIRED FILE NAME!!
csv_file = open(output_path + "FRAP_data_add_name.csv", "w")
csv_writer = csv.writer(csv_file, delimiter=',')
csv_writer.writerow(['ROI Name', 'Time (s)', 'Normalized Intensity'])  # Write header

# Main analysis for each FRAP ROI
for roi_FRAP in roi_list[:-1]:  # Exclude the last ROI, which is for normalization (!)
    If = []  # Frap intensities
    In = []  # Normalization intensities

    # Process each slice for current FRAP ROI
    for i in range(1, n_slices + 1):
        ip = stack.getProcessor(i)
        ip.setRoi(roi_FRAP)
        stats = ImageStatistics.getStatistics(ip, Measurements.MEAN, calibration)
        If.append(stats.mean)

        ip.setRoi(roi_norm)
        stats = ImageStatistics.getStatistics(ip, Measurements.MEAN, calibration)
        In.append(stats.mean)

    # Calculate normalized curve
    min_intensity = min(If)
    bleach_frame = If.index(min_intensity)
    mean_If = sum(If[:bleach_frame]) / bleach_frame
    mean_In = sum(In[:bleach_frame]) / bleach_frame

    # Corrected intensity -> normalization to account for photobleaching from imaging
    corrected_intensity = [If[i] / In[i] for i in range(n_slices)]

    # Mean corrected pre-bleach intensity
    mean_corrected_pre_bleach = sum(corrected_intensity[:bleach_frame]) / bleach_frame

    # Normalization
    normalized_curve = [(corrected_intensity[i] - min(corrected_intensity)) / 
                        (mean_corrected_pre_bleach - min(corrected_intensity)) 
                        for i in range(n_slices)]

    x = [i * calibration.frameInterval for i in range(n_slices)]

    # Write data to CSV
    for time, norm_intensity in zip(x, normalized_curve):
        csv_writer.writerow([roi_FRAP.getName(), time, norm_intensity])

# Close the CSV file
csv_file.close()

IJ.log('Data exported successfully to ' + output_path)
