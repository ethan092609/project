import random
import re
from groq import Groq

# Initialize Groq client
client = Groq()

# Score tracking
player_score = 0
ai_score = 0
play_again = True

# Prompts
prompt1 = "You will be given a topic and a number from a scale of -15 to 15 with context, give a phrase noun, item, or verb depending on the topic within the context of the topic to help the player guess the scale correctly. Do not repeat the same hints. Occasionally if the scale is either -15 or 15, throw in the most diabolical examples. Try not to give away what the scale is and use only the hints to help the player guess the scale."

prompt2 = "You will be given a hint, topic and scale. You have to guess within the scale a number that would match the vibe of the hint. Respond with only the integer (no extra text)."

def extract_number(text):
    """Extract first integer from text, return None if not found."""
    numbers = re.findall(r'-?\d+', text)
    if numbers:
        return int(numbers[0])
    return None

def calculate_points(guess, actual):
    diff = abs(guess - actual)
    if diff == 0:
        return 4
    elif diff == 1:
        return 3
    elif diff == 2:
        return 2
    else:
        return 0

# Game loop
while play_again:
    topic = random.randint(1, 10)
    num = random.randint(-15, 15)

    number_to_word = {
        1: "midnight snack: -15 good, 15 bad",
        2: "classmates: -15 good, 15 bad",
        3: "weekend plans: -15 good, 15 bad",
        4: "games: -15 good, 15 bad",
        5: "fast food: -15 good, 15 bad",
        6: "clothing style: -15 good, 15 bad",
        7: "trends: -15 good, 15 bad",
        8: "sports: -15 hard, 15 easy",
        9: "music: -15 good, 15 bad",
        10: "number: -15 low, 15 high"
    }
    choice = input("\nWould you like to guess or give the hints? (guess/hint/quit): ").strip().lower()

    print(f"\n--- New Round ---")
    print(f"Topic: {number_to_word[topic]}")
    print(f"(Secret scale: {num})" if choice != 'guess' else "")  # Only show when giving hints
    

    if choice == "quit":
        break

    elif choice == "guess":
        # Player guesses based on AI hint
        content1 = f"Topic: {number_to_word[topic]} scale: {num}"

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": prompt1},
                {"role": "user", "content": content1}
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=True
        )

        print("\nAI Hint: ", end="")
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
        print("\n")

        try:
            user_guess = int(input("Enter your guess for the scale (-15 to 15): ").strip())
            points = calculate_points(user_guess, num)
            player_score += points

            if points == 4:
                print(f"Correct! You get {points} points!")
            elif points > 0:
                print(f"Close! The correct scale was {num}. You get {points} points!")
            else:
                print(f"Wrong! The correct scale was {num}.")
        except ValueError:
            print("Invalid input. No points awarded.")

    elif choice == "hint":
        # Player gives hint, AI guesses
        user_hint = input("Enter your hint: ")
        content2 = f"Topic: {number_to_word[topic]} hint: {user_hint}"

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": prompt2},
                {"role": "user", "content": content2}
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=True
        )

        print("\nAI Guess: ", end="")
        ai_response = ""
        for chunk in completion:
            chunk_text = chunk.choices[0].delta.content or ""
            print(chunk_text, end="")
            ai_response += chunk_text
        print("\n")

        # Try to extract number from AI response
        ai_guess = extract_number(ai_response)
        if ai_guess is not None and -15 <= ai_guess <= 15:
            points = calculate_points(ai_guess, num)
            ai_score += points
            print(f"AI guessed {ai_guess}. Correct scale was {num}. AI gets {points} points.")
        else:
            print(f"AI's response couldn't be parsed as a valid number. No points awarded.")

    else:
        print("Invalid choice. Please enter 'guess', 'hint', or 'quit'.")
        continue

    # Show current scores
    print(f"\nCurrent Scores — Player: {player_score} | AI: {ai_score}")

    again = input("\nPlay another round? (yes/no): ").strip().lower()
    if again != 'yes':
        play_again = False

print(f"\nGame Over! Final Scores — Player: {player_score} | AI: {ai_score}")