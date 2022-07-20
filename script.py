from dotenv import load_dotenv
import blockfrost_api
import gspread
import os

# (policyID, worksheet name, #items)
policy_ids = [
    ('788cc573eb32a5378f1d25e6414228c0b7effd788e2f6fb2b11471f3', 'Shields', 555),
    ('11f757d6a582d14faf6a289c4fda728fd33cc1888d16172a964b2145', 'Swords', 1110)
]

load_dotenv()
BLOCKFROST_API_KEY = os.getenv('BLOCKFROST_API_KEY')
SHEET_IDENTITY = os.getenv('SHEET_IDENTITY')
BLOCKFROST_BASE_URL = os.getenv('BLOCKFROST_BASE_URL')

gc = gspread.service_account('google_creds.json')
for policy_id in policy_ids:
    assets = blockfrost_api.get_project_assets(policy_id[0], f'{policy_id[0]}.txt', BLOCKFROST_API_KEY, BLOCKFROST_BASE_URL)
    assets_info = blockfrost_api.get_assets_info(policy_id[0], BLOCKFROST_API_KEY, BLOCKFROST_BASE_URL, assets)

    sheet = gc.open_by_key(SHEET_IDENTITY)
    worksheet = sheet.worksheet(policy_id[1])
    worksheet.update(f'A1:C{policy_id[2]+1}',assets_info)