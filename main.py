from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from schemas.review import Review, CreateReview
from schemas import list_serial_from_db
from bson import ObjectId
from database import reviews_collection
from pymongo import ReturnDocument


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/reviews")
async def get_reviews():
    reviews = await list_serial_from_db(reviews_collection.find())
    return [Review(**review).model_dump(by_alias=True) for review in reviews]


@app.get("/api/review/{review_id}")
async def get_review(review_id):
    review = await reviews_collection.find_one({'_id': ObjectId(review_id)})
    review['id'] = str(review.pop('_id'))
    return Review(**review).model_dump(by_alias=True)


@app.post("/api/review")
async def add_review(review: CreateReview):
    try:
        result = await reviews_collection.insert_one(review.model_dump(by_alias=True))
        return Review(
            **{**review.model_dump(), "id": str(result.inserted_id)}).model_dump(by_alias=True)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data")


@app.put("/api/review")
async def update_review(review: Review):
    try:
        to_update_review = review.model_dump(by_alias=True)
        to_update_review_id = to_update_review.pop('id')
        result = await (reviews_collection.find_one_and_update(
            {"_id": ObjectId(to_update_review_id)},
            {"$set": to_update_review},
            return_document=ReturnDocument.AFTER))

        result['id'] = str(result.pop('_id'))
        return Review(**result).model_dump(by_alias=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/api/reviews")
async def delete_reviews():
    result = await reviews_collection.delete_many({})
    return {"deleted_count": result.deleted_count}


@app.post("/api/reviews")
async def add_reviews():
    await reviews_collection.insert_many([
        {
            "titleEng": "Inception",
            "titleRus": "Начало",
            "isViewed": True,
            "review": "Отличный фильм с захватывающим сюжетом и потрясающими визуальными эффектами.",
            "rating": 9,
            "releaseDate": "2010-07-16T00:00:00.000Z",
            "reviewDate": "2024-07-18T10:00:00.000Z"
        },
        {
            "titleEng": "The Matrix",
            "titleRus": "Матрица",
            "isViewed": True,
            "review": "Культовый фильм, который изменил представление о научной фантастике.",
            "rating": 10,
            "releaseDate": "1999-03-31T00:00:00.000Z",
            "reviewDate": "2024-07-17T10:00:00.000Z"
        },
        {
            "titleEng": "Interstellar",
            "titleRus": "Интерстеллар",
            "isViewed": True,
            "review": "Великолепная картина о космических путешествиях и семейных ценностях.",
            "rating": 9,
            "releaseDate": "2014-11-07T00:00:00.000Z",
            "reviewDate": "2024-07-16T10:00:00.000Z"
        },
        {
            "titleEng": "The Dark Knight",
            "titleRus": "Темный рыцарь",
            "isViewed": True,
            "review": "Один из лучших фильмов о супергероях с впечатляющим исполнением роли Джокера.",
            "rating": 10,
            "releaseDate": "2008-07-18T00:00:00.000Z",
            "reviewDate": "2024-07-15T10:00:00.000Z"
        },
        {
            "titleEng": "Forrest Gump",
            "titleRus": "Форрест Гамп",
            "isViewed": True,
            "review": "Трогательная история о жизни простого человека с удивительной судьбой.",
            "rating": 9,
            "releaseDate": "1994-07-06T00:00:00.000Z",
            "reviewDate": "2024-07-14T10:00:00.000Z"
        },
        {
            "titleEng": "Fight Club",
            "titleRus": "Бойцовский клуб",
            "isViewed": True,
            "review": "Фильм с неожиданным сюжетом и глубокими философскими подтекстами.",
            "rating": 9,
            "releaseDate": "1999-10-15T00:00:00.000Z",
            "reviewDate": "2024-07-13T10:00:00.000Z"
        },
        {
            "titleEng": "The Shawshank Redemption",
            "titleRus": "Побег из Шоушенка",
            "isViewed": True,
            "review": "Мощная драма о надежде и дружбе, которая трогает до глубины души.",
            "rating": 10,
            "releaseDate": "1994-09-23T00:00:00.000Z",
            "reviewDate": "2024-07-12T10:00:00.000Z"
        },
        {
            "titleEng": "Pulp Fiction",
            "titleRus": "Криминальное чтиво",
            "isViewed": True,
            "review": "Культовый фильм с уникальным стилем и запоминающимися персонажами.",
            "rating": 9,
            "releaseDate": "1994-10-14T00:00:00.000Z",
            "reviewDate": "2024-07-11T10:00:00.000Z"
        },
        {
            "titleEng": "The Godfather",
            "titleRus": "Крестный отец",
            "isViewed": True,
            "review": "Эпическая сага о мафиозной семье с великолепной актерской игрой.",
            "rating": 10,
            "releaseDate": "1972-03-24T00:00:00.000Z",
            "reviewDate": "2024-07-10T10:00:00.000Z"
        },
        {
            "titleEng": "Schindler's List",
            "titleRus": "Список Шиндлера",
            "isViewed": True,
            "review": "Мощная историческая драма о спасении евреев во время Холокоста.",
            "rating": 10,
            "releaseDate": "1993-12-15T00:00:00.000Z",
            "reviewDate": "2024-07-09T10:00:00.000Z"
        }
    ]

    )
