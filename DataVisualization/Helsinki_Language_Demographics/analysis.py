import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


"""
This is a basic demonstration on data analysis/visualisation using pandas.
The language of of the output plots are in finnish since I'm bit lazy to change that lol.
The data is open source data from https://stat.hel.fi/pxweb/fi/Aluesarjat/Aluesarjat__vrm__vaerak__umkun/Hginseutu_VA_VR02_Vakiluku_aidinkieli3.px/.
I only downloaded data with three cities and currently only look at data from Helsinki.
This code also has my custom plotting function to make a nice looking plot.
"""

def filter_by_areas_languages(dataframe, areas, languages):
    """Filters the data based on desired areas and languages"""
    
    return dataframe[ (dataframe["Äidinkieli"].isin(languages)) & (dataframe["Alue"].isin(areas) ) ]


def initialize_plot(bgcolor="#DEBA87", figsize=(8, 6), nrows=1, ncols=1):
    """Initialize a figure with ROOT-like styling"""

    # Set up the figure
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    fig.patch.set_facecolor(bgcolor)


    # Ensure axes is always iterable (even if there's just one subplot)
    if nrows == 1 and ncols == 1:
        axes = [axes]
    elif nrows == 1 or ncols == 1:
        axes = axes.flatten()
    else:
        axes = axes.reshape(-1)

    for ax in axes:
        ax.set_facecolor(bgcolor)
        
        # Grid styling
        ax.grid(True, which='major', linestyle='-', linewidth=1.0, alpha=0.5, color='grey')
        ax.grid(True, which='minor', linestyle='-', linewidth=0.5, alpha=0.3, color='grey')
        
        # Add minor ticks
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        
        # Tick parameters - now pointing inwards
        ax.tick_params(which='major', length=10, width=1.0, direction='in')
        ax.tick_params(which='minor', length=5, width=0.5, direction='in')
        
        # Make ticks visible on all sides
        #ax.tick_params(top=True, right=True, which='both')
        
        # Make axis lines more prominent
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)
        
    
    if nrows == 1 and ncols == 1:
        return fig, axes[0]
    else:
        return fig, axes


def data_Helsinki():
    # Here we import and clean the data to only look at the population for Helsinki
    
    filename = "SSVAVR02_20250223-105323.csv"
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{filename}' not found. Please check the path.") from e


    #We replace missing data with NAN
    df.replace("..", np.nan, inplace=True)


    filtered_data = filter_by_areas_languages(df, ["Helsinki"], ["Suomi ja saame", "Ruotsi", "Muu kieli"])
    filtered_data = filtered_data.drop("Alue", axis=1)
    filtered_data.set_index("Äidinkieli", inplace=True)
    #Making sure the data is numeric
    filtered_data = filtered_data.apply(pd.to_numeric, errors="coerce")
    filtered_data = filtered_data.T

    return filtered_data


def all_languages_one_plot(save=False, filename="Plot1.pdf"):
    #This plots all of the languages in a single plot

    dat = data_Helsinki()    
    # Plot
    fig, ax = initialize_plot(figsize=(10, 8))
    for language in dat.columns:
        ax.plot(dat.index, dat[language], label=language)
    
    ax.legend()
    ax.set_xticks(dat.index[::5])
    ax.set_title("Helsingin väestö äidinkielen mukaan") # "Population of Helsinki according to mothertounge"
    ax.set_xlabel("Vuosi")  # Year
    ax.set_ylabel("Väestömäärä")  # Population count

    if save:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def languages_in_subplots_and_together(save=False, filename="Plot2.pdf"):
    #All three languages compared in a single figure with subplots

    dat = data_Helsinki()

    fig, axes = initialize_plot(nrows=2, ncols=2, figsize=(14, 10))

    
    colours = ["blue", "red", "green"]

    #First subplot is combines all the languages
    for i, language in enumerate(dat.columns):
        axes[0].plot(dat.index, dat[language], label=language, color=colours[i])

    axes[0].legend()
    axes[0].set_xticks(dat.index[::5])
    axes[0].set_xlabel("Vuosi")  # Year
    axes[0].set_ylabel("Väestömäärä")  # Population count
    #axes[0].set_title("Kaikki kielet")

    #rest of the subplots are for individual languages
    for i, language in enumerate(dat.columns):
        axes[i+1].plot(dat.index, dat[language], label=language, color=colours[i])
        axes[i+1].legend()
        axes[i+1].set_xticks(dat.index[::5])
        axes[i+1].set_xlabel("Vuosi")  # Year
        axes[i+1].set_ylabel("Väestömäärä")  # Population count
        #axes[i+1].set_title(language)

    fig.suptitle("Helsingin väestö äidinkielen mukaan")

    if save:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()



def main():
    all_languages_one_plot(save=True)
    languages_in_subplots_and_together(save=True)



main()