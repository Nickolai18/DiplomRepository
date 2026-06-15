# from fastapi import FastAPI, Response
# from datetime import datetime
 
# app = FastAPI()
 
# @app.get("/login")
# def root(response: Response):
#     now = datetime.now()    # получаем текущую дату и время
#     response.set_cookie(key="last_visit", value=now)
#     return  {"message": "куки установлены"}

user = {
    "tt": "rer"
}
user.update({"gg":"sf"})
print(user)
