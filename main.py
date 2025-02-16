from fastapi import FastAPI
import numpy as np
import time
from datetime import datetime

app = FastAPI()

@app.get("/heavy_process")
def heavy_process():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start = time.time()
    n = 1000
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.dot(A, B)
    duration = time.time() - start
    print(timestamp, "Heavy process completed in", round(duration, 2), "seconds")
    return {"status": "completed", "duration": duration}
