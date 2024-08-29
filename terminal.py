from helper import send_emails, manage_users, http_send

print("Welcome to MacroMw\n")
print("Browse tasks from the list below")
print("Type in `home` to go to homepage, from anywhere\n")

tasks = [
    "1. Send Emails",
    "2. Manage Users",
    "3. Clear receipts",
    "4. Settings"
]

for task in tasks:
    print(task)
task = input("Enter your choice: ")

if task == "1":
    send_emails()
elif task == "2":
    manage_users()

res = http_send("liwewerobati@gmail.com","Attach2","Say hello to the attachment email", "file.pdf")

if res:
    print("Zatheka")
else:
    print("Zivuta")
