import muselsl
import csv
from muselsl import stream, list_muses
from pylsl import StreamInlet, resolve_byprop
import numpy as np
import time

# Check available Muse devices
csv_file = "muse_data.csv"
csv_columns = ['Timestamp', 'TP9', 'AF7', 'AF8', 'TP10']
with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        #writer.writeheader()
data = {'Timestamp': 0, 'TP9': 0, 'AF7': 0, 'AF8': 0, 'TP10': 0}
stream_inlet = muselsl.stream
# Wait for the stream to be available
streams = resolve_byprop('type', 'EEG', timeout=2)
print(streams)
if streams:
    inlet = StreamInlet(streams[0], max_chunklen=1)
    print(inlet)
    while True:
        eeg_data, timestamp = inlet.pull_chunk(timeout=2.0, max_samples=1)
        if timestamp:
            data['Timestamp'] = timestamp
            data['TP9'] = eeg_data[0][0]
            data['AF7'] = eeg_data[0][1]
            data['AF8'] = eeg_data[0][2]
            data['TP10'] = eeg_data[0][3]
            with open(csv_file, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(data)
                print(np.array(eeg_data).shape)  # Print shape to check the incoming data
                print(eeg_data)
        time.sleep(1)