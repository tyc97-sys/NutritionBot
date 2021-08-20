from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class User_Info(models.Model):
    uid = models.CharField(max_length=50, null=False, default='')  # user_id
    name = models.CharField(max_length=255, blank=True, null=False)  # LINE名字
    mtext = models.JSONField(max_length=255, blank=True, null=True)  # 文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)  # 物件儲存的日期時間
    height = models.FloatField(max_length=255, default = 0.0,  blank=True, null=False)
    weight = models.FloatField(max_length=255, default = 0.0, blank=True, null=False)
    age = models.IntegerField(default = 0, blank=False, null=False)
    sex = models.IntegerField(default = 0, blank=False, null=False) # male: 0, female: 1

    def __str__(self):
        return self.uid