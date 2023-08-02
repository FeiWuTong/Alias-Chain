import csv
import json
import random
import argparse

class ValueCompressor:
    def __init__(self, csv_file):
        self.value_list = self.read_csv(csv_file)

    def read_csv(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            value_list = [int(row[0]) for row in reader]
        return value_list

    def build_freq_map(self):
        freq_map = {}
        for value in self.value_list:
            freq_map[value] = freq_map.get(value, 0) + 1

        sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: item[1], reverse=True))
        return sorted_freq_map

    def assign_alias_value(self, sorted_freq_map):
        alias_map = {}
        alias_byte_lengths = [1, 2, 3, 4]

        for value, freq in sorted_freq_map.items():
            alias_byte_length = alias_byte_lengths[min(len(alias_byte_lengths) - 1, freq - 1)]
            alias_value = random.randint(0, 2 ** (8 * alias_byte_length) - 1)
            alias_map[value] = alias_value

        return alias_map

    def compress(self, json_file, output_file):
        with open(json_file, 'r') as f:
            value_list = json.load(f)

        sorted_freq_map = self.build_freq_map()
        alias_map = self.assign_alias_value(sorted_freq_map)

        alias_value_list = []
        for value in value_list:
            alias_value = alias_map.get(value)
            if alias_value is not None:
                alias_value_list.append(alias_value)

        with open(output_file, 'w') as f:
            json.dump(alias_value_list, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress Value to Alias-Value using CSV data")
    parser.add_argument("csv_file", help="Path to the input CSV file containing Value list")
    parser.add_argument("json_file", help="Path to the input JSON file containing Value list for compression")
    parser.add_argument("output_file", help="Path to the output JSON file to save Alias-Value list")

    args = parser.parse_args()

    compressor = ValueCompressor(args.csv_file)
    compressor.compress(args.json_file, args.output_file)
