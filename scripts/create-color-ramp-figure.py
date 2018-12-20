import ccb
import aei
import numpy as np
import matplotlib as mpl

# set an output file to save to
outfile = '/home/cba/Downloads/rgb-legend.png'

# set some labels for the plots later
label_red = 'Temperature (mean)'
label_grn = 'Temperature (variance)'
label_blu = 'Temperature (skew)'

# set the range of data values for each label
min_red = 10
max_red = 40
min_grn = -30
max_grn = 400
min_blu = -0.25
max_blu = 0.40

# create a set of arrays with varying rgb values to approximate a hue ramp
cols = np.zeros((3, 360)) # with rows r, g, b

# create ascending and descending values for r, g, and b
asc = (np.arange(1,61) / 60.) * 255
dsc = (np.arange(60,0,-1) / 60.) * 255
ones = np.ones(60) * 255
zeros = np.zeros(60) 

# assign these values in the color ramps
# red
cols[0, 0:60] = ones
cols[0, 60:120] = dsc
cols[0, 120:180] = zeros
cols[0, 180:240] = zeros
cols[0, 240:300] = asc
cols[0, 300:360] = ones

# green
cols[1, 0:60] = asc
cols[1, 60:120] = ones
cols[1, 120:180] = ones
cols[1, 180:240] = dsc
cols[1, 240:300] = zeros
cols[1, 300:360] = zeros

# blue
cols[2, 0:60] = zeros
cols[2, 60:120] = zeros
cols[2, 120:180] = asc
cols[2, 180:240] = ones
cols[2, 240:300] = ones
cols[2, 300:360] = dsc

# create a list of rgb pairings
palette = []

for i in range(360):
    rgb = tuple([cols[0,i], cols[1,i], cols[2,i]])
    hx = aei.color.rgb_to_hex(rgb)
    palette.append(hx)
    
# convert this color to a color map    
colors = aei.objects.color(palette=palette, name='rgb')

# set up the figure plots
fig = plt.figure(figsize=(6, 4), dpi=200)
ax1 = fig.add_axes([0.1, 0.075, 0.8, 0.12])

# normalize the colors
norm = mpl.colors.Normalize(vmin=5, vmax=10)

# plot the color bar
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=colors.cmap, norm=norm, orientation='horizontal')
ax1.tick_params(
    axis='x',
    which='both', 
    bottom=False,     
    top=False,         
    labelbottom=False)
ax1.set_xlabel('Map color')

# add other labels
#####
# red
ax2 = fig.add_axes([0.1, 0.3, 0.8, 0.17])
ax2.plot(np.arange(360), cols[0,:], color='red', linewidth=2.5)

# set xticks
ax2.set_xlim([0,360])
ax2.tick_params(
    axis='x',
    which='both', 
    bottom=False,     
    top=False,         
    labelbottom=False)

# set y ticks
ax2.set_yticks([0,255])
yl = ax2.get_yticks().tolist()
yl[0] = min_red
yl[1] = max_red
ax2.set_yticklabels(yl)

# set title
ax2.set_xlabel(label_red)

#####
# green
ax3 = fig.add_axes([0.1, 0.55, 0.8, 0.17])
ax3.plot(np.arange(360), cols[1,:], color='green', linewidth=2.5)

# set xticks
ax3.set_xlim([0,360])
ax3.tick_params(
    axis='x',
    which='both', 
    bottom=False,     
    top=False,         
    labelbottom=False)

# set y ticks
ax3.set_yticks([0,255])
yl = ax3.get_yticks().tolist()
yl[0] = min_grn
yl[1] = max_grn
ax3.set_yticklabels(yl)

# set title
ax3.set_xlabel(label_grn)

#####
# blue
ax4 = fig.add_axes([0.1, 0.8, 0.8, 0.17])
ax4.plot(np.arange(360), cols[2,:], color='blue', linewidth=2.5)

# set xticks
ax4.set_xlim([0,360])
ax4.tick_params(
    axis='x',
    which='both', 
    bottom=False,     
    top=False,         
    labelbottom=False)

# set y ticks
ax4.set_yticks([0,255])
yl = ax4.get_yticks().tolist()
yl[0] = min_blu
yl[1] = max_blu
ax4.set_yticklabels(yl)

# set title
ax4.set_xlabel(label_blu)

######
# save the final output
plt.savefig(outfile)
















