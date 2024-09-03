import json
from dotenv import dotenv_values
import requests


def get_token():
    config = dotenv_values(".env")
    auth_data = {
        "application_token": config["API_TOKEN"]
    }
    r = requests.post(
        "https://cdn.emnify.net//api/v1/authenticate",
        data=json.dumps(auth_data),
        headers={"Content-Type": "application/json"},
    )
    return r.json()["auth_token"]


def list_sims(auth_token):
    r = requests.get(
        "https://cdn.emnify.net/api/v1/sim?per_page=2000",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    data = r.json()
    sim_list = [{"name": s["endpoint"]["name"], "data": s} for s in data]
    sim_list = sorted(sim_list, key=lambda sim: sim["name"])
    return sim_list


def list_activated_sims(auth_token):
    return [s for s in list_sims(auth_token) if s["data"]["status"]["id"] == 1]


def list_suspended_sims(auth_token):
    return [s for s in list_sims(auth_token) if s["data"]["status"]["id"] == 2]


def activate_sim(auth_token, sim_id):
    r = requests.patch(
        f"https://cdn.emnify.net/api/v1/sim/{sim_id}",
        data=json.dumps({"status": {"id": 1}}),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
    )
    return r.status_code // 100 == 2


def suspend_sim(auth_token, sim_id):
    r = requests.patch(
        f"https://cdn.emnify.net/api/v1/sim/{sim_id}",
        data=json.dumps({"status": {"id": 2}}),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
    )
    return r.status_code // 100 == 2
