# Starting up
1. Install Docker
2. Clone
3. `docker-compose up --build -d`
4. To create superuser: `docker-compose exec django python3 /app/src/manage.py createsupperuser`
5. http://localhost:8080/admin to access admin panel 

# API methods:

## 1. User creation
- http://localhost:8080/users/
- POST
```
{
    "username": str,
    "last_name": str,
    "first_name": str,
    "patronymic_name": str,
    "sex": "Male" / "Female" / "Other" / "",
    "birthdate": date (YYYY-MM-DD),
    "groups": [id, id]
}
```

## 2. User edit
- http://localhost:8080/users/<USER_ID>/
- GET, PUT, PATCH
```
{
    "username": str,
    "last_name": str,
    "first_name": str,
    "patronymic_name": str,
    "sex": "Male" / "Female" / "Other" / "",
    "birthdate": date (YYYY-MM-DD),
    "groups": [id, id]
}
```

## 3. User inactivation
- http://localhost:8080/users/<USER_ID>/inactivate/
- PATCH
- Send any PATCH request to inactivate user.

## 4. Get doctor's free slots
- http://localhost:8080/timetable/doctor/<DOCTOR_ID>/
- GET

## 5. Sign up for an appointment
- http://localhost:8080/timetable/slot/<SLOT_ID>/signup/
- PATCH
- Send any PATCH request to sign up

## 6. Cancel an appointment
- http://localhost:8080/timetable/slot/<SLOT_ID>/cancel/
- PATCH
- Send any PATCH request to cancel an appointment

## 7. Signups statistics
- http://localhost:8080/timetable/stat/
- GET
- Params (optional):
  - **start_date**: date (YYYY-MM-DD), default: today
  - **end date**: date (YYYY-MM-DD), default: start_date + 30 days
  
## 8. Get auth token
- http://localhost:8080/api-token-auth/
- POST
```
{
  "username": str,
  "password": str
}
```
