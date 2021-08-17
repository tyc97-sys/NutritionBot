# NutritionBot

進入 [Line Developers](https://developers.line.biz/zh-hant/) 登入自己的帳號，填入該填入的資料。

## Messaging API channel

之後選擇建立 Messaging API channel （基本資料的填寫 Line 並無限制）

![image](https://user-images.githubusercontent.com/85750836/129725874-850305b7-4e16-4781-8610-81fb8af0fc8b.png)

有兩個憑證是等一下會用到的。

1. Basic settings > Channel secret 
2. Messaging API > Channel access token (long-lived) （需要點 issue）

## LINE Bot 憑證

先建置環境，安裝會使用到的Python套件

```
$ pip install django
$ pip install line-bot-sdk
$ pip install beautifulsoup4
$ pip install requests
```

接著，建立Django專案、應用程式及資料庫遷移(Migration)

```
$ django-admin startproject mylinebot .  #建立Django專案
 
$ python manage.py startapp NutritionBot  #建立Django應用程式 程式名稱 NutritionBot
 
$ python manage.py migrate  #執行資料遷移(Migration)
```

![image](https://user-images.githubusercontent.com/85750836/129728360-9bd0637a-1d6f-4469-b00b-7f9f247281ae.png)
+ 此時 `mylinebot` 是**專案主程式**
+ `NutritionBot` 是**應用程式**

之後在 mylinebot/settings.py 裡增加上述所提到的兩個憑證

```python
LINE_CHANNEL_ACCESS_TOKEN = 'Messaging API > Channel access token'
 
LINE_CHANNEL_SECRET = 'Basic settings > Channel secret'
```

並且在同樣的檔案裡的 `INSTALLED_APPS` 的地方加上剛剛所建立的 Django 應用程式，範例如下：
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'NutritionBot.apps.NutritionbotConfig',
]
```
也就是在 NutritionBot/apps.py 裡的 `class NutritionbotConfig`

## 開發 Line Bot 應用程式

以上都設定完成後，開啟 NutritionBot/views.py，這邊就是轉寫 Line Bot 接收訊息後要執行的運算邏輯。

先建立最基本的 echo ChatBot 當作示範（回傳傳送過去的訊息）
```python
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

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

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
```

`def callback` 中，當偵測到使用者有傳入的事件，就會透過Python迴圈進行讀取。

接下來就要設定這個LINE Bot應用程式(APP)的連結網址，所以在新建立一個 NutritionBot/urls.py檔案，加入以下的網址設定：
```python
from django.urls import path
from . import views
 
urlpatterns = [
    path('callback', views.callback)
]
```

而為了要將這個 APP 的網址也加入到專案主程式中，所以在 mylinebot/urls.py 檔案中，加入以下的網址設定：
```python
from django.contrib import admin
from django.urls import path, include
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('NutritionBot/', include('NutritionBot.urls')) #包含應用程式的網址
]
```
