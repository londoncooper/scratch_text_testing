import ast
import time
import subprocess
import re
import random

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


test_script =  "forever(move(10), say_for('banana', 5))"

def copy_windows(text):
        subprocess.run("clip", input=text, check=True, encoding="utf-8")

def parse():
    code_str = input("Give line of scratch text: ")
    substring_var = ["move", "say_for"]
    code_str = insert_randoms(code_str,substring_var)
    # Parse the string into an Abstract Syntax Tree
    tree = ast.parse(code_str.strip(), mode='eval')
    first_func:str = ""

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check if it's a simple Name call
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if not first_func:
                   first_func = func_name
                else:
                    print("The current Function is: "+func_name+". The previous Function was: "+first_func+".")
                    first_func = func_name
                
    # This walks through the entire tree and finds all function calls
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]

    #print(str(functions))
    copy_windows("AST: "+ast.dump(tree, indent=4))

    # Inspect the AST structure (e.g., dump it to a readable format)
    print("coppied to clipboard")
    unparsed = ast.unparse(tree)
    print("Plain unparse: "+unparsed)
    print("")
    print("Unparsed string with random id removed: "+ remove_random(unparsed, substring_var))
    time.sleep(5)

def choice_logic():
    choice = input("p or up: ")
    if choice.lower() == "p":
        parse()
    elif choice.lower() == "up":
        pass
    else:
         print("invalid input.")
         choice_logic()

parse()