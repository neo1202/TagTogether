from locust import HttpUser, TaskSet, task, between
import random
import string
import time

class CompetitionBehavior(TaskSet):
    # Before the test starts, the user needs to register a new account and log in to obtain a JWT token
    def on_start(self):
        # Initialize start time when the user starts
        self.start_time = time.time()
        # Simulate user registration
        self.user_name = ''.join(random.choices(string.ascii_lowercase, k=10))
        self.password = "testpassword"
        self.client.post("/api/auth/register", json={"user_name": self.user_name, "password": self.password})

        # Simulate user login to get a token
        response = self.client.post("/api/auth/login", json={"user_name": self.user_name, "password": self.password})
        self.token = response.json().get("access_token")

    # Adjust weights dynamically to simulate increasing traffic
    def adjust_task_weights(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time  # Use custom start time

        # Define time thresholds as a percentage of total run time
        total_duration = 100
        early_phase_threshold = total_duration * 0.5
        mid_phase_threshold = total_duration * 0.75
        final_phase_threshold = total_duration * 0.9

        # Adjust task weights based on elapsed time
        if elapsed_time < early_phase_threshold:
            # Early phase: Lower upload weight
            self.tasks = {
                self.get_leaderboard: 5,
                self.join_team: 3,
                self.create_team: 1,
                self.register_and_upload: 2,  # Lower weight for upload
            }
        elif elapsed_time < mid_phase_threshold:
            # Mid phase: Moderate upload weight
            self.tasks = {
                self.get_leaderboard: 3,
                self.join_team: 3,
                self.create_team: 2,
                self.register_and_upload: 3,  # Moderate weight for upload
            }
        elif elapsed_time < final_phase_threshold:
            # Final phase: High upload weight
            self.tasks = {
                self.get_leaderboard: 2,
                self.join_team: 1,
                self.create_team: 2,
                self.register_and_upload: 5,  # High weight for upload
            }
        else:
            # Post-final phase: Maximum upload weight
            self.tasks = {
                self.get_leaderboard: 1,
                self.join_team: 1,
                self.create_team: 1,
                self.register_and_upload: 10,  # Maximum weight for upload
            }

    @task
    def register_and_upload(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/api/user/upload-post", json={"content": "This is a test post"}, headers=headers)

    @task
    def get_leaderboard(self):
        self.client.get("/api/team/leaderboard/")

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

    def on_stop(self):
        # Adjust task weights dynamically based on simulation progress
        self.adjust_task_weights()


class CompetitionUser(HttpUser):
    tasks = [CompetitionBehavior]
    wait_time = between(1, 5)