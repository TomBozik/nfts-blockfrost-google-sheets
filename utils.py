import pickle
import csv

def save_assets_to_file(assets, filename):
    with open(filename, 'wb') as f:
        pickle.dump(assets, f)

def load_assets_from_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def decode_asset_name(name, policy_id):
    asset_hex_name = name[len(policy_id):]
    return bytearray.decode(bytearray.fromhex(asset_hex_name))

def save_csv(data, headers, filename):
    data = [headers] + data
    with open(filename, "w", newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(data)
