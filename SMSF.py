import subprocess
import sys
import os
import re

sys.stdout.reconfigure(line_buffering=True)

def search_exploits(search_term):
    result = subprocess.run(['searchsploit', search_term], capture_output=True, text=True)
    return result.stdout.strip()

def contains_metasploit(exploits):
    for exploit in exploits:
        if "metasploit" in exploit.lower():
            return True
    return False

def open_msfconsole_with_exploit(exploit_name):
    os.system(f"msfconsole -q -x 'search {exploit_name};'")
    sys.exit(1)

def get_exploit_details(exploit_number, exploits_list):
    try:
        exploit_line = exploits_list[exploit_number - 1].strip().split()
        return {'path': os.path.join('/usr/share/exploitdb/exploits', exploit_line[-1]), 'language': exploit_line[-2]}
    except IndexError:
        print("Invalid exploit number.")
        sys.exit(1)

def get_input_instructions(exploit_path):
    try:
        with open(exploit_path, 'r') as file:
            content = file.read()

            regex_pattern = r'Use:.*\n'
            regex_input_instructions = re.findall(regex_pattern, content, re.IGNORECASE)

            input_instructions = []
            for instruction in regex_input_instructions:
                if instruction.strip():
                    input_instructions.append(instruction.strip())

            return input_instructions

    except FileNotFoundError:
        print("Exploit file not found.")
        sys.exit(1)

def create_output_directory():
    output_directory = os.path.join(os.getcwd(), 'Exploits')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory

def copy_exploit_to_local(exploit_path, output_directory):
    output_file = os.path.join(output_directory, os.path.basename(exploit_path))
    try:
        import shutil
        shutil.copy2(exploit_path, output_file)
        print(f"Exploit successfully copied to {output_file}")
    except FileNotFoundError:
        print("Error: Exploit file not found.")
        sys.exit(1)

def main():
    try:
        os.system('clear')
        print("""
███████╗███╗   ███╗███████╗███████╗
██╔════╝████╗ ████║██╔════╝██╔════╝
███████╗██╔████╔██║███████╗█████╗  
╚════██║██║╚██╔╝██║╚════██║██╔══╝  
███████║██║ ╚═╝ ██║███████║██║     
╚══════╝╚═╝     ╚═╝╚══════╝╚═╝     
   ----Sploity McSploitFace----    """)
        output_directory = create_output_directory()

        search_term = input("Enter a search term: ")
        exploits = search_exploits(search_term).split('\n')[3:-3]
        print("\nSearch results:\n")
        for i, exploit in enumerate(exploits, start=1):
            print(f"{i}. {exploit.strip()}")

        if contains_metasploit(exploits):
            open_metasploit = input("\nMetasploit module found. Do you want to open Metasploit (y/n)? ")
            if open_metasploit.lower() == 'y':
                open_msfconsole_with_exploit(search_term)

        exploit_number = int(input("\nEnter the exploit number: "))
        exploit_details = get_exploit_details(exploit_number, exploits)
        input_instructions = get_input_instructions(exploit_details['path'])

        if input_instructions:
            print("\nInput instructions:")
            for instruction in input_instructions:
                print(instruction.strip())

        copy_choice = input("\nDo you want to copy the exploit to the local Exploits folder (y/n)? ")
        if copy_choice.lower() == 'y':
            copy_exploit_to_local(exploit_details['path'], output_directory)

    except KeyboardInterrupt:
        print("\nUser interrupted the process.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

