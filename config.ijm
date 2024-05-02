# Macro intended to autoscale contrast, set LUT, set scale bar (10uM bottom right), add time stamp, and set propeties (time per frame)
# !!! Please adjust the parameters! Especially interval= range= frames= and frame= !!!
run("Green");
run("Enhance Contrast", "saturated=0.35");
run("Scale Bar...", "width=10 height=50 thickness=15 font=50 bold overlay label");
run("Label...", "format=0 starting=0 interval=2 x=5 y=10 font=15 text=sec range=1-200 use");
run("Properties...", "channels=1 slices=1 frames=33 pixel_width=0.0650000 pixel_height=0.0650000 voxel_depth=1.0000000 frame=2");
