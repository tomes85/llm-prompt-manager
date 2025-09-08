import sys
from typing import List
import json
import pyperclip

PROMPT_JSON_FILE = "myprompts.json"

class Prompt:
    def __init__(self, name: str, prompt: str):
        self.name = name
        self.prompt = prompt

def load_prompts(file: str) -> List[Prompt]:
    list_of_prompts = []
    try:
        with open(file, "r") as json_data:
            d = json.load(json_data)

        for p_json in d:
            prompt = Prompt(name = p_json["name"], prompt = p_json["prompt"])
            list_of_prompts.append(prompt)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON.")
        return []
    
    return list_of_prompts

def save_prompts(file: str, list_of_prompts: List[Prompt]) -> None:
    prompts_dict = []
    for prompt in list_of_prompts:
        prompts_dict.append({"name": prompt.name, "prompt": prompt.prompt})

    with open(file, "w") as json_data:
        json.dump(prompts_dict, json_data, indent=2)


def add_new_prompt() -> None:
    prompts = load_prompts(PROMPT_JSON_FILE)
    prompt_name = input("Enter the name of the prompt: ")
    prompt_prompt = input("Enter the prompt: ")

    prompt = Prompt(name=prompt_name, prompt=prompt_prompt)
    prompts.append(prompt)
    save_prompts(PROMPT_JSON_FILE, prompts)

def list_all_prompts():
    prompts = load_prompts(PROMPT_JSON_FILE)

    for i,prompt in enumerate(prompts):
        print(f"==========================")
        print(f"Prompt Number: {i}")
        print(f"Name of the prompt: {prompt.name}")
        print(f"The prompt: {prompt.prompt}")

def delete_prompt(number: int) -> None:
    prompts = load_prompts(PROMPT_JSON_FILE)
    if number < len(prompts):
        del prompts[number]
        save_prompts(PROMPT_JSON_FILE, prompts)

def copy(number: int) -> None:
    prompts = load_prompts(PROMPT_JSON_FILE)
    if number < len(prompts):
        prompt = prompts[number].prompt
        pyperclip.copy(prompt)
        print(f"Copied prompt number {number} into clipboard!")
    else:
        print("Index out of range!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python prompt.py <Command> <options>")

    if sys.argv[1] == "add":
        print("Adding new prompt")
        add_new_prompt()

    if sys.argv[1] == "list":
        print("Listing available prompts:")
        list_all_prompts()

    if sys.argv[1] == "delete":
        print("Deleting prompt")

        if len(sys.argv) != 3:
            print("Usage: python prompt.py delete <number>")
            print("Use the list command to view the number of the prompt to be deleted.")
            exit(0)
        delete_prompt(int(sys.argv[2]))

    if sys.argv[1] == "copy":
        if len(sys.argv) != 3:
            print("Usage: python prompt.py copy <number>")
            print("Use the list command to view the number of the prompt to be copied.")
            exit(0)
        copy(int(sys.argv[2]))

        



    

