from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel as pydantic_to_camel


def to_camel(string: str) -> str:
    return pydantic_to_camel(string)


class Review(BaseModel):
    id: str

    title_eng: str = Field(..., alias='titleEng')
    title_rus: str = Field(..., alias='titleRus')
    is_viewed: bool = Field(..., alias='isViewed')
    review: str
    rating: int

    release_date: str = Field(..., alias='releaseDate')
    review_date: str = Field(..., alias='reviewDate')

    class Config:
        alias_generator = to_camel
        populate_by_name = True

        json_schema_extra = {
            "examples": [
                {"id": "669f6a213d9a636c5eee5529",
                 "titleEng": "Inception",
                 "titleRus": "Начало",
                 "isViewed": True,
                 "review": "Отличный фильм с захватывающим сюжетом и потрясающими визуальными эффектами.",
                 "rating": 9,
                 "releaseDate": "2024-07-21T19:30:09.066Z",
                 "reviewDate": "2024-07-18T10:00:00.000Z"
                 }
            ]
        }


class CreateReview(BaseModel):
    title_eng: str = Field(..., alias='titleEng')
    title_rus: str = Field(..., alias='titleRus')
    is_viewed: bool = Field(..., alias='isViewed')
    review: str
    rating: int

    release_date: str = Field(..., alias='releaseDate')
    review_date: str = Field(..., alias='reviewDate')

    class Config:
        alias_generator = to_camel
        populate_by_name = True
