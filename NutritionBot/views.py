from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from .models import *
from .map import *
from .healthy_box import *
from .web_html import *
import folium
# from .rich_menu import *
import json

# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

text_history = ['歷史紀錄']
text_history1 = ['歷史紀錄']

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

        # rich_menu_id = create_menu()
        # set_menu_image(r"F:\AI\Line_Chatbot\NutritionBot\NutritionBot\rich-menu.png", rich_menu_id)
        # print(rich_menu_id)

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
                            BMR = user.bmr
                            water = user.water

                        if '身體資訊' in mtext:
                            if height == 0 or weight == 0 or age == 0:
                                text_ = '你還沒輸入過基本資訊'
                                message.append(TextSendMessage(text_))
                                text_ = '請先輸入你的身高(cm)／體重(kg)／年齡／性別 (用空格區別)'
                                message.append(TextSendMessage(text_))
                            else:
                                if sex == 1:
                                    sex_ = '女'
                                else:
                                    sex_ = '男'
                                text_ = "{} 您好\n上次輸入：\n身高：{}\n體重：{}\n年齡：{}\n性別：{}\n是否需要更改".format(name, height, weight,
                                                                                                  age, sex_)
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

                        elif len(mtext.split()) == 4:
                            info = mtext.split()
                            print(info)

                            text_confirm = "身高：{}\n體重：{}\n年齡：{}\n性別：{}\n再次確認，需要更改嗎？".format(info[0], info[1], info[2],
                                                                                            info[3])

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
                                BMR = 13.7 * weight + 5 * height - 6.8 * age + 66  # 男生 = (13.7×體重(公斤))+(5.0×身高(公分))-(6.8×年齡)+66
                            else:
                                BMR = 9.6 * weight + 1.8 * height - 4.7 * age + 655  # 女生 = (9.6×體重(公斤))+(1.8×身高(公分))-(4.7×年齡)+655

                            # text_ = '您的基礎代謝（BMR）為：{} kcal'.format(int(BMR))
                            # message.append(TextSendMessage(text_))
                            # print("BMR", int(BMR))
                            # User_Info.objects.filter(uid=uid).update(bmr=BMR)
                            #
                            water = float(weight * 30 / 1000)
                            # text_ = '每天需喝水：{:.1f}L'.format(water)
                            # message.append(TextSendMessage(text_))
                            # print("{:.1f}".format(water))
                            # User_Info.objects.filter(uid=uid).update(water=water)

                            text_ = '您的基礎代謝（BMR）為：{} kcal\n每天需喝水：{:.1f}L'.format(int(BMR), water)

                            User_Info.objects.filter(uid=uid).update(bmr=BMR)
                            User_Info.objects.filter(uid=uid).update(water=water)

                            message.append(
                                TemplateSendMessage(
                                    alt_text='Buttons template',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url="https://i.imgur.com/0484Uz3.png",
                                        imageAspectRatio="square",
                                        text=text_,
                                        actions=[
                                            MessageTemplateAction(
                                                label='OK 瞭解了',
                                                text='OK',
                                            ),
                                            MessageTemplateAction(
                                                label='甚麼是 BMR ?',
                                                text='BMR?',
                                            )])))

                        elif 'BMR?' in mtext:
                            text_ = 'BMR (Basal Metabolic Rate) 是基礎代謝率的英文縮寫，是指「人類一天不動也能消耗的熱量」! \n BMR 高的人在沒做甚麼事情時就消耗了許多熱量，代表著這種人在減肥來說更加容易；相反的BMR低的人就要更注意控制自己的飲食。'
                            message.append(TextSendMessage(text_))

                        elif '營養素' in mtext:
                            message.append(
                                TemplateSendMessage(
                                    alt_text='Buttons template',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url="https://i.imgur.com/1Gao7ZM.png",
                                        imageAspectRatio="square",
                                        title='終極目標',
                                        text='現在的目標是？',
                                        actions=[
                                            MessageTemplateAction(
                                                label='減脂 / 減重',
                                                text='減脂 / 減重'
                                            ),
                                            MessageTemplateAction(
                                                label='保持身材',
                                                text='保持身材'
                                            ),
                                            MessageTemplateAction(
                                                label='增肌 / 增重',
                                                text='增肌 / 增重'
                                            )])))

                        elif ('減脂 / 減重' in mtext) or ('保持身材' in mtext) or ('增肌 / 增重' in mtext):
                            text_history.append(mtext)

                            print('text_history', text_history)
                            text_ = '活動程度：\n- 無活動：久坐\n- 輕量活動：每周運動1-3天\n- 中度活動量：站走稍多、每周運動3-5天\n- 高度活動量：站走為主、每周運動6-7天'
                            message.append(TextSendMessage(text_))
                            message.append(
                                TemplateSendMessage(
                                    alt_text='Buttons template',
                                    # imageUrl="",
                                    # imageAspectRatio="square",
                                    template=ButtonsTemplate(
                                        thumbnail_image_url = "https://imgur.com/stpxRps.jpg",
                                        imageAspectRatio="square",
                                        title='活動程度',
                                        text='平常活動程度？',
                                        actions=[
                                            MessageTemplateAction(
                                                label='無活動',
                                                text='無活動'
                                            ),
                                            MessageTemplateAction(
                                                label='輕量活動',
                                                text='輕量活動'
                                            ),
                                            MessageTemplateAction(
                                                label='中度活動量',
                                                text='中度活動量'
                                            ),
                                            MessageTemplateAction(
                                                label='高度活動量',
                                                text='高度活動量'
                                            )])))

                        elif ('無活動' in mtext) or ('輕量活動' in mtext) or ('中度活動量' in mtext) or ('高度活動量' in mtext):
                            # text_history.append(mtext)
                            print('text_history', text_history)
                            print('mtext', mtext)

                            if '無活動' in mtext:
                                TDEE = 1.2 * BMR
                                text_='平日作息：{}\n每日的 TDEE：{} kcal'.format(mtext, int(TDEE))
                                message.append(TextSendMessage(text_))
                                if '減脂 / 減重' in text_history:
                                    TDEE = 0.8 * TDEE
                                    carb = TDEE * 0.45 / 4
                                    protein = TDEE * 0.35 / 4
                                    fat = TDEE * 0.2 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '保持身材' in text_history:
                                    TDEE = TDEE
                                    carb = TDEE * 0.55 / 4
                                    protein = TDEE * 0.15 / 4
                                    fat = TDEE * 0.3 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '增肌 / 增重' in text_history:
                                    TDEE = TDEE + 400
                                    carb = TDEE * 0.6 / 4
                                    protein = TDEE * 0.25 / 4
                                    fat = TDEE * 0.15 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                message.append(TextSendMessage(text_))
                            elif '輕量活動' in mtext:
                                TDEE = 1.375 * BMR
                                text_='平日作息：{}\n每日的 TDEE：{} kcal'.format(mtext, int(TDEE))
                                message.append(TextSendMessage(text_))
                                if '減脂 / 減重' in text_history:
                                    TDEE = 0.8 * TDEE
                                    carb = TDEE * 0.45 / 4
                                    protein = TDEE * 0.35 / 4
                                    fat = TDEE * 0.2 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '保持身材' in text_history:
                                    TDEE = TDEE
                                    carb = TDEE * 0.55 / 4
                                    protein = TDEE * 0.15 / 4
                                    fat = TDEE * 0.3 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '增肌 / 增重' in text_history:
                                    TDEE = TDEE + 400
                                    carb = TDEE * 0.6 / 4
                                    protein = TDEE * 0.25 / 4
                                    fat = TDEE * 0.15 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                message.append(TextSendMessage(text_))
                            elif '中度活動量' in mtext:
                                TDEE = 1.55 * BMR
                                text_='平日作息：{}\n每日的 TDEE：{} kcal'.format(mtext, int(TDEE))
                                message.append(TextSendMessage(text_))
                                if '減脂 / 減重' in text_history:
                                    TDEE = 0.8 * TDEE
                                    carb = TDEE * 0.45 / 4
                                    protein = TDEE * 0.35 / 4
                                    fat = TDEE * 0.2 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '保持身材' in text_history:
                                    TDEE = TDEE
                                    carb = TDEE * 0.55 / 4
                                    protein = TDEE * 0.15 / 4
                                    fat = TDEE * 0.3 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '增肌 / 增重' in text_history:
                                    TDEE = TDEE + 400
                                    carb = TDEE * 0.6 / 4
                                    protein = TDEE * 0.25 / 4
                                    fat = TDEE * 0.15 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                message.append(TextSendMessage(text_))
                            elif '高度活動量' in mtext:
                                TDEE = 1.725 * BMR
                                text_='平日作息：{}\n每日的 TDEE：{} kcal'.format(mtext, int(TDEE))
                                message.append(TextSendMessage(text_))
                                if '減脂 / 減重' in text_history:
                                    TDEE = 0.8 * TDEE
                                    carb = TDEE * 0.45 / 4
                                    protein = TDEE * 0.35 / 4
                                    fat = TDEE * 0.2 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '保持身材' in text_history:
                                    TDEE = TDEE
                                    carb = TDEE * 0.55 / 4
                                    protein = TDEE * 0.15 / 4
                                    fat = TDEE * 0.3 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                elif '增肌 / 增重' in text_history:
                                    TDEE = TDEE + 400
                                    carb = TDEE * 0.6 / 4
                                    protein = TDEE * 0.25 / 4
                                    fat = TDEE * 0.15 / 9

                                    text_ = '若你想{}，那麼為這個目標所訂的 TDEE：{} kcal\n\n建議的營養素：\n- 碳水化合物：{:.1f} g\n- 蛋白脂：{:.1f} g\n- 脂肪：{:.1f} g'.format(
                                        text_history.pop(), int(TDEE), carb, protein, fat)

                                message.append(TextSendMessage(text_))
                                # 這邊先用文字代替，之後可以改成圖片，圖片最下面顯示"想知道詳細資訊請點擊圖片"之類的文字

                            text_ = '想更瞭解 TDEE 嗎？'
                            message.append(
                                TemplateSendMessage(
                                    alt_text='Confirm template',
                                    template=ConfirmTemplate(
                                        text=text_,
                                        actions=[
                                            MessageTemplateAction(
                                                label='好挖',
                                                text='好挖',
                                            ),
                                            MessageTemplateAction(
                                                label='不用了',
                                                text='不用了',
                                            )])))
                        elif '好挖' in mtext:
                            text_ = "甚麼是 TDEE？\nTDEE 全名 Total Daily Energy Expenditure\n是總熱量消耗的英文縮寫，指身體一整天所消耗掉的熱量。\n\n當 攝取的卡路里 = TDEE時，體重會維持"
                            message.append(TextSendMessage(text_))

                        elif "運動gogo" in mtext:
                            text_history1.append("運動gogo")
                            text_ = "請傳送位置訊息。\n將會為您找到最近的運動場所。"
                            message.append(TextSendMessage(text_))
                        elif "吃" in mtext:
                            text_history1.append("吃")
                            text_ = "請傳送位置訊息。\n將會為您找到最近的幾間健康餐盒專賣店。"
                            message.append(TextSendMessage(text_))

                        elif "菜單" in mtext:
                            if "樂坡" in mtext:
                                message.append(
                                    ImageSendMessage(
                                        original_content_url='https://i.imgur.com/iDwPOHB.jpg',
                                        preview_image_url='https://i.imgur.com/iDwPOHB.jpg'
                                    )
                                )
                            elif "好餵" in mtext:
                                message.append(
                                    ImageSendMessage(
                                        original_content_url='https://i.imgur.com/dWTdC4F.jpg',
                                        preview_image_url='https://i.imgur.com/dWTdC4F.jpg'
                                    )
                                )
                            elif "常常" in mtext:
                                message.append(
                                    ImageSendMessage(
                                        original_content_url='https://imgur.com/JJexRti.jpg',
                                        preview_image_url='https://imgur.com/JJexRti.jpg'
                                    )
                                )
                            elif "海灘" in mtext:
                                message.append(
                                    ImageSendMessage(
                                        original_content_url='https://i.imgur.com/IXsVXgE.jpg',
                                        preview_image_url='https://i.imgur.com/IXsVXgE.jpg'
                                    )
                                )
                        elif "電話" in mtext:
                            if "樂坡" in mtext:
                                message.append(
                                    TextSendMessage(
                                        text='+886-900609159'
                                    )
                                )
                            elif "好餵" in mtext:
                                message.append(
                                    TextSendMessage(
                                        text='+886-978705252'
                                    )
                                )
                            elif "常常" in mtext:
                                message.append(
                                    TextSendMessage(
                                        text='+886-2-23582356'
                                    )
                                )
                            elif "海灘" in mtext:
                                message.append(
                                    TextSendMessage(
                                        text='+886-2-23778977'
                                    )
                                )



                    print(text_history1, text_history)
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'location':
                    # latitude = event.message.latitude
                    # longitude = event.message.longitude
                    # print(text_history1.pop())
                    location = [event.message.latitude, event.message.longitude]

                    history = text_history1.pop()

                    if "運動gogo" in history:

                        path = r'F:\AI\Line_Chatbot\NutritionBot\fitness.geojson'

                        text_, addr_, name_, coor_ = find_nearest_place(location=location, path=path)
                        message.append(TextSendMessage(text_))

                        print(addr_, name_)

                        line_bot_api.reply_message(event.reply_token, LocationSendMessage(title=name_, address='Taipei', latitude=coor_[0], longitude=coor_[1]))

                    elif "吃" in history:

                        path = r'F:\AI\Line_Chatbot\NutritionBot\restaurant.geojson'

                        # sending_text1, sending_text2, sending_text3 = find_nearest_restaurant(location=location, path=path)
                        #
                        # message.append(TextSendMessage(sending_text1))
                        # message.append(TextSendMessage(sending_text2))
                        # message.append(TextSendMessage(sending_text3))

                        line_bot_api.reply_message(event.reply_token, find_nearest_restaurant(location=location, path=path))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
