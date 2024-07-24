#! /bin/bash


#! /bin/bash

mkdir .tmp_exp_analyzer

# If file not exist
if [ ! -f pcap_to_csv ]; then
    echo "Compiling pcap_to_csv..."
    make
fi

EXPFILE=$1

tar -zxf $EXPFILE -C .tmp_exp_analyzer --wildcards '*server*'

echo "Extracted $EXPFILE"

echo "Running experiment analyzer..."
cd .tmp_exp_analyzer
for f in *.tar; do mkdir ${f}.files; tar -xf "$f" -C ${f}.files; done

# Find recursevely all .pcap files and iterate over them
for f in $(find . -name "*.pcap"); do
    echo "Converting $f to csv..."
    # tshark -r $f -T fields -e frame.time_epoch -e frame.len -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.seq -e tcp.ack -e tcp.flags -e tcp.window_size -e tcp.analysis.ack_rtt -e tcp.analysis.ack_rtt -e tcp.analysis.bytes_in_flight
    ../pcap_to_csv $f packets.csv
    python3 ../analyze_output_pcap.py -s 16 -f packets.csv
done

cd ..
echo "Experiment analyzer finished"
rm -rf .tmp_exp_analyzer