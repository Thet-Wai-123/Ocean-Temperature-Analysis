from matplotlib import pyplot as plt
import numpy as np

def plot_data(df, x, y, xLabel, yLabel, title):
    plt.figure(figsize=(12, 6))
    plt.plot(df[x], df[y])  
    plt.xlabel(xLabel) 
    plt.ylabel(yLabel)
    plt.title(title)
    plt.show()

def plot_multiple_data(df, x, y_list, labels, xLabel, yLabel, title):
    plt.figure(figsize=(20, 6))
    colors = ['blue', 'orange']
    for y, label, color in zip(y_list, labels, colors):
        plt.plot(df[x], df[y], label=label, alpha = 0.5, color=color)
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()