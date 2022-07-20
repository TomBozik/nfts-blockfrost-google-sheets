import requests
import os
from pycardano import Address, Network
import utils

def get_project_assets(project_policy, assets_filename, blockfrost_api_key, blockfrost_base_url):
    '''
        Downloads (and save to file) the assets from the blockfrost API, if there is already a file with assets, just loads them from the file.
    '''
    if not os.path.exists(assets_filename):
        headers = { 'project_id': blockfrost_api_key }
        all_assets = []
        page = 1

        while True:
            assets = requests.get(f'{blockfrost_base_url}/assets/policy/{project_policy}?page={page}', headers=headers)
            if 'error' in assets.json():
                return []
            if len(assets.json()) == 0:
                break
            for asset in assets.json():
                all_assets.append(asset['asset'])
            page += 1
        utils.save_assets_to_file(all_assets, assets_filename)
        return all_assets

    else:
        return utils.load_assets_from_file(assets_filename)



def get_assets_info(policy_id, blockfrost_api_key, blockfrost_base_url, assets):
    '''
        Downloads the assets info from the blockfrost API (name, address, stake key).
    '''
    headers = { 'project_id': blockfrost_api_key }
    data = []
    for i, asset in enumerate(assets):
        print(f'Asset {i}')
        if asset != policy_id:
            asset_info = requests.get(f'{blockfrost_base_url}/assets/{asset}/addresses', headers=headers)

            if 'error' in asset_info.json():
                return []

            if len(asset_info.json()) != 0:
                address = asset_info.json()[0]['address']
            else:
                address = 'NOT FOUND'

            try:
                addr = Address.from_primitive(str(address))
                addr_stake = Address(staking_part=addr.staking_part, network=Network.MAINNET)
            except:
                addr_stake = 'NOT FOUND'

            data.append([utils.decode_asset_name(asset, policy_id), address, str(addr_stake)])

    utils.save_csv(data, ['name', 'address', 'stake'], f'{policy_id}.csv')
    return [['name', 'address', 'stake']] + data