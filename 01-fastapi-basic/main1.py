from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/slow-async", tags=["학습용"])
async def slow_async():
    # async 방식의 대기시간 측정
    await asyncio.sleep(3) #sec
    return {"type", "async", "message: 3초 대기 완료"}

@app.get("/slow-block", tags=["학습용"])
async def slow_block():
    # sync 방식의 대기시간 측정
    time.sleep(3) #sec
    return {"type", "block", "message: 3초 대기 완료"}