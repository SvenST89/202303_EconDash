# For Visualization
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
from IPython.core.pylabtools import figsize

def plot_allstd_fig(df):
    index=df.index
    index=index.tolist()
    for col in list(df.columns): # iterate across the columns where the observation value is to find for each maturity
        y=df[col].tolist()
        plt.plot(index, y, label=col)

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Yields', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.title("3M-30Y Yield Development", fontweight='bold')
    plt.rcParams['text.color']='grey' # optional, if you want to change the coloring of the text part

    # Then, show the figure
    plt.show()

def plot_final_yield_curve_std(df):
    index=df.index
    index=index.tolist()
    for col in list(df.columns): # iterate across the columns where the observation value is to find for each maturity
        y=df[col].tolist()
        plt.plot(index, y, label=col)

    plt.xlabel('Maturities', fontsize=16)
    plt.ylabel('Yields', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.title("ECB Euro Area Yield Curve", fontweight='bold')
    plt.rcParams['text.color']='black' # optional, if you want to change the coloring of the text part

    # Then, show the figure
    plt.show()
