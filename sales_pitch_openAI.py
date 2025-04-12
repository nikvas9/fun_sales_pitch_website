"""
This is a multishot LLM Model
Must have .env file in the same folder:
  File name: ".env" //without quotes
  File contents:OPENAI_API_KEY=sk-proj <paste your OpenAI key from https://platform.openai.com/settings/organization/api-keys here, something like "sk-proj......">
"""


import openai
import bs4
import requests
import json
import os
import sys
from typing import List, Dict, Any # Added type hints

# Ensure OpenAI API key is available early
# Consider loading from .env file using python-dotenv
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
    sys.exit(1) # Exit if key is missing
# Initialize OpenAI client once
client = openai.OpenAI(api_key=api_key)

MODEL="gpt-4o-mini"

class Website:
    url: str
    title: str
    # description: str # description is declared but never assigned
    body: bytes # response.content is bytes
    links: List[str]
    text: str

    # Class attribute for the system prompt - using f-string for cleaner multiline
    link_system_prompt = f"""You are provided with a list of links found on a webpage.
      You are able to decide which of the links would be most relevant to include in a brochure about the company, \
      such as links to an About page, or a Company Page, or Careers/Jobs pages.
      You should respond in JSON as in this example:
      {{
          "links": [
              {{"type": "about page", "url": "https://example.com/about"}},
              {{"type": "careers page", "url": "https://example.com/careers"}}
          ]
      }}""" # Corrected JSON example formatting

    def __init__(self, url: str):
        """Initializes the Website object by fetching and parsing the URL."""
        self.url = url
        # Set default values in case of errors
        self.title = "Initialization Error"
        self.text = ""
        self.links = []
        self.body = b""

        try:
            # Use a common user-agent header
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(self.url, headers=headers, timeout=10) # Added timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            self.body = response.content

            soup = bs4.BeautifulSoup(self.body, 'html.parser')
            self.title = soup.title.string if soup.title else 'No title found'

            if soup.body:
                # Decompose irrelevant tags *before* getting text for cleaner output
                # Added more common irrelevant tags like header, footer, nav
                for irrelevant in soup.body(["script", "style", "img", "input", "header", "footer", "nav", "aside"]):
                    if irrelevant: # Check if tag exists before decomposing
                       irrelevant.decompose()
                # Get text *after* decomposition
                self.text = soup.body.get_text(separator='\n', strip=True)
            else:
                self.text = 'No body tag found' # More informative message

            # Extract links more robustly: ensure 'href' exists and starts with http/https
            links_raw = [link.get('href') for link in soup.find_all('a', href=True)]
            self.links = [link for link in links_raw if isinstance(link, str) and link.startswith(('http://', 'https://'))]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {self.url}: {e}", file=sys.stderr)
            self.title = f"Error fetching URL: {e}" # Store error in title
            # Keep default empty values for text, links, body
        except Exception as e:
            # Catch potential BeautifulSoup errors or others
            print(f"Error processing URL {self.url}: {e}", file=sys.stderr)
            self.title = f"Error processing URL: {e}" # Store error in title
            # Keep default empty values

    def get_contents(self) -> Dict[str, str]:
        """Returns the title and extracted text content of the webpage."""
        return {
            'Webpage Title': self.title,
            'Webpage Contents': self.text
        }

    def _get_links_user_prompt(self) -> str:
        """Helper method to generate the user prompt for link analysis."""
        # Use f-string for cleaner formatting
        prompt = (
            f"Here is the list of links from the website {self.url} - "
            "please decide which of these are relevant web links for a brochure about the company. "
            "Please do not include terms of service, privacy policy, or any other irrelevant links.\n\n"
            "Links (some might be irrelevant):\n"
        )
        # Handle case with no links found
        if not self.links:
            prompt += "No links found on the page."
        else:
            prompt += "\n".join(self.links)
        return prompt

    def get_relevant_links(self) -> Dict[str, Any]:
        """
        Uses OpenAI to analyze the links found on the page and returns a structured
        list of relevant ones.
        """
        # Check if initialization failed
        if "Error" in self.title:
             return {"error": f"Cannot get links due to initialization failure: {self.title}"}
        # Check if there are links to analyze
        if not self.links:
            print(f"No links found on {self.url} to analyze.", file=sys.stderr)
            return {"links": []} # Return empty list if no links

        try:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": self.link_system_prompt},
                    {"role": "user", "content": self._get_links_user_prompt()}
                ],
                response_format={"type": "json_object"}
            )
            result_content = completion.choices[0].message.content
            if not result_content:
                 print("Warning: Received empty content from OpenAI.", file=sys.stderr)
                 return {"links": [], "warning": "Empty response from AI"}

            # Parse the JSON content
            return json.loads(result_content)

        except openai.APIError as e:
             print(f"OpenAI API error: {e}", file=sys.stderr)
             return {"error": "OpenAI API error", "details": str(e)}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response from OpenAI: {e}", file=sys.stderr)
            print(f"Raw response content: {result_content}", file=sys.stderr)
            return {"error": "Invalid JSON response from AI", "details": str(e), "raw_content": result_content}
        except Exception as e:
            # Catch other potential errors during the API call or processing
            print(f"An unexpected error occurred in get_relevant_links: {e}", file=sys.stderr)
            return {"error": "Unexpected error during link analysis", "details": str(e)}

    def translater(company_name, url, language_from, language_to):
        # Assuming you have a function to translate text
        # This is a placeholder for the actual translation logic
        data = Website.create_brochure(company_name, url)
        if not data:
            print("No data to translate.")
            return None
        if language_from = language_to return data
        try:
            response = openai.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"You are a translator from {language_from} to {language_to}."},
                    {"role": "user", "content": data}
                ],
            )
            data = response.choices[0].message.content
            print("Translation completed successfully.")
            print("Translated text:", data)
        except Exception as e:
            print(f"Error during translation: {e}")
            return None
        # Assuming the response contains the translated text
        return f"Translated from {language_from} to {language_to}: {data}"

# --- Execution ---
if __name__ == "__main__":
    company_name = "Example company"
    target_url = "https://example.com"
    translate_from = "English"
    translate_to = "Spanish"
    print(f"Fetching and analyzing links for: {target_url}")

    # Create an instance of the Website class
    website_obj = Website(target_url)

    # Check if the website object was initialized successfully before proceeding
    if "Error" in website_obj.title:
         print(f"Could not process website {target_url}. Exiting.", file=sys.stderr)
         # Optionally print website_obj.get_contents() for more details
         sys.exit(1)

    # Call the instance method to get relevant links
    sales_brochure = website_obj.translater(company_name, target_url, translate_from, translate_to)

    # Print the result
    print("\nRelevant links analysis result:")
    # Pretty print the JSON for readability
    print(json.dumps(relevant_links_data, indent=2))

    # Example of getting contents (uncomment to use)
    # print("\nWebsite Contents:")
    # print(json.dumps(website_obj.get_contents(), indent=2))
