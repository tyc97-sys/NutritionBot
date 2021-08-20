from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from .models import *
import json
# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        # 當有事件傳入
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print("message", event.message)
                message = []

                if event.message.type == 'text':
                    mtext = event.message.text
                    uid = event.source.user_id
                    profile = line_bot_api.get_profile(uid)
                    name = profile.display_name
                    # 新增之好友
                    if User_Info.objects.filter(uid=uid).exists() == False:
                        User_Info.objects.create(uid=uid, name=name, mtext='', height=0.0, weight=0.0, age=0)  # 一開始設空格
                        text_ = "初次新增會員成功\n姓名: {}".format(name)
                        message.append(TextSendMessage(text_))

                    # 以新增過好友
                    elif User_Info.objects.filter(uid=uid).exists() == True:
                        user_info = User_Info.objects.filter(uid=uid)

                        for user in user_info:
                            height = user.height  # 讀取先前紀錄過之身高
                            weight = user.weight  # 讀取先前紀錄過之體重
                            age = user.age  # 讀取先前紀錄過之年齡
                            sex = user.sex # 讀取先前紀錄過的性別

                        if 'hi' in mtext.lower() or '嗨' in mtext or 'hello' in mtext.lower():
                            text_ = '{} 您好\n今天需要甚麼幫助？'.format(name)
                            message.append(TextSendMessage(text_))
                            message.append(
                                TemplateSendMessage(
                                    alt_text='Buttons template',
                                    template=ButtonsTemplate(
                                        title='Menu',
                                        text='請選擇需要甚麼服務',
                                        actions=[
                                            PostbackTemplateAction(
                                                label='輸入身體資訊',
                                                text='身體資訊',
                                                data='A&身高&體重&性別&年齡'
                                            ),
                                            PostbackTemplateAction(
                                                label='計算營養素',
                                                text='營養素',
                                                data='B&營養素'
                                            ),
                                            PostbackTemplateAction(
                                                label='想去運動',
                                                text='運動 gogo',
                                                data='C&運動'
                                            ),
                                            PostbackTemplateAction(
                                                label='想吃飯',
                                                text='吃吃吃',
                                                data='D&訂餐'
                                            )
                                        ]
                                    )
                                )
                            )

                        elif '身體資訊' in mtext:
                            if height == 0 or weight == 0 or age == 0:
                                text_ = '你還沒輸入過基本資訊'
                                message.append(TextSendMessage(text_))
                                text_ = '"請先輸入你的身高(cm)／體重(kg)／年齡／性別 (用空格區別)'
                                message.append(TextSendMessage(text_))

                            else:
                                text_ = "{} 您好\n上次輸入的身高：{} 體重：{} 年齡：{} 性別：{}\n是否需要重新輸入".format(name, height, weight, age, sex)
                                message.append(TextSendMessage(text_))
                                message.append(
                                    TemplateSendMessage(
                                        alt_text='Confirm template',
                                        template=ConfirmTemplate(
                                            text='確認嗎',
                                            actions=[
                                                MessageTemplateAction(
                                                    label='Yes',
                                                    text='Yes',
                                                ),
                                                MessageTemplateAction(
                                                    label='No',
                                                    text='No',
                                                ),
                                            ]
                                        )
                                    )
                                )


                    line_bot_api.reply_message(event.reply_token, message)
                        # if len(mtext.split()) == 3:
                        #     data_ = list(map(float, mtext.split()))
                        #     User_Info.objects.filter(uid=uid).update(height=data_[0])
                        #     User_Info.objects.filter(uid=uid).update(weight=data_[1])
                        #     User_Info.objects.filter(uid=uid).update(age=int(data_[2]))
                        #
                        #     text_ = "{} 您好\n您的身高：{} 體重：{} 年齡：{}。".format(name, data_[0], data_[1], int(data_[2]))
                        #
                        #     message.append(TextSendMessage(text_))
                        #
                        # elif height == 0 or weight == 0 or age == 0:
                        #     text_ = "請輸入你的身高(cm)／體重(kg)／年齡 (請用空格區別)"
                        #     message.append(TextSendMessage(text_))
                        #     print(mtext)
                        #
                        # elif 'Yes' in mtext:
                        #     User_Info.objects.filter(uid=uid).update(height=0)
                        #     User_Info.objects.filter(uid=uid).update(weight=0)
                        #     User_Info.objects.filter(uid=uid).update(age=0)
                        #     # text_ = "重整"
                        #     # message.append(TextSendMessage(text_))
                        #
                        # elif height != 0 and weight != 0 and age != 0:
                        #     text_ = "{} 您好\n上次輸入的身高：{} 體重：{} 年齡：{}\n是否需要重新輸入".format(name, height, weight, age)
                        #     message.append(TemplateSendMessage(
                        #         alt_text='Confirm template',
                        #         template=ConfirmTemplate(
                        #             text=text_,
                        #             actions=[
                        #                 MessageTemplateAction(
                        #                     label='Yes',
                        #                     text='Yes',
                        #                 ),
                        #                 MessageTemplateAction(
                        #                     label='No',
                        #                     text='No',
                        #                 ),
                        #             ])))



        return HttpResponse()
    else:
        return HttpResponseBadRequest()