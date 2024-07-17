
import uvicorn


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='localhost', reload=True, workers=2)


# host=194.195.86.148 port=32465 dbname=db_mct user=db_mlm password=!*j2zD&ae54MAK7Q
