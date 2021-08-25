
import requests

headers = {"Authorization":"Bearer mxJdY40QwXP/pQR6Vilr8J7fBdsLD9E6whHFlUL0Z+XC5BtQtRI1ZKBg/PTpnTYSINtaFnMEcwu7ZKnHjrFnI4mcRnHMr3bwpq9xuBruXPnQRktRkwtTZESrRieAmVW0Rn/NxuQfWNTaKwhxSfgXqgdB04t89/1O/w1cDnyilFU=",
           "Content-Type":"application/json"}

rich_menu_id = 'richmenu-da7b4e4631f5358c6d32d86f371ac67f'

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)

print(req.text)


from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('3Ma92PMIfy790Z...')

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)