from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MeetingDetail(BaseModel):
    id: PyObjectId
    time: datetime
    psychologist_id: PyObjectId
    status: str


class User(MongoModel):
    mail: EmailStr
    password: str
    sex: str
    birth_date: datetime
    name: str
    surname: str
    phone_number: str
    meetings: List[MeetingDetail] = []
    reviews: List[PyObjectId] = []
    transactions: List[PyObjectId] = []


class Education(BaseModel):
    institution: str
    degree: str
    year_graduated: datetime


class WorkExperience(BaseModel):
    position: str
    place: str
    years: List[datetime]


class Psychologist(MongoModel):
    user: User
    price: float
    address: str
    meeting_format: str
    education: List[Education]
    work_experience: List[WorkExperience]
    language: str
    articles: List[PyObjectId] = []


class Meeting(MongoModel):
    time: datetime
    user_id: PyObjectId
    psychologist_id: PyObjectId
    status: str  # scheduled | completed | canceled


class Review(MongoModel):
    content: str
    user_id: PyObjectId
    psychologist_id: PyObjectId
    created_at: datetime
    rating: float


class Article(MongoModel):
    content: str
    psychologist_id: PyObjectId
    created_at: datetime
    updated_at: datetime


class Transaction(MongoModel):
    user_id: PyObjectId
    amount: float
    created_at: datetime
