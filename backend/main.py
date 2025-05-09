from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from chat import ChatSession

# app = FastAPI()
#
# # 允许跨域访问（方便你前端调用）
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 生产环境建议设置指定域名
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

app = FastAPI()


from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.exception_handlers import request_validation_exception_handler
import logging

# Explicitly print error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f" Validation error: {exc.errors()}")
    # logging.error(f"❗ Body received: {exc.body}")
    return await request_validation_exception_handler(request, exc)


class ResumeRequest(BaseModel):
    name: str
    education: str
    skills: str
    experience: str
    job_description: str
    type: str  # e.g., 'json_resume_bullet'
    fmt: str
    tone: str # e.g., 'concise'
    requirement: str

@app.post("/generate")
def generate(request: ResumeRequest):
    # 初始化临时对话 session
    session = ChatSession(
        output_format=request.fmt,
        output_type=request.type,
        tone=request.tone
    )

    # 构造用户输入文本
    user_input = {
        "name":  request.name,
        "education": request.education,
        "skills": request.skills,
        "experience": request.experience,
        "jd": request.job_description,
        "requirement": request.requirement

    }

    session.add_user_input(user_input)
    response = session.get_bot_response()
    return {"output": response}