# Manual for Dashboard

This project uses OpenAI's Assistants API to analyze utility bill data from a CSV file. It can answer questions about the data and generate visualizations based on your prompts.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Python and Pip**

    - This script requires Python. You can check if you have it by opening your terminal (or Command Prompt on Windows) and typing `python --version`. If you don't have it, download it from the [official Python website](https://www.python.org/downloads/). 
    - **For Windows users**: When installing Python, make sure to check the box that says "Add Python to PATH".
    - `pip` (the Python package installer) is included with Python versions 3.4 and later. If you have an older version of Python or if `pip` is not working, see the [official pip installation guide](https://pip.pypa.io/en/stable/installation/) for instructions.

2.  **OpenAI API Key**: You'll need an API key from OpenAI. You can get one by signing up on the [OpenAI platform](https://platform.openai.com/). To start using the API key, you have to provide a payment method and load some credits into your account. 

3.  **Data File**: A CSV file named `utility_bills.csv` containing your utility bill data. For now, this file must be in the same directory as the `test.py` script.

## Setup and Installation

Follow these steps to set up and run the project.

### 1. Download the Code

If you received this as a zip file, unzip it. Otherwise, make sure you have the `test.py` script and `requirements.txt` file in a folder on your computer.

### 2. Install Required Libraries

The script depends on the `openai` library. We'll use `pip`, Python's package installer, to install it from the `requirements.txt` file. The `import` statements within the `test.py` script will then be able to use this library.

Open your terminal or Command Prompt, navigate to the project folder, and run the following command:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs the necessary library.

### 3. Configure Your OpenAI API Key

You need to set your OpenAI API key as an environment variable so the script can securely access it.

**On macOS or Linux:**

Open your terminal and run the following command, replacing `'your-api-key'` with your actual key:

```bash
export OPENAI_API_KEY='your-api-key'
```

_Note: This key will only be set for your current terminal session. For a more permanent solution, you can add this line to your shell's startup file (e.g., `~/.bashrc`, `~/.zshrc`)._

**On Windows:**

Open Command Prompt and run this command, replacing `'your-api-key'` with your actual key:

```bash
set OPENAI_API_KEY='your-api-key'
```

Alternatively, you can set it through the System Properties:

1. Search for "Environment Variables" in the Start menu and select "Edit the system environment variables".
2. In the System Properties window, click the "Environment Variables..." button.
3. In the "User variables" section, click "New..."
4. For "Variable name", enter `OPENAI_API_KEY`.
5. For "Variable value", paste your OpenAI API key.
6. Click OK on all windows. You may need to restart your Command Prompt or your computer for the changes to take effect.

## How to Run the Script

Once you have completed the setup, you can run the script.

1.  Open your terminal or Command Prompt.
2.  Navigate to the directory where you saved the project files (`test.py`, `utility_bills.csv`, `requirements.txt`).
    ```bash
    # Example:
    cd path/to/your/project/folder
    ```
3.  Run the script using the following command:
    ```bash
    python test.py
    ```

## What to Expect

When you run the script, it will:

1.  Upload your `utility_bills.csv` file to OpenAI.
2.  Create a new OpenAI Assistant (or update a previously created one) designed for data analysis.
3.  Ask the assistant to analyze your data and create a visualization based on the prompt in the script.
4.  Print the assistant's text response to your terminal.
5.  If the assistant generates a chart or plot, it will be saved as a `.png` image file (e.g., `viz_image-xxxxxxxx.png`) in the same folder.

### Customizing the Analysis

The script includes a default prompt to analyze the total amount due and predict the next month's amount. You can change this prompt by editing the `content` in this section of `test.py`:

```python
# ... existing code ...
# Modify this for prompt
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="YOUR NEW PROMPT HERE. For example: 'Create a pie chart showing the distribution of charges by service type.'"
)
# ... existing code ...
```

```

```
