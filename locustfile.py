from locust import SequentialTaskSet, task, User, between
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
import time

class StreamlitTaskSet(SequentialTaskSet):
    def on_start(self):
        chrome_options = Options()
        # headlessモードの場合は下記コメントを外す
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 初回アクセス：action=local
        start_time = time.time()
        self.driver.get("http://localhost:8501?action=local")
        response_time = int((time.time() - start_time) * 1000)
        print("Initial page loaded with action=local")
        # ユーザーインスタンス経由でイベントを発火
        self.user.environment.events.request.fire(
            request_type="selenium",
            name="GET /action=local",
            response_time=response_time,
            response_length=0,
            exception=None,
            context={}
        )
    
    @task
    def trigger_fastapi(self):
        start_time = time.time()
        self.driver.get("http://localhost:8501?action=fastapi")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "object-key-val"))
        )

        response_time = int((time.time() - start_time) * 1000)
        print("Triggered action=fastapi")
        self.user.environment.events.request.fire(
            request_type="selenium",
            name="GET /action=fastapi",
            response_time=response_time,
            response_length=0,
            exception=None,
            context={}
        )
    
    def on_stop(self):
        self.driver.quit()

class StreamlitUser(User):
    tasks = [StreamlitTaskSet]
    wait_time = between(5, 10)
