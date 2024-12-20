from locust import HttpUser, TaskSet, task, between, tag
import random
import string
import time
import csv

# Initialize a CSV file to log check-in requests
with open('checkin_log.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

class CompetitionBehavior(TaskSet):
    def on_start(self):
        self.request_count = 0
        self.start_time = time.time()
        # Simulate user registration
        self.user_name = ''.join(random.choices(string.ascii_lowercase, k=10))
        self.password = "testpassword"
        self.client.post("/api/auth/register", json={"user_name": self.user_name, "password": self.password})

        # Simulate user login to get a token
        response = self.client.post("/api/auth/login", json={"user_name": self.user_name, "password": self.password})
        
        # Check if the response is successful and contains JSON
        if response.status_code == 200:
            try:
                self.token = response.json().get("access_token")
            except ValueError:
                print("Login response is not JSON:", response.text)
                self.token = None
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            self.token = None

        # If token is not available, skip this round
        if not self.token:
            print("Skipping this round due to missing access token.")
            return

    def adjust_task_weights(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        total_duration = 140
        early_phase_threshold = total_duration * 0.45
        mid_phase_threshold = total_duration * 0.75
        final_phase_threshold = total_duration * 0.8
        post_final_phase_threshold = total_duration * 0.9

        if elapsed_time < early_phase_threshold:
            # Early phase: Lower upload weight
            self.tasks = {
                self.get_leaderboard: 5,
                self.join_team: 2,
                self.create_team: 2,
                self.register_and_upload: 2,
            }
        elif elapsed_time < mid_phase_threshold:
            # Mid phase: Moderate upload weight
            self.tasks = {
                self.get_leaderboard: 3,
                self.join_team: 3,
                self.create_team: 2,
                self.register_and_upload: 3,
            }
        elif elapsed_time < final_phase_threshold:
            # Final phase: High upload weight
            self.tasks = {
                self.get_leaderboard: 1,
                self.join_team: 2,
                self.create_team: 2,
                self.register_and_upload: 8,
            }
        elif elapsed_time < post_final_phase_threshold:
            # Post-final phase: Exponentially high upload weight
            self.tasks = {
                self.get_leaderboard: 1,
                self.join_team: 1,
                self.create_team: 0,
                self.register_and_upload: 6,
            }
        else:
            # Post-final phase: Exponentially high upload weight
            self.tasks = {
                self.get_leaderboard: 2,
                self.join_team: 1,
                self.create_team: 0,
                self.register_and_upload: 32,
                self.login: 1,  # Very frequent login in post-final phase
            }

    @tag('checkin')
    @task
    def register_and_upload(self):
        self.request_count += 1
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/api/user/upload-post", json={"content": "This is a test post"}, headers=headers)
        
        # Log the request count with a timestamp
        with open('checkin_log.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['timestamp', 'count'])
            writer.writerow({'timestamp': time.time(), 'count': self.request_count})

    @task
    def get_leaderboard(self):
        self.client.get("/api/team/leaderboard")

    @task
    def create_team(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        team_name = ''.join(random.choices(string.ascii_lowercase, k=10))
        self.client.post("/api/team/create-team", json={"team_name": team_name}, headers=headers)

    @task
    def join_team(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/api/team/all-teams", headers=headers)
        
        if response.status_code == 200:
            try:
                teams = response.json()
                if teams:
                    team_name = random.choice(teams).get("name")
                    self.client.post("/api/team/join-team", json={"team_name": team_name}, headers=headers)
            except ValueError:
                print("Response is not JSON:", response.text)
        else:
            print(f"Failed to get teams: {response.status_code} - {response.text}")

    @task
    def login(self):
        # Simulate user login to get a token
        response = self.client.post("/api/auth/login", json={"user_name": self.user_name, "password": self.password})
        
        # Check if the response is successful and contains JSON
        if response.status_code == 200:
            try:
                self.token = response.json().get("access_token")
            except ValueError:
                print("Login response is not JSON:", response.text)
                self.token = None
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            self.token = None

    def on_stop(self):
        # Adjust task weights dynamically based on simulation progress
        self.adjust_task_weights()

class CompetitionUser(HttpUser):
    tasks = [CompetitionBehavior]
    wait_time = between(1, 5)