# AI-Powered Website Sales pitch & Brochure Generator

## Description

This Python script leverages web scraping and OpenAI's language models to analyze a company's website, identify key pages (like "About" or "Careers"), aggregate their content, and generate a concise company brochure in Markdown format. It can also stream the brochure generation process.

## 📜 Disclaimer

This project is for **educational and demonstration purposes only**.  
All content and code are provided "as-is" without any warranty.  
The author assumes **no responsibility** for legal, financial, or other outcomes resulting from the use of this code.

- This repository does **not contain any proprietary or confidential information**.
- Any resemblance to real companies, systems, or data is purely coincidental.
- The views expressed here are solely my own and do not represent those of my employer (past or present).
- Use of this code is governed by the [MIT License](LICENSE) or the license specified in this repository.

Always consult your organization's policy and legal team before reusing or sharing code.

## Features

*   **Web Scraping:** Fetches and parses HTML content from specified URLs using `requests` and `BeautifulSoup`.
*   **Content Extraction:** Extracts relevant text content while attempting to remove boilerplate (scripts, styles, navigation, etc.).
*   **Link Analysis:** Identifies potentially relevant internal links (e.g., About, Careers) using an OpenAI model (`gpt-4o-mini` by default).
*   **Content Aggregation:** Fetches content from the identified relevant pages and combines it with the landing page content.
*   **AI Brochure Generation:** Uses an OpenAI model to synthesize the aggregated content into a professional company brochure.
*   **Streaming Output:** Supports streaming the brochure generation process for real-time feedback.
*   **Error Handling:** Includes basic error handling for network requests, content parsing, and API interactions.
*   **Configuration:** Easily configurable via environment variables and constants within the script.

## Requirements

*   Python 3.7+
*   An OpenAI API Key
*   Python libraries:
    *   `openai`
    *   `requests`
    *   `beautifulsoup4`
    *   `python-dotenv`
    *   `ipython` (Optional, for enhanced display features like `display(Markdown(...))` in notebooks)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *(Note: You'll need to create a `requirements.txt` file. You can generate one using `pip freeze > requirements.txt` after installing the libraries manually: `pip install openai requests beautifulsoup4 python-dotenv ipython`)*

3.  **Configure OpenAI API Key:**
    Create a file named `.env` in the root project directory and add your OpenAI API key:
    ```dotenv
    OPENAI_API_KEY=your_openai_api_key_here
    ```
    The script uses `python-dotenv` to load this key automatically. Alternatively, ensure the `OPENAI_API_KEY` environment variable is set in your system.

## Usage

You can run the script directly from the command line. The main execution block (`if __name__ == "__main__":`) is currently set up to process a specific URL (`https://anthropic.com`) and generate a brochure using the streaming function.

```bash
python your_script_name.py
To analyze a different website, modify the target_url and company variables within the if __name__ == "__main__": block:

python
# --- Main Execution ---
if __name__ == "__main__":
    target_url = "https://www.example.com" # Change this
    company = "Example Company"           # Change this

    print(f"\n=== Running Brochure Generation for: {company} ({target_url}) ===")

    # Choose one: Stream the brochure...
    stream_brochure(company, target_url)

    # ...or generate it non-streamed
    # brochure_content = create_brochure(company, target_url)
    # if brochure_content:
    #     print(f"\nSuccessfully generated brochure for {company}.")
    #     # Optionally save to file
    #     # with open(f"{company}_brochure.md", "w") as f:
    #     #     f.write(brochure_content)
    # else:
    #     print(f"\nFailed to generate brochure for {company}.")

    print("\n=== Script Finished ===")
You can also import the Website class and functions (get_relevant_links, aggregate_website_data, create_brochure, stream_brochure) into other Python scripts or Jupyter notebooks.

Configuration
Key configuration options are located near the top of the script:

MODEL: The OpenAI model used for analysis and generation (default: "gpt-4o-mini").
REQUEST_HEADERS: The User-Agent header used for web requests.
REQUEST_TIMEOUT: Timeout in seconds for web requests (default: 15).
Prompts (LINK_SYSTEM_PROMPT, BROCHURE_SYSTEM_PROMPT): Modify these to change the AI's behavior.
```


