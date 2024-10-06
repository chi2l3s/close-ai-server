from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import g4f

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените на нужные вам источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель для входящего сообщения
class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(msg: Message):
    user_message = msg.message

    if not user_message:
        raise HTTPException(status_code=400, detail="Сообщение не получено")

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        
        msg_response = response.choices[0].message['content']  # Извлекаем ответ
        return {"response": msg_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
