import random


topic = random.randint(1,10)
# Basic dictionary mapping numbers to words/phrases
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
    10: "number: -15 low, 15 high:"
}

# Access values by number

num = random.randint(-15,15)

# # number_to_points = {
# #     -15: 
# # }





prompt1 = "You will be given a topic and a number from a scale of -15 to 15 with context, give a phrase noun, item, or verb depending on the topic within the context of the topic to help the player guess the scale correctly. Do not repeat the same hints. Occasionally if the scale is either -15 or 15, throw in the most diabolical examples. Try not to give away what the scale is and use only the hints to help the player guess the scale."
prompt2 = "You will be given a hint, topic and scale. You have to guess within the scale a number that would match the vibe of the hint"

content1 = "Topic: " + number_to_word[topic] + " scale: " + str(num)
# content2 = "Topic: " + number_to_word[topic] + " hint: " + input("enter your hint")

choice = input("Would you like to guess or give the hints? (guess/hint): ").strip().lower()
if choice == "guess": 
   print(number_to_word[topic])
   topic = prompt1
   hint = content1

else: 
    print("Topic: " + number_to_word[topic] + " Scale: " + str(num))
    user_hint = input("enter your hint: ")
    content2 = "Topic: " + number_to_word[topic] + " hint: " + user_hint
    topic = prompt2
    hint = content2



from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": topic
      },
      {
        "role": "user",
        "content": hint
      }
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
print("\n")

if choice == "guess":
    user_guess = input("\nEnter your guess for the scale (-15 to 15): ").strip()
    try:
        user_guess = int(user_guess)
        if user_guess == num:
            print("Correct! You guessed the scale accurately. You get 4 points!")
        elif user_guess == num+1 or user_guess == num-1:
            print("Close! The correct scale was " + str(num) + ". You get 3 points!")
        elif user_guess == num+2 or user_guess == num-2:
            print("Not bad! The correct scale was " + str(num) + ". You get 2 points!")
        else:
            print(f"Wrong! The correct scale was {num}.")
    except ValueError:
        print("Invalid input. Please enter a number between -15 and 15.")
