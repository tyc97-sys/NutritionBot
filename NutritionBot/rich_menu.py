import requests
import json

token = 'mxJdY40QwXP/pQR6Vilr8J7fBdsLD9E6whHFlUL0Z+XC5BtQtRI1ZKBg/PTpnTYSINtaFnMEcwu7ZKnHjrFnI4mcRnHMr3bwpq9xuBruXPnQRktRkwtTZESrRieAmVW0Rn/NxuQfWNTaKwhxSfgXqgdB04t89/1O/w1cDnyilFU='

headers = {"Authorization":"Bearer mxJdY40QwXP/pQR6Vilr8J7fBdsLD9E6whHFlUL0Z+XC5BtQtRI1ZKBg/PTpnTYSINtaFnMEcwu7ZKnHjrFnI4mcRnHMr3bwpq9xuBruXPnQRktRkwtTZESrRieAmVW0Rn/NxuQfWNTaKwhxSfgXqgdB04t89/1O/w1cDnyilFU=", "Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 843},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "Controller",
    "areas":[
        {
          "bounds": {"x": 551, "y": 325, "width": 321, "height": 321},
          "action": {"type": "message", "text": "up"}
        },
        {
          "bounds": {"x": 876, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "right"}
        },
        {
          "bounds": {"x": 551, "y": 972, "width": 321, "height": 321},
          "action": {"type": "message", "text": "down"}
        },
        {
          "bounds": {"x": 225, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "left"}
        },
        {
          "bounds": {"x": 1433, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn b"}
        },
        {
          "bounds": {"x": 1907, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn a"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)
# print(type(req.text))



from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi(token)
rich_menu_id = 'richmenu-da7b4e4631f5358c6d32d86f371ac67f'
#
# path = r'F:\AI\Line_Chatbot\NutritionBot\NutritionBot\rich-menu.png'
#
# with open(path, 'rb') as f:
#     line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)
print(req.text)

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)
