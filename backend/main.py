from fastapi import FastAPI
from pydantic import BaseModel
from lumen import Lumen

app = FastAPI()
lumen = Lumen()

class Message(BaseModel):
    user_input: str
    user_name: str

@app.post("/ask")
def ask_lumen(msg: Message):
    lumen.remember("name", msg.user_name)
    reply = lumen.generate_reply(msg.user_input)
    return {"reply": reply}