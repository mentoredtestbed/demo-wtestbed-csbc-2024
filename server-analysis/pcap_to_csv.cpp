#include <iostream>
#include <fstream>
#include <pcap.h>
#include <ctime>
#include <chrono>
#include <iomanip>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <input pcap file> <output csv file>\n";
        return 1;
    }

    char errbuff[PCAP_ERRBUF_SIZE];
    pcap_t *pcap = pcap_open_offline(argv[1], errbuff);
    if (pcap == nullptr) {
        std::cerr << "Error reading pcap file: " << errbuff << std::endl;
        return 1;
    }

    std::ofstream outputFile(argv[2]);
    outputFile << "Timestamp,Packet Size\n";

    struct pcap_pkthdr *header;
    const u_char *data;
    struct tm *ltime;
    char timestr[16];
    time_t local_tv_sec;

    // Determine the size of the file for progress calculation
    std::ifstream file(argv[1], std::ifstream::ate | std::ifstream::binary);
    std::streamsize fileSize = file.tellg();
    file.close();

    std::streamsize processedBytes = 0;
    std::streamsize dataChunkSize;

    // Read and process packets
    while (int returnValue = pcap_next_ex(pcap, &header, &data) >= 0) {
        // Convert the timestamp to readable format
        local_tv_sec = header->ts.tv_sec;
        ltime=localtime(&local_tv_sec);
        strftime(timestr, sizeof timestr, "%H:%M:%S", ltime);

        outputFile << timestr << "." << header->ts.tv_usec << "," << header->len << "\n";

        // Estimate the size of data processed
        dataChunkSize = sizeof(struct pcap_pkthdr) + header->caplen;
        processedBytes += dataChunkSize;

        // Calculate and display progress
        float progress = (processedBytes * 100.0) / fileSize;
        std::cout << "\rProgress: " << std::fixed << std::setprecision(2) << progress << "%";
        std::cout.flush();
    }

    std::cout << "\nFinished processing packets.\n";

    pcap_close(pcap);
    outputFile.close();
    std::cout << "CSV file created successfully.\n";

    return 0;
}
