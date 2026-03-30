# run once

from app.auth import init_db, create_user

init_db()

create_user("admin", "admin123", role="admin")

create_user("employee", "user123", role="user")

print("users created")