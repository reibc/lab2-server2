from pymysql import connect
from fastapi import FastAPI, HTTPException
import json
server = FastAPI()

db = connect(host="clwxydcjair55xn0.chr7pe7iynqr.eu-west-1.rds.amazonaws.com", port=3306, user="lkn7ajxns24zkkwp", password="jouw6mxkhosaf6e3", db="l9liva98km3vqrba")
@server.get('/')
async def home():
    return {'message':'Welcome!'}

@server.get('/data')
async def get_data():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM persons")
        data = cursor.fetchall()
    return data

@server.get('/data/{id}')
async def get_data(id : int):
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM persons WHERE PersonID = {id}")
        data = cursor.fetchall()
    return data

@server.post("/data")
def post_data(person_id: int, last_name: str, first_name: str, address: str, city: str):
    try:
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO persons (PersonID, LastName, FirstName, Address, City) VALUES (%s, %s, %s, %s, %s)",
            (person_id, last_name, first_name, address, city)
            )
            db.commit()
        return {"message": "Data successfully inserted into the database"}
    except:
        raise HTTPException(status_code = 405, detail='ERROR: Duplicate ID!')
        

@server.delete("/rm/{id}")
async def delete_data(id: int):
    cursor = db.cursor()
    cursor.execute(f"DELETE from persons where PersonID = {id}")
    db.commit()

    return {"message": "Successfully deleted data"}
