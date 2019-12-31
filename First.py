# # 홍길동 씨의 과목별 점수는 다음과 같다. 홍길동 씨의 평균 점수를 구해 보자.

# # 과목	점수
# # 국어	80
# # 영어	75
# # 수학	55

# # 주석 단축키 ctrl + / 

# korean = 80
# english = 75
# math = 55

# average = (korean + english + math) / 3

# print(average)  

# # Q2
# # 자연수 13이 홀수인지 짝수인지 판별할 수 있는 방법에 대해 말해 보자.

# number = 13
# divide = number %2

# if divide:
#     print("홀수")
# else:
#     print("짝수")



# # 홍길동 씨의 주민등록번호는 881120-1068234이다. 홍길동 씨의 주민등록번호를 연월일(YYYYMMDD) 부분과 그 뒤의 숫자 부분으로 나누어 출력해 보자.

# # ※ 문자열 슬라이싱 기법을 사용해 보자.

# privateNumber = "881120-1068234"

# YYMMDD = privateNumber[0:6]

# otherNum = privateNumber[7:]

# print(YYMMDD)

# print(otherNum)


# # 다음과 같은 문자열 a:b:c:d가 있다. 문자열의 replace 함수를 사용하여 a#b#c#d로 바꿔서 출력해 보자.

# # >>> a = "a:b:c:d"

# replaceText = "A:B:C:D"

# replaceText = replaceText.replace("A","B",-1)

# print(replaceText)

# # [1, 3, 5, 4, 2] 리스트를 [5, 4, 3, 2, 1]로 만들어 보자.

# # ※ 리스트의 내장 함수를 사용해 보자.

# List = [1, 3, 5, 4, 2]

# List.sort()
# List.reverse()
# print(List)

# # ['Life', 'is', 'too', 'short'] 리스트를 Life is too short 문자열로 만들어 출력해 보자.

# # ※ 문자열의 join 함수를 사용하면 리스트를 문자열로 쉽게 만들 수 있다.

# textList = ['Life', 'is', 'too', 'short']

# textList = " ".join(textList)

# print(textList)



# # (1,2,3) 튜플에 값 4를 추가하여 (1,2,3,4)를 만들어 출력해 보자.

# # ※ 더하기(+)를 사용해 보자.


# Tuple1 = (1,2,3)

# Tuple2 = (4)

# Tuple1 = Tuple1 + Tuple2

# print(Tuple1)

import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(('192.168.0.40',502))

i = 0 
while i < 10:
    sock.send("ENQ01RSS0106%PW000EOT".encode())