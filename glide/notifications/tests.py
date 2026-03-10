import requests

access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzczMTMxMTE5LCJpYXQiOjE3NzMxMjc1MTksImp0aSI6ImE1NmNmMWMzYWJjOTQ1Njg5ZmRjMTcwYWE0ODg0MGUzIiwidXNlcl9pZCI6IjUifQ.qtCf1xtttNH8MeNn-Ty5rT0v_V7H6ZJUSXw5n6G0N_I"
headers = {"Authorization": f"Bearer {access}"}
resp = requests.get("http://localhost:8000/api/notifications/", headers=headers)
print("GET notifications:", resp.status_code, resp.json())

# Assuming there is a notification with id 1, mark it as read
if resp.json()['results']:
    resp2 = requests.post("http://localhost:8000/api/notifications/1/mark_read/", headers=headers)
    print("Mark read:", resp2.status_code, resp2.json())
else:
    print("No notifications to mark as read")