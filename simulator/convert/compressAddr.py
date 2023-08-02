import csv
import json
import random
import argparse

class AddrCompressor:
    def __init__(self, csv_file):
        self.addr_list = self.read_csv(csv_file)

    def read_csv(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            addr_list = [row[0] for row in reader]
        return addr_list

    def build_freq_map(self):
        freq_map = {}
        for addr in self.addr_list:
            freq_map[addr] = freq_map.get(addr, 0) + 1

        sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: item[1], reverse=True))
        return sorted_freq_map

    def assign_alias_addr(self, sorted_freq_map):
        alias_map = {}
        alias_byte_lengths = [1, 2, 3, 4]

        for addr, freq in sorted_freq_map.items():
            alias_byte_length = alias_byte_lengths[min(len(alias_byte_lengths) - 1, freq - 1)]
            alias_addr = bytes([random.randint(0, 255) for _ in range(alias_byte_length)])
            alias_map[addr] = alias_addr

        return alias_map

    def compress(self, json_file, output_file):
        with open(json_file, 'r') as f:
            addr_list = json.load(f)

        sorted_freq_map = self.build_freq_map()
        alias_map = self.assign_alias_addr(sorted_freq_map)

        alias_addr_list = []
        for addr in addr_list:
            alias_addr = alias_map.get(addr)
            if alias_addr is not None:
                alias_addr_list.append(alias_addr.hex())

        with open(output_file, 'w') as f:
            json.dump(alias_addr_list, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress Addr to Alias-Addr using CSV data")
    parser.add_argument("csv_file", help="Path to the input CSV file containing Addr list")
    parser.add_argument("json_file", help="Path to the input JSON file containing Addr list for compression")
    parser.add_argument("output_file", help="Path to the output JSON file to save Alias-Addr list")

    args = parser.parse_args()

    compressor = AddrCompressor(args.csv_file)
    compressor.compress(args.json_file, args.output_file)
