from argparse import ArgumentParser
import textwrap, os, json
from IPython.display import display, Markdown
import google.generativeai as genai

class Ask_AI():
    def __init__(self):

        GOOGLE_API_KEY = "AIzaSyCWoROsbgDUERdpjwVlMWLGqV36vC1H80U"

        self.file_name = 'data.json'

        self.data = []

        # Setting up the Argument Parser
        parser = ArgumentParser(
            prog='Ask AI.',
            description='Ask Gemini-Google-Ai Your Question.'
        )

        # add question argument
        parser.add_argument("question", type=str, 
                            help="To Ask AI Your Question:")

        # Parsing the command line arguments.
        args = parser.parse_args()

        # Set up the Generative AI configuration with the API key
        genai.configure(api_key=GOOGLE_API_KEY)

        # Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
        self.model = genai.GenerativeModel('gemini-pro')

        self.ask_Question(args)

    def ask_Question(self, args):
        # Get user input for the query
        if not args.question == None:
            response = self.model.generate_content(args.question)

            # Display the generated content in Markdown format
            display(self.to_markdown(response.text))

            for chunk in response:
                print(chunk.text)
                print("_" * 80)

        save = ''
        while save == '' or not save == 'y' and not save == 'n':
            save = input("\nSave it in File (y,n) : ")

        if save == "y" or save == "Y":
            if not args.question == None:
                self.data = self.save_question(args.question, response.text)  

    # Function to convert plain text to Markdown format
    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
    
    def save_question(self, question, answer):
        if os.path.exists(self.file_name) and self.data == []:
            # Load existing data from data.json
            try:
                self.data = self.read_file(self.file_name, self.data)
                self.data.append({'Question': question, 'Answer': answer})
            except json.JSONDecodeError or FileNotFoundError:
                # Handle the case where data.json is empty or invalid JSON.
                self.data.append({'Question': question, 'Answer': answer})
        elif (os.path.exists(self.file_name) and not self.data == []) or \
        (not os.path.exists(self.file_name) and not self.data == []) or \
        (not os.path.exists(self.file_name) and self.data == []):
            self.data.append({'Question': question, 'Answer': answer})

        file = open(self.file_name,"w")
        json.dump(self.data, file, indent=4)
        file.close()      

    def read_file(self, file_name, data):
        if os.path.exists(file_name):
            file = open(file_name, 'r')
            data = json.load(file)
            file.close()
            return data
        else:
            print("File Not Exist")
            return

if __name__ == "__main__":
    app = Ask_AI()