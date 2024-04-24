import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
palette = [
    '#004aad',
    '#5bb7c3',
    '#f4eedc',
    '#848484',
    '#001C41'
]
def rot_show(rot=90):
    plt.xticks(rotation=rot)
    plt.show()
kwargs = {
    'legend' : False,
    'palette' : palette,
    'edgecolor' : 'black',
    'linewidth' : 1
}
def subplots_show():
    plt.subplots_adjust(wspace=.6,hspace=.6)
    plt.show()
cmap = LinearSegmentedColormap.from_list('Mi_cbar',['#AD6300','#f4eedc','#004aad'])
