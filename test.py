from openai import OpenAI, NotFoundError
import os, time

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

def upload_file():
    """Uploads the utility_bills.csv file to OpenAI."""
    print("Uploading file...")
    file = client.files.create(
        file=open("data/optima_sonoran.csv", "rb"),
        purpose="assistants"
    )
    print("File uploaded successfully.")
    return file

def choose_assistant(file):
    """Lists existing assistants and allows the user to choose one or create a new one."""
    print("Fetching existing assistants...")
    assistants = client.beta.assistants.list().data

    if assistants:
        print("Existing Assistants:")
        for i, assistant in enumerate(assistants):
            print(f"{i + 1}. {assistant.name} ({assistant.id})")

        while True:
            try:
                choice = input("Choose an assistant by number, or type 'n' to create a new one: ")
                if choice.lower() == 'n':
                    return create_assistant(file)
                
                assistant_index = int(choice) - 1
                if 0 <= assistant_index < len(assistants):
                    chosen_assistant_id = assistants[assistant_index].id
                    print(f"Using assistant: {assistants[assistant_index].name}")
                    # Update the assistant to use the new file.
                    return client.beta.assistants.update(
                        assistant_id=chosen_assistant_id,
                        tool_resources={"code_interpreter": {"file_ids": [file.id]}},
                    )
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'n'.")
    else:
        print("No existing assistants found.")
        return create_assistant(file)

def create_assistant(file):
    """Creates a new assistant."""
    print("Creating a new assistant...")
    assistant = client.beta.assistants.create(
        name="Utility Bill Analyst",
        instructions="You are an expert data analyst. Your role is to analyze utility bill data from CSV files, answer questions about it, and create visualizations. When asked to create a plot or chart, generate the image and make it available for download.",
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
        tool_resources={
            "code_interpreter": {
                "file_ids": [file.id]
            }
        },
        model="gpt-4o"
    )
    print(f"New assistant created: {assistant.name} ({assistant.id})")
    return assistant

def main():
    """Main function to run the analysis."""
    file = upload_file()
    assistant = choose_assistant(file)

    if not assistant:
        print("Could not obtain an assistant. Exiting.")
        return

    thread = client.beta.threads.create()

    # Modify this for prompt
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="From the provided water bill csv file, create a data visualization, such as a graph, analyzing the total amount due for each csv data point, and also create a data point predicting the total amount due for the month of 2024 June"
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    print(f"Starting run with assistant {assistant.id}...")
    # Poll until the Run is finished
    while run.status not in {"completed", "failed", "cancelled"}:
        time.sleep(2)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {run.status}")

    print("Run finished:", run.status)

    # Fetch the Assistant's reply & download any images it produced
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    for msg in reversed(messages.data):  # newest → oldest
        if msg.role != "assistant":
            continue

        for part in msg.content:
            if part.type == "text":
                print("\nAssistant says:\n", part.text.value)

            elif part.type == "image_file":
                image_id = part.image_file.file_id
                bin_data = client.files.content(image_id).read()

                out_path = f"viz_{image_id}.png"
                with open(out_path, "wb") as f:
                    f.write(bin_data)
                print(f"Saved chart to {out_path}")

if __name__ == "__main__":
    main()