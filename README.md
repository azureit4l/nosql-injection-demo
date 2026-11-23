# Topic 12 - Modern Database Attacks

This project is a login demo for the Introduction to Information Security course. It compares a vulnerable MongoDB login with a login that checks input types and passwords.

**Note:** Run the project on localhost only. The vulnerable login is for the class demonstration.

## Group

- Group: N04
- Class: 502061
- Kieu Quoc Thai - 525H0192
- Pham Thai Nguyen - 525H0174

## Requirements

- Python 3
- MongoDB Community Server
- Web browser
- MongoDB Compass (to view the database)

## Run the project

1. Start MongoDB on your computer.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment:

```bash
py -m venv .venv
.venv\Scripts\activate
```

4. Install the libraries:

```bash
pip install -r requirements.txt
```

5. Start the application:

```bash
python app.py
```

6. Open `http://127.0.0.1:5000` in your browser.

## Demo account

- Username: `admin`
- Password: `Admin@123`

## Demo steps

1. Log in normally on both sides with the demo account.
2. Click **Try $gt Injection** on the Vulnerable Login side. It should return a successful login even though the real password was not sent.
3. Click **Try the Same Payload** on the Secure Login side. It should reject the request because the password is an object, not a string.
4. Open MongoDB Compass and view the `nosql_injection_demo` database.

## Collections

- `vulnerable_users` has the demo password as text. It is used to show the vulnerable query.
- `secure_users` has `password_hash`. The application checks the entered password against this hash.

## Main code

The vulnerable login puts the received values directly into a MongoDB query:

```python
user = vulnerable_users.find_one({
    "username": username,
    "password": password
})
```

The attack button sends this password value:

```json
{ "$gt": "" }
```

`$gt` means greater than. Because the saved demo password is a non-empty string, the condition can match it. The secure login accepts only string inputs, searches by username, and checks the password hash separately.

The midterm report also discussed `$ne`. `$ne` means not equal, while `$gt` means greater than. They are different MongoDB query operators, but both can change query conditions when untrusted input is used as part of a query. This final demo uses `$gt`, as suggested in Topic 12.
