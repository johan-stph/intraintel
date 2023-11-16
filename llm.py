from langchain.llms import OpenAI

context = "My name is Johannes and i am 22 years old"

llm = OpenAI(model="gpt-3.5-turbo")


def generate_prompt(context, user_input):
    """
    Combine context and user input into a single prompt.
    """
    return f"{context}\n\nUser: {user_input}\nAI:"

def get_response(prompt):
    """
    Send the prompt to GPT-3.5 and get a response.
    """
    return llm.generate([prompt], max_tokens=500)



# Example usage
while True:
    # Get user input
    user_input = input("Enter your question or 'quit' to exit: ")
    if user_input.lower() == 'quit':
        break

    # Generate and send prompt
    prompt = generate_prompt(context, user_input)
    response = get_response(prompt)

    # Print the response
    print("Response from GPT-3.5:", response)