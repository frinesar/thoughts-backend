import os
import motor.motor_asyncio
from dotenv import load_dotenv


load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv('PASSWORD')


uri = f'''mongodb+srv://{LOGIN}:{
    PASSWORD}@cluster0.waeicad.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'''

client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.ReviewData
reviews_collection = db.Reviews
