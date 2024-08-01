# new_backend


## 업데이트 이력
- [2024-07-23 나현진] 유저 CRUD & 로그인, 명언 CRUD, postgreSQL 연결 및 초기화
- [2024-07-28 정혜나] Quote CRUD, 좋아요, 댓글 기능 구현, account ProfileView 추가
- [2024-07-29 남기동] account 필드 제거, superuser 수정, Quote output field 조정
- [2024-07-29 정혜나] 사용자가 명언 Post 기능 구현, ProfileView 수정
- [2024-07-30 남기동] Chroma 연결, Quote CRUD와 연동, CommentAdminView 생성, 명언 추천 기능 구현, 명언 좋아요 내림차순 조회 구현
- [2024-07-31 남기동] 서버 설정 관련 명령어(server.md) 업로드, settings.py의 ALLOW_HOST=['*']로 변경(외부 접속 허용을 위해)
- [2024-07-31 정혜나] 팔로잉 기능 구현

<br>

## 서버 이용 방법
- pem키 사용 없이 ID, Password로 접속 가능하게 변경해두었습니다
- Putty에서 Host Name에 15.164.27.255, Port 22로 설정하고 Open
- ID : ec2-user
- PASSWORD : shinsudong
- (확인용) 'http://15.164.27.255/quote/', 'http://15.164.27.255/accounts/register/' 로 체크 가능
- (Admin 'http://15.164.27.255/admin/' ) Email : admin@google.com, Password : admin 


<br>

## 설치방법

```bash
$ git clone https://github.com/mukzzanglion-team2/new_backend.git
$ cd new_backend
$ python -m venv venv
$ source ./venv/Scripts/activate
$ pip install -r requirements.txt

# 필요에 따라 PostgreSQL Docker Container 생성 및 실행
$ docker run -p 5432:5432 --name test-postgres -e POSTGRES_PASSWORD=1234 -e TZ=Asia/Seoul -d postgres:latest
# docker exec -it {container_id} bash --> psql -U postgres --> create database quote_db; --> exit --> exit

# accounts, quote의 models.py에 ForeignKey, ManyToManyField 주석처리하고
$ python manage.py makemigrations account
$ python manage.py makemigrations quote
$ python manage.py migrate

# accoutns, quote의 models.py에 주석처리한 부분 해제하고
$ python manage.py makemigrations account
$ python manage.py makemigrations quote
$ python manage.py migrate

$ python manage.py createsuperuser
# email, nickname, password 입력하면 유저 생성

$ python manage.py runserver
```


## .env 파일
```
SECRET_KEY = 'django-insecure-p8+g6!$v=)5e3_bfwn&la9f8y95ccx=awv&3$-t1oe(nkgcbsf'
KAKAO_REST_API_KEY='217fcb126e662a8cbaa60bff80aa32df'
DB_NAME= 'quote_db'
DB_USER='postgres'
DB_PASSWORD='1234'
DB_HOST='localhost'
DB_PORT='5432'
UPSTAGE_API_KEY = "up_ZkSUCtOpUsc5oeVuCVe8zcnVKTEPj"
CHROMA_HOST = "20.249.183.16"
CHROMA_PORT = "8001"
```


## Directory Tree
```
project/
├── config/
│   ├── apps.py         
│   ├── settings.py
│   ├── ...
│   └── urls.py         
├── account/            # User, Login 관련
│   ├── crud.py         
│   ├── serializers.py
│   ├── urls.py         # URL Mapping
│   ├── ...
│   └── views.py        # 웹 요청 처리
├── quote/              # 명언 관련
│   ├── crud.py         
│   ├── serializers.py
│   ├── urls.py         # URL Mapping
│   ├── ...
│   └── views.py        # 웹 요청 처리
├── manage.py          
├── requirements.txt    
├── .env                # 환경 변수 파일
├── .gitignore        
└── venv/               # 가상 환경
```


## Model Schema
```javascript
User {
	id : PK(auto_increment)
	
	# Not NULL
	email : email
	password : str(~30)
	nickname : str(~50)
	
	# NULL
	liked_quotes : List[quote_id] = []
	is_active : True
	is_staff : False(superuser만 True)
}

Quote {
	id : PK(auto_increment)
	
	# Not NULL
	content: str(~100)
	description : str(~500)   
	author : str(~100)        # 해당 명언의 발화자(원저작자)
	
	# NULL
	image : ImageField
	created_at : Datetime
	like_count: PositiveInteger	
}

Comment {
	id : PK(auto_increment)

	# Not NULL
	content : TextField
	quote : Quote.id
	user : User.nickname

	# NULL
	created_at : Datetime
}
```


## 참고할 노션 페이지
<https://www.notion.so/rmdnps10/Back-End-60d517d1690b44bc9d4c0ded0b839ec9>
