import json
import re
from pathlib import Path

# File where profile data will be stored
PROFILE_FILE = "profile.json"


def validate_name(name):
    return len(name.strip()) >= 2


def validate_age(age):
    return age.isdigit() and 0 < int(age) < 130


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_phone(phone):
    # Allows digits with optional + sign
    pattern = r"^\+?\d{7,15}$"
    return re.match(pattern, phone) is not None


def get_valid_input(prompt, validator, error_message):
    while True:
        value = input(prompt).strip()

        if validator(value):
            return value

        print(f"❌ {error_message}\n")


def collect_profile():
    print("\n=== User Profile Setup ===\n")

    profile = {
        "name": get_valid_input(
            "Enter full name: ",
            validate_name,
            "Name must contain at least 2 characters."
        ),

        "age": int(get_valid_input(
            "Enter age: ",
            validate_age,
            "Please enter a valid age between 1 and 129."
        )),

        "email": get_valid_input(
            "Enter email address: ",
            validate_email,
            "Please enter a valid email address."
        ),

        "phone": get_valid_input(
            "Enter phone number: ",
            validate_phone,
            "Phone number must contain 7–15 digits."
        ),

        "skills": input(
            "Enter skills (comma-separated): "
        ).split(",")
    }

    # Clean whitespace from skills
    profile["skills"] = [skill.strip() for skill in profile["skills"] if skill.strip()]

    return profile


def save_profile(profile):
    with open(PROFILE_FILE, "w") as file:
        json.dump(profile, file, indent=4)

    print(f"\n✅ Profile saved to '{PROFILE_FILE}'")


def load_profile():
    if not Path(PROFILE_FILE).exists():
        print("\n❌ No saved profile found.")
        return None

    with open(PROFILE_FILE, "r") as file:
        return json.load(file)


def display_profile(profile):
    print("\n=== Saved User Profile ===\n")

    for key, value in profile.items():
        if isinstance(value, list):
            value = ", ".join(value)

        print(f"{key.title()}: {value}")


def main():
    while True:
        print("\n===== PROFILE MANAGER =====")
        print("1. Create new profile")
        print("2. View saved profile")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            profile = collect_profile()
            save_profile(profile)

        elif choice == "2":
            profile = load_profile()

            if profile:
                display_profile(profile)

        elif choice == "3":
            print("\n👋 Goodbye!")
            break

        else:
            print("\n❌ Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()