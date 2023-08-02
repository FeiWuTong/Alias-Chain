import argparse
import json

class ArguCompressor:
    def __init__(self, alias_map_file):
        self.alias_map = self.read_alias_map(alias_map_file)

    def read_alias_map(self, file_path):
        with open(file_path, 'r') as f:
            alias_map = json.load(f)
        return alias_map

    def compress_argu(self, argu):
        aVec = bytearray()
        zVec = bytearray()
        alias_argu = bytearray(argu[:4])

        for i in range(4, len(argu), 32):
            chunk = argu[i:i+32]
            found = False

            for key, value in self.alias_map.items():
                if chunk == bytearray(key):
                    alias_argu.extend(value)
                    aVec.append(1)
                    found = True
                    break

            if not found:
                leading_zeros = 0
                for char in chunk:
                    if char == 0:
                        leading_zeros += 1
                    else:
                        break

                alias_argu.extend(chunk[leading_zeros:])
                zVec.append(leading_zeros)

        return alias_argu, aVec, zVec

    def process_argu_list(self, argu_list):
        alias_argu_list = []
        aVec_list = []
        zVec_list = []

        for argu in argu_list:
            alias_argu, aVec, zVec = self.compress_argu(argu.encode())
            alias_argu_list.append(alias_argu.hex())
            aVec_list.append(list(aVec))
            zVec_list.append(list(zVec))

        return alias_argu_list, aVec_list, zVec_list

    def run(self, input_file, output_file):
        with open(input_file, 'r') as f:
            input_data = json.load(f)

        alias_argu_list, aVec_list, zVec_list = self.process_argu_list(input_data["argu_list"])

        with open(output_file, 'w') as f:
            json.dump({
                "Alias-Argu": alias_argu_list,
                "aVec": aVec_list,
                "zVec": zVec_list
            }, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress Argu to Alias-Argu using Alias-Map")
    parser.add_argument("input_file", help="Path to the input json file containing Argu list")
    parser.add_argument("output_file", help="Path to the output json file to save Alias-Argu list")
    parser.add_argument("alias_map_file", help="Path to the json file containing the Alias-Map")

    args = parser.parse_args()

    compressor = ArguCompressor(args.alias_map_file)
    compressor.run(args.input_file, args.output_file)
