# Dashboard for 3-Ph power sensor
## Basic API
### Introduction
* 자료구조는 JSON 형식을 따름
* Host, url, token 등의 정보는 서버에서 정의하여 내려준 naming 사용
* Boot 시 서버로부터 time 동기화하고, 1일 또는 1주일에 한번 시간동기화
* 센서에서 데이터를 재 전송할 때 기준은 timestamp로 하며 서버에서는 timestamp를 기준으로 데이터 관리
* 데이터 전송은 1초에 1회
### Definition
#### POST https://{host}/powermon/data

Request Body
````
{
	“version” : <string>,
	“sensor_id” : <string>,
	“token” : <string>,
	“timestamp” : <int>,
	“data” : [
		{
			“probe_id” : <int>,   	# default 1
			“probe_type” : <string>,  	# “CT” 또는 “rogow_coil”
			“power” : [<int>, <int>, ..],	# 초 당 20회 계측
			“pf” : [<int>, <int>, ..],		# 초 당 20회 계측
			“voltage” : <int>, 		# 초 당 20회 계측의 RMS 값 또는
			“voltage” : [<int>, <int>, ..]	# power나 pf와 동일한 형식
    },
		{
			“probe_id” : <int>,   	# default 2
			“probe_type” : <string>,  	# “CT” 또는 “rogow_coil”
			“power” : [<int>, <int>, ..],	# 초 당 20회 계측
			“pf” : [<int>, <int>, ..],		# 초 당 20회 계측
			“voltage” : <int>, 		# 초 당 20회 계측의 RMS 값 또는
			“voltage” : [<int>, <int>, ..]	# power나 pf와 동일한 형식
    },
		{
			“probe_id” : <int>,   	# default 3
			“probe_type” : <string>,  	# “CT” 또는 “rogow_coil”
			“power” : [<int>, <int>, ..],	# 초 당 20회 계측
			“pf” : [<int>, <int>, ..],		# 초 당 20회 계측
			“voltage” : <int>, 		# 초 당 20회 계측의 RMS 값 또는
			“voltage” : [<int>, <int>, ..]	# power나 pf와 동일한 형식
    }
	]
}
````
### Properties
* Version
  * 연월일
  * Ex: 221013
* Sensor_id
  * 영문(회사명, 장소명 등) + 6자리 숫자
  * Ex: gresystem000001
* Token
  * 보안용인데.. boot 시 서버로부터 token을 받아서 이를 사용하는 것으로 생각 중.. 좋은 아이디어 구하는 중..
  * TBD
* Timestamp
  * UTC기준
* Probe_id
  * 3개의 계측용 CT 또는 rogowski coil이 있으므로 각각을 1, 2, 3 또는 ABC로 구분
* Probe_type
  * 3개의 계측용 probe가 서로 다를 경우는 흔하지 않으나, 각각의 protype 표시
  * Ex: CT” or “rogow_coil”
* Power, pf, voltage
  * 각각 전력, 역률, 전압의  주어진 시간 동안의 RMS 값
  * 예를 들어 1초에 한번 계측한다면 1초간의 RMS값, 1초에 20번 계측한다면 50ms 동안의 RMS 값.

### Git Log
commit a79da43b6ecf994ee8361745576fb2ce9ff1ba3c (HEAD -> master, origin/master)
Author: jeongsooh <jeongsooh@hotmail.com>
Date:   Mon Oct 17 14:00:31 2022 +0900

    readme 추가

## Environment 
```
$ pip install djangorestframework
```
#### powermon/settings.py
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'base',
]
```
#### powermon/urls.py
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
```
#### base/models.py
```
class Item(models.Model):
  version = models.CharField(max_length=64)
  sensor_id = models.CharField(max_length=64)
  token = models.CharField(max_length=256)
  timestamp = models.DateTimeField(auto_now_add=False)
  data = models.JSONField(default='{}')
  created = models.DateTimeField(auto_now_add=True)
```
#### base/admin.py
```
from django.contrib import admin
from .models import Item

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
  list_display = ('version', 'sensor_id','token', 'timestamp', 'data', 'created',)

admin.site.register(Item, ItemAdmin)
```
#### api/serializers.py
```
from rest_framework import serializers
from base.models import Item

class ItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = '__all__'
```
#### api/urls.py
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('powermon/data/', views.addItem)
]
```
#### api/views.py
```
import json
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from .serializers import ItemSerializer

# Create your views here.

@api_view(['GET'])
def getData(request):
  items = Item.objects.all()
  serializer = ItemSerializer(items, many=True)
  return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
  print('data: %s' % request.data)
  serializer = ItemSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
  return Response(serializer.data) 
```
#### 테스트 구동
```
$ python manage.py runserver 5000
Watching for file changes with StatReloader
Performing system checks...

System check identified some issues:

System check identified 1 issue (0 silenced).
October 17, 2022 - 14:32:32
Django version 4.1.2, using settings 'powermon.settings'
Starting development server at http://127.0.0.1:5000/
Quit the server with CTRL-BREAK.
```
## 구현 내용 소개
#### MySQL integration
먼저 mysqlclient를 설치하고
```
$ pip install mysqlclient
Collecting mysqlclient
  Using cached mysqlclient-2.1.1-cp310-cp310-win_amd64.whl (178 kB)
Installing collected packages: mysqlclient
Successfully installed mysqlclient-2.1.1
(venv) 
```
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'powermon',
        'USER': 'jeongsooh',
        'PASSWORD': 'tkatjdfh4rlf#17',
        'Host': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_commend': 'set sql_mode="STRICT_TRANS_TABLES"',
            'charset': 'utf8mb4',
            'use_unicode': True,
        }
    }
}
```

#### user, sensor app 추가
user/models.py, user/admin.py, user/forms.py, user/views.py 작성
powermon/settings.py update
```
INSTALLED_APPS += [
    'base',
    'user',
    'sensor',
]
```
powermon/urls.py 수정
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('powermon/', include('api.urls')),
    path('', include('user.urls'))
]
```
user/urls.py 작성
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
]
```
user/templates/base.html, index.html 작성
bootstrap static file 사용을 위해서 powermon/settings.py 수정
```
# STATIC_URL = 'static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

#### python manage.py runserver 했을 때 channels가 동작하지 않는 이유로 channels upgrade
* django와 channels version mismatch로 에러 발생
* channels 공식 문서 참조: https://channels.readthedocs.io/en/stable/ 
