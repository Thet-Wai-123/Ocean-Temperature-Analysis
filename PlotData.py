from matplotlib import pyplot as plt

def plot_data(df, x, y, xLabel, yLabel, title):
    plt.figure(figsize=(12, 6))
    plt.plot(df[x], df[y])  
    plt.xlabel(xLabel) 
    plt.ylabel(yLabel)
    plt.title(title)
    plt.show()