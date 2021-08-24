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

flag_ = []

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
                            sex = user.sex  # 讀取先前紀錄過的性別

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
                                            )])))

                        elif '身體資訊' in mtext:
                            if height == 0 or weight == 0 or age == 0:
                                text_ = '你還沒輸入過基本資訊'
                                message.append(TextSendMessage(text_))
                                text_ = '"請先輸入你的身高(cm)／體重(kg)／年齡／性別 (用空格區別)'
                                message.append(TextSendMessage(text_))
                            else:
                                if sex == 1:
                                    sex_ = '女'
                                else:
                                    sex_ = '男'
                                text_ = "{} 您好\n上次輸入：\n身高：{}\n體重：{}\n年齡：{}\n性別：{}\n是否需要更改".format(name, height, weight, age, sex_)
                                message.append(TextSendMessage(text_))
                                message.append(
                                    TemplateSendMessage(
                                        alt_text='Confirm template',
                                        template=ConfirmTemplate(
                                            text='要更改嗎',
                                            actions=[
                                                MessageTemplateAction(
                                                    label='Yes',
                                                    text='Yes',
                                                ),
                                                MessageTemplateAction(
                                                    label='No',
                                                    text='No',
                                                )])))
                        elif '營養素' in mtext:
                            message.append(
                                TemplateSendMessage(
                                    alt_text='Buttons template',
                                    template=ButtonsTemplate(
                                        title='終極目標',
                                        text='現在的目標是？',
                                        actions=[
                                            PostbackTemplateAction(
                                                label='減脂／減重',
                                                text='減脂 減重',
                                                data='E&減脂'
                                            ),
                                            PostbackTemplateAction(
                                                label='保持身材',
                                                text='保持身材',
                                                data='F&保持身材'
                                            ),
                                            PostbackTemplateAction(
                                                label='增肌／增重',
                                                text='增肌 增重',
                                                data='G&增肌'
                                            )])))

                        elif len(mtext.split()) == 4:
                            info = mtext.split()
                            print(info)

                            text_confirm = "身高：{}\n體重：{}\n年齡：{}\n性別：{}\n再次確認，需要更改嗎？".format(name, info[0], info[1], info[2], info[3])

                            if '女' in info:
                                info[3] = 1
                            else:
                                info[3] = 0
                            print(info)

                            User_Info.objects.filter(uid=uid).update(height=info[0])
                            User_Info.objects.filter(uid=uid).update(weight=info[1])
                            User_Info.objects.filter(uid=uid).update(age=info[2])
                            User_Info.objects.filter(uid=uid).update(sex=info[3])

                            text_ = '已更新完畢！'
                            message.append(TextSendMessage(text_))
                            message.append(
                                TemplateSendMessage(
                                    alt_text='Confirm template',
                                    template=ConfirmTemplate(
                                        text=text_confirm,
                                        actions=[
                                            MessageTemplateAction(
                                                label='Yes',
                                                text='Yes',
                                            ),
                                            MessageTemplateAction(
                                                label='No',
                                                text='No',
                                            )])))

                        elif 'Yes' in mtext:
                            text_ = '那麼請重新輸入\n身高(cm)／體重(kg)／年齡／性別 (用空格區別)'
                            message.append(TextSendMessage(text_))

                        elif 'No' in mtext:
                            if sex == 0:
                                BMR = 13.7 * weight + 5 * height - 6.8 * age + 66 # 男生 = (13.7×體重(公斤))+(5.0×身高(公分))-(6.8×年齡)+66
                            else:
                                BMR = 9.6 * weight + 1.8 * height - 4.7 * age + 655  # 女生 = (9.6×體重(公斤))+(1.8×身高(公分))-(4.7×年齡)+655

                            text_ = '您的基礎代謝（BMR）為：{} kcal'.format(int(BMR))
                            message.append(TextSendMessage(text_))
                            print("BMR", int(BMR))

                            water = float(weight * 30 / 1000)
                            text_ = '每天需喝水：{:.1f} L'.format(water)
                            message.append(TextSendMessage(text_))
                            print("{:.1f}".format(water))

                    line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()