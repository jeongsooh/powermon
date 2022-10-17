# Dashboard for 3-Ph power sensor
## Shared interface
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




