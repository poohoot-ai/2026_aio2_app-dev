from fastapi import FastAPI, status, HTTPException
from schemas import WeatherResponse, BookCreate, BookResponse, GoogleBooks
from external_api import fetch_weather, fetch_books
from fastapi.staticfiles import StaticFiles

tags_metadata = [
    {"name": "도서", "description": "도서 등록, 조회, 검색"},
    {"name": "외부 연동", "description": "Google Books와 날씨 API 연동"},
    {"name": "시스템", "description": "서버 상태 확인"},
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="도서 관리 API",
    description="도서를 등록·조회하고 외부 검색으로 정보를 가져오는 API",
    version="1.0.0",
    contact={"name": "홍길동", "email": "hong@example.com"},
)
app.mount("/static", StaticFiles(directory="static"), name="static")

books = [
    {"id": 1, "title": "파이썬 입문", "author": "김철수", "year": 2021},
    {"id": 2, "title": "FastAPI 실전", "author": "이영희", "year": 2023},
    {"id": 3, "title": "파이썬 웹개발", "author": "김철수", "year": 2022},
    {"id": 4, "title": "데이터 분석 기초", "author": "박민수", "year": 2020},
    {"id": 5, "title": "FastAPI로 배우는 백엔드", "author": "이영희", "year": 2024}
]

@app.get("/")
def read_root():
    return {"status" : "hello"}

@app.get("/health")
def health():
    return {"status" : "healthy"}

@app.get("/info")
def info():
    return {"name": "도서 관리 API", "version": "0.1.0"}

# 도서의 목록을 제공하는 엔드포인트
@app.get("/books", tags=["도서"], response_model=list[BookResponse])
def list_books():
    return books

@app.get("/books/search")
def search_books(keyword: str = ""):
    if not keyword:
        return books
    return [b for b in books if keyword in b["title"]]

@app.get("/books/filter")
def filter_books(keyword: str = "", sort: str = ""):
    result = books

    # for book in books:
    if keyword:
        # 리스트 컴프리헨션 - for + if > 리스트
        result = [b for b in result if b["author"] == keyword]

        if sort == "year":
            result = sorted(result, key=lambda b: b["year"])

    return result

@app.get("/books/page")
def page_books(skip: int = 0, limit: int = 2):
    return books[skip: skip + limit]

@app.post(
        "/books", 
        tags=["도서"],
        summary="도서 등록",
        response_description="등록된 도서 정보",        
        response_model=BookResponse, 
        status_code=status.HTTP_201_CREATED
    )
def create_book(book: BookCreate):
    """
    새 도서를 등록합니다.

    - **title**: 1자 이상 100자 이하
    - **year**: 1900 이상 2100 이하
    - 같은 제목이 이미 있으면 409를 반환합니다.
    """
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(status_code=409, detail="기존에 등록된 도서입니다")

    new_id = max([b["id"] for b in books], default=0) + 1
    new_book = {"id": new_id, **book.model_dump()}
    books.append(new_book)
    return new_book

# 테스트 시나리오
# 1. 새로운 책 등록
# 2. 책 목록을 조회
# 3. 등록한 책을 검색

# @app.get("/weather/raw")
# async def weather_raw():
#     async with httpx.AsyncClient(timeout=5.0) as client:
#         response = await client.get(
#             "https://api.open-meteo.com/v1/forecast",
#             params={
#             "latitude": 36.8,
#             "longitude": 127.1,
#             "current": "temperature_2m",
#             },
#         )
#     return response.json()

@app.get("/weather", response_model=WeatherResponse)
async def weather(latitude: float = 36.8, longitude: float = 127.1):
    return await fetch_weather(latitude, longitude)

#엔드포인트
@app.get("/books/external", response_model=list[GoogleBooks])
async def search_external_books(keyword: str, limit: int=5):
    return await fetch_books(keyword, limit)

@app.get(
        "/books/{book_id}", 
        responses={
            404: {"description": "해당 번호의 도서가 없음"},
        },
        response_model=BookResponse
    )
def read_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")