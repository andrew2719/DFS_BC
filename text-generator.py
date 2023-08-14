import random
import string
import os


def generate_random_text(size):
    # Define characters that can be used in the random text
    characters = string.ascii_letters + string.digits + string.punctuation + " "  # Include space

    # Generate a random string
    random_string = ''.join(random.choice(characters) for _ in range(size))

    return random_string


preferred_size_kb = 10  # Change this to your preferred size in KB
preferred_size_bytes = preferred_size_kb * 1024  # Convert KB to bytes

random_text = generate_random_text(preferred_size_bytes)

output_file = 'text-file.txt'

with open(output_file, "w") as file:
    file.write(random_text)

print(f"{os.path.getsize(output_file)} KB 'text-file' created")
