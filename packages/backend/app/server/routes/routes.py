from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from fastapi import Query
from typing import Optional, List

from fastapi import APIRouter
import motor.motor_asyncio
from pydantic import BaseModel, EmailStr

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client.phs
users_collection = db["users"]
psychologists_collection = db["psychologists"]

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
        price: Optional[float] = Query(None),
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

    if price is not None:
        query["price"] = price

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