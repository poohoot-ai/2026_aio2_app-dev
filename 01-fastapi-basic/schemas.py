from pydantic import BaseModel, Field, field_validator

class Publisher(BaseModel):
    name: str
    city: str = "고양"

class BookCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        description="도서 제목",
        examples=["처음 시작하는 FastAPI"],
    )
    author: str = Field(
        min_length=1,
        max_length=50,
        description="저자명",
        examples=["빌 루바노빅"],
    )
    year: int = Field(
        ge=1900,
        le=2100,
        description="출판 연도",
        examples=[2024],
    )
    tags: list[str] = Field(default_factory=list, description="분류 태그")
    publisher: Publisher | None = Field(default=None, description="출판사 정보")

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("제목은 공백일 수 없습니다")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "처음 시작하는 FastAPI",
                    "author": "빌 루바노빅",
                    "year": 2024,
                    "tags": ["python", "backend"],
                    "publisher": {"name": "한빛미디어", "city": "서울"},
                }
            ]
        }
    }

class BookResponse(BookCreate):
    id: int

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature: float
    time: str

class GoogleBooks(BaseModel):
    title: str
    authors: list[str] = Field(default_factory=list)
    published_date: str = ""

class ErrorDetail(BaseModel):
    detail: str = Field(description="오류 메시지", examples=["도서를 찾을 수 없습니다"])