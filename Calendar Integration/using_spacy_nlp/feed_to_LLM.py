
with open('calendar_events.txt', 'r') as file:
    prompt = file.read()

# Now you can use this prompt as input to your LLM
print(prompt)

import openai

# Initialize your OpenAI API key (replace with your own API key)
openai.api_key = 'your-api-key'

# Read the calendar data from the text file
with open('calendar_events.txt', 'r') as file:
    calendar_data = file.read()

prompt = f"""
You are tasked with generating a user profile based on the following calendar events and user preferences.

Calendar Data:
{calendar_data}

Based on this information, generate a detailed user profile, including the following:
- User's key interests (e.g., travel, business development)
- Preferred travel destinations or activities
- Professional goals and tendencies
- Social preferences (e.g., introverted/extroverted)
- Time management habits
- Other possible lifestyle indicators
"""

# Call GPT-3.5 to generate the user profile based on the prompt
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an AI that generates user profiles."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000,  # Adjust as needed to get a detailed response
    temperature=0.7   # Adjust the creativity level
)

# Print the response from GPT-3.5
print(response['choices'][0]['message']['content'])