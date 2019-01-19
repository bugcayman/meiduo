from django.shortcuts import render
from random import randint
from rest_framework.views import APIView,Response
# Create your views here.

from django_redis import get_redis_connection
from meiduo_mall.libs.yuntongxun.sms import CCP

class SMSCodeView(APIView):
    def get(self,request,mobile):
        # 1.生成短信验证码
        sms_code = '%06d'%randint(0,999999)
        #2.创建redis连接对象
        redis_conn = get_redis_connection("verify_codes")
        #3.将短信验证码储存
        #redis_conn.setex(key,过期时间,value)
        redis_conn.setex('sms_%s'%mobile,300,sms_code)
        #4.利用容联运发短信
        CCP().send_template_sms(mobile,[sms_code,5],1)
        #响应对象
        return Response({"massage":"OK"})