# Sample Code 

## Rest Api Server에 연동된 db에서 데이터를 읽어오는 클래스(Singleton)
> ![image](https://user-images.githubusercontent.com/46432795/115825360-43f82780-a444-11eb-9873-c21276404062.png)

## PLC(기기 제어용 산업용 컨트롤러)와의 통신을 위한 클래스
 * PLC 접속 method
> ![image](https://user-images.githubusercontent.com/46432795/115826147-68083880-a445-11eb-8199-b0e2b84e3813.png)
 
 * PLC의 데이터 읽어오는 method
> ![image](https://user-images.githubusercontent.com/46432795/115826463-ed8be880-a445-11eb-863d-c745bc5cd058.png) 

 * PLC의 데이터가 저장된 Register 번지를 저장해놓은 Enum

> ![image](https://user-images.githubusercontent.com/46432795/115826611-25932b80-a446-11eb-9eaf-41d0f81b308b.png)


## 프로그램 구동 화면 일부

> ![image](https://user-images.githubusercontent.com/46432795/115830019-aa804400-a44a-11eb-86db-45a6a552465b.png)

 * 데이터 표시 라벨 업데이트 method
 * PLC에서 데이터 수신 후 가공하는 부분
 > ![image](https://user-images.githubusercontent.com/46432795/115832078-68a4cd00-a44d-11eb-91e8-ddb128fb8c09.png) 

 * 라벨 업데이트 부분

 > ![image](https://user-images.githubusercontent.com/46432795/115832372-ccc79100-a44d-11eb-9d7e-f0892a5d9eb8.png)