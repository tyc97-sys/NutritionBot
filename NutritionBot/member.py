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
from .member import *
import json
def check_id(event):
    message = []
    uid = event.source.user_id
    profile = line_bot_api.get_profile(uid)
    name = profile.display_name

    if User_Info.objects.filter(uid=uid).exists() == False:
         return False

    elif User_Info.objects.filter(uid=uid).exists() == True:
        user_info = User_Info.objects.filter(uid=uid)
        for user in user_info:
            height = user.height  # 讀取先前紀錄過之身高
            weight = user.weight  # 讀取先前紀錄過之體重
            age = user.age  # 讀取先前紀錄過之年齡
            sex = user.sex  # 讀取先前紀錄過的性別
            BMR = user.bmr
            water = user.water

        return height, weight, age, sex, BMR, water