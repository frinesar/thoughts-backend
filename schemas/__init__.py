def individual_serial_from_db(review) -> dict:
    return {
        "id": str(review["_id"]),
        "title_eng": review["titleEng"],
        "title_rus": review["titleRus"],
        "is_viewed": review["isViewed"],
        "review": review["review"],
        "rating": review["rating"],
        "release_date": review["releaseDate"],
        "review_date": review["reviewDate"]
    }


async def list_serial_from_db(reviews) -> list[dict]:
    return [individual_serial_from_db(review) async for review in reviews]
