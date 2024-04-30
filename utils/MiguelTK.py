import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import pandas as pd

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

def bar_plot(var,df):
    sns.barplot(
        data = df[var]
        .value_counts()
        .to_frame(),
        x = 'count',
        y = var,
        hue = var,
        **kwargs
    )
    
def group_corr(df:pd.DataFrame,by:str,num_vars:list,dep_var:str):
    df_ =  (
                df
                .groupby(by)
                [num_vars]
                .corr()
                .reset_index(names=[by,'feature'])
                .query('feature == @dep_var')
                .drop(columns=['feature',dep_var])
                .set_index(by)
            )
    return df_