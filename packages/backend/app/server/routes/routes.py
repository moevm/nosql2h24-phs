from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException, UploadFile, File
from fastapi import Query
from typing import Optional, List
from fastapi.responses import FileResponse
from bson import json_util
import json
from fastapi import APIRouter
import motor.motor_asyncio
from pydantic import BaseModel, EmailStr
import os

MONGO_DETAILS = "mongodb://db:27017"
# MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client.phs
users_collection = db["users"]
psychologists_collection = db["psychologists"]

TEMP_DIR = "./temp"
DUMP_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dump.json")
os.makedirs(TEMP_DIR, exist_ok=True)

router = APIRouter()


class RegisterUserRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    name: str
    surname: str
    email: EmailStr
    registered_at: datetime


class PsychologistResponse(BaseModel):
    id: str
    name: str
    surname: str
    email: EmailStr
    price: Optional[float]
    address: Optional[str]
    meeting_format: Optional[str]
    language: Optional[str]


async def load_dump_if_empty():
    collection_names = []
    if not collection_names:
        if os.path.exists(DUMP_FILE_PATH):
            with open(DUMP_FILE_PATH, "r", encoding="utf-8") as f:
                data = json_util.loads(f.read())
            for collection_name, documents in data.items():
                collection = db[collection_name]
                await collection.insert_many(documents)
            print("Database initialized with dump.json data.")
        else:
            print(f"Dump file {DUMP_FILE_PATH} not found. Skipping initialization.")
    else:
        print("Database already contains data. Skipping dump.json loading.")


@router.post("/register", response_model=UserResponse)
async def register_user(user: RegisterUserRequest):
    existing_user = await users_collection.find_one({"mail": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = {
        "mail": user.email,
        "password": user.password,
        "name": user.firstName,
        "surname": user.lastName,
        "sex": None,
        "birth_date": None,
        "phone_number": None,
        "meetings": [],
        "reviews": [],
        "transactions": [],
        "registered_at": datetime.utcnow(),
    }
    result = await users_collection.insert_one(new_user)
    created_user = await users_collection.find_one({"_id": result.inserted_id})

    return UserResponse(
        name=created_user["name"],
        surname=created_user["surname"],
        email=created_user["mail"],
        registered_at=created_user["registered_at"],
    )


@router.post("/login")
async def login_user(credentials: LoginRequest):
    user = await users_collection.find_one({"mail": credentials.email})
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "user_id": str(user["_id"])}


@router.get("/psychologists", response_model=List[PsychologistResponse])
async def search_psychologists(
        search: Optional[str] = Query(None),
        email: Optional[str] = Query(None),
        price_min: Optional[float] = Query(None),
        price_max: Optional[float] = Query(None),
        address: Optional[str] = Query(None),
        meeting_format: Optional[str] = Query(None),
        language: Optional[str] = Query(None),
):
    query = {}

    if search:
        query["$or"] = [
            {"user.name": {"$regex": search, "$options": "i"}},
            {"user.surname": {"$regex": search, "$options": "i"}},
        ]

    if email:
        query["user.mail"] = {"$regex": email, "$options": "i"}

    if price_min is not None or price_max is not None:
        query["price"] = {}
        if price_min is not None:
            query["price"]["$gte"] = price_min
        if price_max is not None:
            query["price"]["$lte"] = price_max
        if not query["price"]:
            del query["price"]

    if address:
        query["address"] = {"$regex": address, "$options": "i"}

    if meeting_format:
        query["meeting_format"] = {"$regex": meeting_format, "$options": "i"}

    if language:
        query["language"] = {"$regex": language, "$options": "i"}

    psychologists = await psychologists_collection.find(query).to_list(length=50)

    return [
        PsychologistResponse(
            id=str(psychologist["_id"]),
            name=psychologist["user"]["name"],
            surname=psychologist["user"]["surname"],
            email=psychologist["user"]["mail"],
            price=psychologist.get("price"),
            address=psychologist.get("address"),
            meeting_format=psychologist.get("meeting_format"),
            language=psychologist.get("language"),
        )
        for psychologist in psychologists
    ]


@router.get("/psychologists/{psychologist_id}", response_model=PsychologistResponse)
async def get_psychologist(psychologist_id: str):
    try:
        if not ObjectId.is_valid(psychologist_id):
            raise HTTPException(status_code=400, detail="Invalid psychologist ID")

        psychologist = await psychologists_collection.find_one({"_id": ObjectId(psychologist_id)})
        if not psychologist:
            raise HTTPException(status_code=404, detail="Psychologist not found")

        return PsychologistResponse(
            id=str(psychologist["_id"]),
            name=psychologist["user"]["name"],
            surname=psychologist["user"]["surname"],
            email=psychologist["user"]["mail"],
            price=psychologist.get("price"),
            address=psychologist.get("address"),
            meeting_format=psychologist.get("meeting_format"),
            language=psychologist.get("language"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export", response_class=FileResponse)
async def export_data():
    try:
        data = {}
        collections = await db.list_collection_names()
        for collection_name in collections:
            collection = db[collection_name]
            documents = await collection.find().to_list()
            data[collection_name] = json.loads(json_util.dumps(documents))

        file_path = os.path.join(TEMP_DIR, "exported_data.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return FileResponse(file_path, filename="exported_data.json", media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import")
async def import_data(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/json":
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JSON file.")

        content = await file.read()
        data = json_util.loads(content)
        collection_names = await db.list_collection_names()

        for collection_name, documents in data.items():
            if collection_name not in collection_names:
                db.create_collection(collection_name)
            collection = db[collection_name]
            await collection.delete_many({})
            await collection.insert_many(documents)

        return {"message": "Data imported successfully"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
