import argparse
import os
import re
import subprocess
from argparse import ArgumentParser


COMPONENT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
REQUIREMENTS_FILE = os.path.join(COMPONENT_FOLDER, "package", "requirements.txt")
COMPONENT_NAME = os.path.basename(os.path.normpath(COMPONENT_FOLDER))
VENV_FOLDER = os.path.join(COMPONENT_FOLDER, "venv-"+COMPONENT_NAME)

VENV_UPDATE = "{activate_command} && pip "
FREEZE_COMMAND = "{activate_command} && pip freeze"


def get_venv_activate_command():

    # Get the OS abstraction
    os_name = os.name
    if os_name == "nt":  # Windows
        command = "call " + os.path.join(VENV_FOLDER, "Scripts", "activate.bat")
    elif os_name == "posix":  # Unix
        command = "source " + os.path.join(VENV_FOLDER, "bin", "activate")
    else:
        raise Exception("Operating System of type {} not supported.".format(os_name))

    return command


def is_valid_requirement(requirement):

    # List of requirements to filter out
    forbidden_requirements = [
        "pkg-resources",
        "^-e",
        "pywin32",
        "pywinpty"
    ]
    forbidden_match = "(" + ")|(".join(forbidden_requirements) + ")"

    # Check if there is one match
    return not re.match(forbidden_match, requirement)


if __name__ == '__main__':

    # Parse the command line arguments
    parser = ArgumentParser()
    parser.add_argument("parameters", metavar="param", nargs=argparse.REMAINDER, help="Pip parameters.")
    args = parser.parse_args()

    # Invoke pip with parameters
    activate_command = get_venv_activate_command()
    pip_command = VENV_UPDATE.format(activate_command=activate_command) + " ".join(args.parameters)
    subprocess.run(pip_command, check=True, shell=True, cwd=os.getcwd())

    # Freeze requirements
    freeze_command = FREEZE_COMMAND.format(activate_command=activate_command)
    result = subprocess.run(freeze_command, check=True, shell=True, capture_output=True)

    # Parse requirements in a list
    output = result.stdout.decode("utf-8")
    requirements = re.sub("[\r\n]+", "\n", output).split("\n")
    print(requirements)

    # Get real requirements and update the requirements.txt file
    real_requirements = [req for req in requirements if is_valid_requirement(req)]
    with open(REQUIREMENTS_FILE, "w") as f:
        for requirement in real_requirements:
            f.write(requirement + "\n")
