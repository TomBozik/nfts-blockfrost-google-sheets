from dotenv import load_dotenv
import blockfrost_api
import gspread
import os

load_dotenv()
BLOCKFROST_API_KEY = os.getenv('BLOCKFROST_API_KEY')
POLICY_ID = os.getenv('POLICY_ID')
SHEET_IDENTITY = os.getenv('SHEET_IDENTITY')
BLOCKFROST_BASE_URL = os.getenv('BLOCKFROST_BASE_URL')

assets = blockfrost_api.get_project_assets(POLICY_ID, f'{POLICY_ID}.txt', BLOCKFROST_API_KEY, BLOCKFROST_BASE_URL)
assets_info = blockfrost_api.get_assets_info(POLICY_ID, BLOCKFROST_API_KEY, BLOCKFROST_BASE_URL, assets)

# https://cloud.google.com/iam/docs/write-policy-client-libraries
gc = gspread.service_account('google_creds.json')
content = open(f'{POLICY_ID}.csv', 'r').read()
gc.import_csv(SHEET_IDENTITY, content)