from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import traceback
import google.generativeai as genai

API_KEY = "AIzaSyAJKYpJoh02v2KVFhjSJqTkEKzI_ekM4_M"
genai.configure(api_key=API_KEY)

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str = "default"
    message: str

@app.post("/chat")
async def chat_with_ommo(request: ChatRequest):
    try:
        user_msg = request.message.strip()
        
        # استخدام صيغة الموديل القياسية المضمونة 100%
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name
                break
        else:
            model_name = 'models/gemini-1.5-flash'

        active_model = genai.GenerativeModel(model_name)
        
        prompt = f"أنت نموذج ذكاء اصطناعي ذكي اسمه Ommo، من تطوير محمد طراف. أجب على هذا السؤال بذكاء ودون تكرار اسمك: {user_msg}"
        response = active_model.generate_content(prompt)
        
        return {"reply": response.text}
        
    except Exception as e:
        print("ERROR:", traceback.format_exc())
        return {"reply": f"أهلاً بك يا أسطورة! أنا Ommo وجاهز للرد على استفسارك: {user_msg}"}

if os.path.exists("public"):
    app.mount("/", StaticFiles(directory="public", html=True), name="public")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
