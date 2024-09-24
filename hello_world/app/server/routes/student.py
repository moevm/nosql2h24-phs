from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import add_student, retrieve_students
from server.models.student import StudentSchema, ResponseModel

student_router = APIRouter()

@student_router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")

@student_router.get("/", response_description="Students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")