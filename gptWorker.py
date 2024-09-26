import os,fnmatch,openai,re
from dotenv import load_dotenv
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

gitignore_file = ".gitignore"
load_dotenv()
openai.api_key = os.getenv('API_KEY')
other_ignore = ["gptWorker.py","README.md"]

def is_text_file(file_path):
    blacklist = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.mp4', '.mkv', '.avi', '.mov', '.webm', '.otf', '.ico', '.jfif']
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() in blacklist:
        return False
    return True

def parse_gitignore(gitignore_content): return [line.strip() for line in gitignore_content.splitlines() if line.strip() and not line.startswith("#")]

def process_folder(folder_path, gitignore_rules):
    return_text = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file in other_ignore: continue
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, start=folder_path)
            relative_dir = os.path.dirname(relative_path)
            if gitignore_rules and gitignore_rules.match_file(relative_path):
                continue
            is_text = is_text_file(file_path)
            return_text += f"\n\n::: Filename: {file} :::\n"
            return_text += f"::: Filepath: ./{relative_dir}{'' if relative_dir in ('', '.') else '/'} :::\n\n"
            if is_text:
                with open(file_path, "r", encoding="utf-8", errors='ignore') as source_file:
                    return_text += source_file.read()
            else:
                return_text += "::: Non-text file, content not included :::"
    return return_text

def main():
    gitignore_rules = None
    if os.path.exists(gitignore_file):
        with open(gitignore_file, "r") as f:
            gitignore_content = f.read()
        gitignore_patterns = parse_gitignore(gitignore_content)
        gitignore_rules = PathSpec.from_lines(GitWildMatchPattern, gitignore_patterns)

    gptObject = [
        {
            'role': 'system',
            'content': (
                "This file contains the concatenated content of a codebase.\n"+
                "Each file's content is preceded by a header containing the file name and its path.\n"+
                "The header format is as follows:\n"+
                "\n"+
                "::: Filename: <filename> :::\n"+
                "::: Filepath: <filepath_without_name> :::\n"+
                "\n"+
                "Non-text files are included as headers only, without content.\n"+
                "\n"+
                "---Start of codebase---\n"+
                process_folder(os.getcwd(), gitignore_rules)+"\n"+
                "---End of codebase---\n\n"
            )
        },
        {
            'role': 'user',
            'content': (
                "Please perform the following task on the given codebase:"+"\n"+
                ""+"\n"+
                input("Enter your task: ")+"\n"+
                ""+"\n"+
                "you can create new files by using a new name and path, Once you have made the necessary changes, please provide the updated codebase by listing the changed files with their respective headers and content, in the same format as the input:"+"\n"+
                ""+"\n"+
                "::: Filename: <filename> :::"+"\n"+
                "::: Filepath: <filepath_without_name> :::"+"\n"+
                "<file_content>"+"\n"+
                ""+"\n"+
                "Do not include any additional explanations or comments you should use a file instructions.txt for this, as the output will be parsed directly."+"\n"
            )
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=gptObject
    )

    # Calculer le nombre de tokens du message 'system'
    num_tokens_system = len(gptObject[0]['content'].split() + gptObject[1]['content'].split())
    print(f"Nombre de tokens total dans le message 'system' + 'user': {num_tokens_system}")

    gpt4_output = response.choices[0].message.content

    file_pattern = re.compile(r"::: Filename: (.*?) :::\n::: Filepath: (\..*?/) :::\n(.*?)(?=\n\n::: Filename:|\Z)", re.DOTALL)
    changed_files = file_pattern.findall(gpt4_output)
    for file in changed_files:
        filename, relative_dir, file_content = file
        filepath = os.path.join(os.getcwd(), relative_dir[2:], filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write("\n".join([k for k in file_content.split("\n") if k[:3] != "```"]))
    if len(changed_files) == 0:
        print(gpt4_output)
    if "instructions.txt" in gpt4_output:
        print("Please read the instructions.txt file for additional information.")
    print(f"{len(changed_files)} files updated.")

if __name__ == "__main__":
    while True:
        main()