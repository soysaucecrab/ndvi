import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
from time import sleep  #time 라이브러리의 sleep함수 사용

servoPin          = 12   # 서보 핀
SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기

GPIO.setmode(GPIO.BOARD)        # GPIO 설정
GPIO.setup(servoPin, GPIO.OUT)  # 서보핀 출력으로 설정

servo = GPIO.PWM(servoPin, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.
[출처] 라즈베리파이(RaspberryPi) 서보모터(MG90, SG90, MG995) 사용하기 - 파이썬(Python) + PWM|작성자 천동이

