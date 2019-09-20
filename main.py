import gspread
from flask import jsonify, make_response
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime, timedelta
import os

KEY = json.loads(os.environ.get('CREDENTIALS'))

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(KEY, scope)


def process(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        print(f"Look a {request.method}!!")
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    print(f"args: {request.args} | data: {request.data} | json: {request.get_json()}")
    data = request.get_json(silent=True)

    name = data.get('name')

    adults = data.get('guest_adult', '0')
    adults = 1 if adults == "Apenas eu" else adults

    kids = data.get('guest_kid', '0')
    kids = 0 if kids == "Nenhuma" else kids

    gc = gspread.authorize(creds)
    sheet = gc.open_by_url(os.environ.get('SHEET_URL')).worksheet("_site")

    next_row = next_available_row(sheet)

    dt = datetime.now() - timedelta(hours=3)
    sheet.update_acell(f'A{next_row}', dt.isoformat())
    sheet.update_acell(f'B{next_row}', name)
    sheet.update_acell(f'C{next_row}', adults)
    sheet.update_acell(f'D{next_row}', kids)

    data = {'message': 'Created', 'code': 'SUCCESS'}

    return json.dumps(data), 201, headers


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list) + 1)
