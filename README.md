# SRMS(Smart Remote Management System)

## 내용

 * 회사의 정부과제로 진행한 프로젝트
 * 회사 기기(산업용 대형 전기 탈수기)의 전반적인 데이터를 모니터링
 * 기기의 소모품 사용시간을 체크, 사용시간이 넘어가면 이메일 발송
 * 기기의 알람이 발생하면 확인 가능

## 사용 기술 및 환경

* FrontEnd - Python(QT, Modbus)
* BackEnd - Django, MariaDB, Modbus


## 프로그램 구동 사진 

#### 기본 모니터링 화면 
> ![TC공용_원격모니터링 프로그램 실행](https://user-images.githubusercontent.com/46432795/99750169-3fd97e00-2b23-11eb-8b34-eac280f26799.JPG)
> * 각 지역별 기기 기본 상황을 모니터링
> * 각 기기명 클릭 시 세부 모니터링 화면을 호출

#### 세부 모니터링 화면 
> ![TC공용_부산_A버튼클릭](https://user-images.githubusercontent.com/46432795/99750460-c8f0b500-2b23-11eb-9417-8b296739305e.JPG)
> * 기기의 전반적인 데이터를 모니터링
> * Tab으로 구성

#### 가동시간 Tab 
> ![가동시간-추가부품](https://user-images.githubusercontent.com/46432795/99750624-0d7c5080-2b24-11eb-9587-1d4f24e4b693.JPG)
> * 기기의 소모품 사용시간을 모니터링
> * 기본 소모품 이외의 다른 소모품 추가 가능
> * 소모품이 준비, 교체시간 이상 사용되면 설정된 이메일로 알람 발송







