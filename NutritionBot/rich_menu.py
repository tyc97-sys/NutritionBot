import requests
import json

token = 'mxJdY40QwXP/pQR6Vilr8J7fBdsLD9E6whHFlUL0Z+XC5BtQtRI1ZKBg/PTpnTYSINtaFnMEcwu7ZKnHjrFnI4mcRnHMr3bwpq9xuBruXPnQRktRkwtTZESrRieAmVW0Rn/NxuQfWNTaKwhxSfgXqgdB04t89/1O/w1cDnyilFU='

headers = {"Authorization":"Bearer mxJdY40QwXP/pQR6Vilr8J7fBdsLD9E6whHFlUL0Z+XC5BtQtRI1ZKBg/PTpnTYSINtaFnMEcwu7ZKnHjrFnI4mcRnHMr3bwpq9xuBruXPnQRktRkwtTZESrRieAmVW0Rn/NxuQfWNTaKwhxSfgXqgdB04t89/1O/w1cDnyilFU=" , "Content-Type":"application/json"}

# body = {
#     "size": {"width": 2500, "height": 1686},
#     "selected": "false",
#     "name": "Menu",
#     "chatBarText": "更多資訊",
#     "areas":[
#         {
#           "bounds": {"x": 113, "y": 45, "width": 1036, "height": 762},
#           "action": {"type": "message", "text": "身體資訊"}
#         },
#         {
#           "bounds": {"x": 1321, "y": 45, "width": 1036, "height": 762},
#           "action": {"type": "message", "text": "營養素"}
#         },
#         {
#           "bounds": {"x": 113, "y": 910, "width": 1036, "height": 762},
#           "action": {"type": "message", "text": "吃"}
#         },
#         {
#           "bounds": {"x": 1321, "y": 910, "width": 1036, "height": 762},
#           "action": {"type": "message", "text": "運動gogo"}
#         }
#     ]
#   }
#
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                        headers=headers,data=json.dumps(body).encode('utf-8'))
#
# print(req.text)


from linebot import (
    LineBotApi, WebhookHandler
)
# # =======================================================
line_bot_api = LineBotApi(token)
rich_menu_id = 'richmenu-5da46afbb97bea26bd8a998e58e60642'
# # =======================================================
# path = r'F:\AI\Line_Chatbot\NutritionBot\menu.jpg'
#
# with open(path, 'rb') as f:
#     line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)
# # =======================================================
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)
print(req.text)

rich_menu_list = line_bot_api.get_rich_menu_list()


# # =======================================================
# line_bot_api.delete_rich_menu(rich_menu_id)