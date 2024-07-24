import pandas as pd

import matplotlib.pyplot as plt

from tqdm.auto import tqdm



def read_data(file_path):

    data = pd.read_csv(file_path)

    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%H:%M:%S.%f')

    return data



def compute_metrics(data, freq='S'):

    data.set_index('Timestamp', inplace=True)



    # Start counting the timestamp from 0

    data.index = data.index - data.index[0]

    throughput = data['Packet Size'].resample(freq).sum()  # Sum of packet sizes

    packet_counts = data['Packet Size'].resample(freq).count()  # Count of packets

    return throughput, packet_counts



def plot_metrics(throughput, packet_counts, freq, fontsize, expected_time):

    fig, ax1 = plt.subplots(figsize=(12, 6))


    # convert expected_time to Timedelta
    expected_time = pd.Timedelta(seconds=expected_time)


    color = 'tab:red'

    ax1.set_xlabel('Tempo (segundos)', fontsize=fontsize, fontweight='bold')

    ax1.set_ylabel('Vazão (MB)', color=color, fontsize=fontsize, fontweight='bold')



    # Plot x axis as time
    # "Recover" the initial part not captured in the pcap file
    # data_x = throughput.index/1000000000
    data_x = throughput.index
    print(max(throughput.index))
    print(expected_time)
    if max(data_x) < expected_time:
        data_x = data_x + (expected_time - max(data_x))

    
    ax1.plot(data_x/1000000000, throughput.values/(2**20), color=color)

    ax1.tick_params(axis='y', labelcolor=color)



    ax2 = ax1.twinx()

    color = 'tab:blue'

    ax2.set_ylabel('Número de Pacotes', color=color, fontsize=fontsize, fontweight='bold')

    data_x = packet_counts.index
    if max(data_x) < expected_time:
        data_x = data_x + (expected_time - max(data_x))

    ax2.plot(data_x/1000000000, packet_counts.values, color=color)

    ax2.tick_params(axis='y', labelcolor=color)



    # Avoid using scientific notation

    ax1.get_xaxis().get_major_formatter().set_scientific(False)

    ax1.get_yaxis().get_major_formatter().set_scientific(False)

    ax2.get_yaxis().get_major_formatter().set_scientific(False)



    # Set font size

    ax1.tick_params(axis='both', which='major', labelsize=fontsize)

    ax2.tick_params(axis='both', which='major', labelsize=fontsize)



    plt.show()



def main():



    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--input_file', dest='input_file', required=True)

    parser.add_argument('-s', '--fontsize', dest='fontsize', type=int, default=12, help='Font size for the plot')

    parser.add_argument('-t', '--expected_time', dest='time', type=int, default=60, help='Experiment expected time in seconds')

    args = parser.parse_args()



    file_path = args.input_file

    expected_time = args.time

    # freq_options = {'S': 'Second', 'T': 'Minute', 'H': 'Hour', 'D': 'Day', 'M': 'Month', 'Y': 'Year'}

    freq_options = {'S': 'Second'}

    

    data = read_data(file_path)

    

    

    for freq, label in tqdm(freq_options.items(), desc="Computing and plotting metrics"):

        throughput, packet_counts = compute_metrics(data, freq=freq)

        plot_metrics(throughput, packet_counts, label, args.fontsize, expected_time)



if __name__ == '__main__':

    main()