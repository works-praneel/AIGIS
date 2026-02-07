from locust import HttpUser, task

class LoadTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")
