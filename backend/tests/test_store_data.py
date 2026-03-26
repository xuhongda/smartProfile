import requests
import json

# 测试数据
test_data = {
    "users": [
        {
            "username": "testuser1",
            "email": "test1@example.com",
            "password_hash": "hashed_password1"
        },
        {
            "username": "testuser2",
            "email": "test2@example.com",
            "password_hash": "hashed_password2"
        }
    ],
    "profiles": [
        {
            "user_id": 1,
            "name": "Test User 1",
            "bio": "This is test user 1",
            "location": "Beijing"
        },
        {
            "user_id": 2,
            "name": "Test User 2",
            "bio": "This is test user 2",
            "location": "Shanghai"
        }
    ],
    "education": [
        {
            "profile_id": 1,
            "school": "University A",
            "degree": "Bachelor",
            "field": "Computer Science",
            "start_date": "2020-09-01",
            "end_date": "2024-06-30"
        },
        {
            "profile_id": 2,
            "school": "University B",
            "degree": "Master",
            "field": "Data Science",
            "start_date": "2021-09-01",
            "end_date": "2023-06-30"
        }
    ],
    "experience": [
        {
            "profile_id": 1,
            "company": "Company A",
            "position": "Software Engineer",
            "start_date": "2024-07-01"
        },
        {
            "profile_id": 2,
            "company": "Company B",
            "position": "Data Analyst",
            "start_date": "2023-07-01"
        }
    ],
    "skills": [
        {
            "profile_id": 1,
            "name": "Python",
            "level": 5
        },
        {
            "profile_id": 1,
            "name": "JavaScript",
            "level": 4
        },
        {
            "profile_id": 2,
            "name": "Python",
            "level": 4
        },
        {
            "profile_id": 2,
            "name": "SQL",
            "level": 5
        }
    ]
}

# 发送请求
try:
    response = requests.post(
        "http://localhost:8000/store-data",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print("Response status code:", response.status_code)
    print("Response content:", response.json())
except Exception as e:
    print(f"Error: {e}")
