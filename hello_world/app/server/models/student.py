from pydantic import BaseModel, Field


class StudentSchema(BaseModel):
    fullname: str = Field(...)
    course_of_study: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "course_of_study": "Water resources engineering",
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}