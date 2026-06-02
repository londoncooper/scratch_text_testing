import ast
import time
import subprocess
import re
import random
import msvcrt
import prompt_toolkit
from prompt_toolkit import prompt
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.key_binding import KeyBindings

def insert_randoms(main_string, target_sub):
    # Define a function to generate the replacement string
    pattern = "|".join(re.escape(word) for word in target_sub)
    def add_number(match):
        # Returns the found substring + a random integer
        random_num = random.randint(1, 100)
        return f"{match.group(0)}{random_num}"

    # Use re.sub to find every instance and apply the function
    # re.escape ensures special characters in target_sub don't break the regex
    result = re.sub(pattern, add_number, main_string)
    return result

def remove_random(main_string, target_sub):
    pattern = r"(" + "|".join(re.escape(word) for word in target_sub) + r")\d+"
    result = re.sub(pattern, r"\1", main_string)
    return result   



test_script =  "forever(move(10), say_for('banana', 5), set_var('my_var', 5))"

def copy_windows(text):
        subprocess.run("clip", input=text, check=True, encoding="utf-8")

def parse(input_string_var):
    substring_var = ["move", "say_for","set_var"]
    input_string_var_rand = insert_randoms(input_string_var,substring_var)
    # Parse the string into an Abstract Syntax Tree
    tree = ast.parse(input_string_var.strip(), mode='exec')
    rand_str_tree = ast.parse(input_string_var_rand.strip(), mode='exec')
    first_func:str = ""
    print("plain tree")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check if it's a simple Name call
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if not first_func:
                   first_func = func_name
                else:
                    print(f"The current Function is: {func_name}. The previous Function was: {first_func}.")
                    first_func = func_name
                    time.sleep(1)
    first_func = ""
    print("random string tree.")
    for node in ast.walk(rand_str_tree):
        if isinstance(node, ast.Call):
            # Check if it's a simple Name call
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if not first_func:
                   first_func = func_name
                else:
                    print(f"The current Function is: {func_name}. The previous Function was: {first_func}.")
                    first_func = func_name
                    time.sleep(1)
                
    # This walks through the entire tree and finds all function calls
    copy_windows("AST: "+ast.dump(tree, indent=4))

    # Inspect the AST structure (e.g., dump it to a readable format)
    print("coppied original tree to clipboard")
    time.sleep(1)
    unparsed = ast.unparse(rand_str_tree)
    print(f"""Plain unparse with random: 
    {unparsed}""")
    print("")
    time.sleep(1)
    idless_unparse = remove_random(unparsed, substring_var)
    print(f"""Unparsed string with random id removed via function, and not stored tree: 
    {idless_unparse}""")
    time.sleep(1)
    print("Press any key to exit...")
    msvcrt.getch()

def choice_logic():
    choice = input("1: use test or 2: enter your own: ")
    if choice == "1":
        parse(test_script)
    elif choice == "2":
        try:
                
            bindings = KeyBindings()

            # 2. Make the Tab key insert 4 spaces
            @bindings.add('tab')
            def _(event):
                event.current_buffer.insert_text('    ')
            print("Enter your text (Press Enter twice to submit):")
            session = PromptSession()
            lines = []

            final_input = session.prompt('> ', multiline=True)

            final_input = "\n".join(lines)
            parse(final_input)
            result = 10 / 0
        except Exception as general_error:
            # Code that catches any other unexpected error
            print(f"Something else went wrong: {general_error}")
            time.sleep(5)

    else:
         print("invalid input.")
         choice_logic()

choice_logic()
