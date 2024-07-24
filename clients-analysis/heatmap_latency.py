import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_data(file_path):
    # Read CSV file, assuming the first column is the index
    data = pd.read_csv(file_path, index_col=0, sep='\t')
    return data

def plot_heatmap(data):
    # Create a heatmap using seaborn
    
    plt.figure(figsize=(30, 12))  # You can adjust the figure size as needed
    
    # Set font size to 22
    sns.set(font_scale=2.0)
    
    # sns.set_style({'font.family': 'serif', 'font.serif': ['Times New Roman'], 'font.size': 4})
    sns.set_style({'font.size': 22})

    # Plot data without decimal case
    # get the fig and ax objects

    g = sns.heatmap(data, annot=True, fmt="d", cmap='viridis', annot_kws={"size": 22})
    # g = sns.heatmap(data, annot=True, fmt=".1f", cmap='viridis', annot_kws={"size": 22})
    
    # plt.title('Latência para cada par de nós (ms)')

    # Put the x axis on top
    plt.ylabel('De')
    plt.xlabel('Para')
    g.axes.xaxis.set_ticks_position("top")
    g.axes.xaxis.set_label_position("top")

    # Remove margin
    plt.margins(0, 0)

    plt.savefig('heatmap_latency.pdf')  # Save the heatmap as an image

def main():
    file_path = 'latency_data.csv'  # Change this to your actual file path
    latency_data = read_data(file_path)
    
    # Round the data to the nearest integer
    latency_data = latency_data.round(0).astype(int)
    print(latency_data)

    plot_heatmap(latency_data)

if __name__ == "__main__":
    main()
