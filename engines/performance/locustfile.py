from locust import HttpUser, task

class LoadTest(HttpUser):

    def on_start(self):
        self.client.verify = False

    @task
    def index(self):
        self.client.get("/")