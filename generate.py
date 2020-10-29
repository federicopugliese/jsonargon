import os
import shutil
import subprocess
import sys

# Import the yaml module
try:
    import yaml
except ImportError:
    # Install the yaml interpreter
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML==5.3.1"])
    import yaml


SOURCE = "src"
MAIN_BRANCH = "master"

PROJECT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
SOURCE_FOLDER = os.path.join(PROJECT_FOLDER, SOURCE)
ARCHETYPE_FOLDER = os.path.join(SOURCE_FOLDER, "archetype")
GENERATE_FILE = os.path.join(PROJECT_FOLDER, "generate.yml")


def main():

    # Get configuration file
    config = get_config()

    # Generate all specified modules
    try:

        # For each specified module, generate from its archetype
        for module, specifications in config[SOURCE].items():
            generate(module, specifications["archetype"], specifications["config"])

    except Exception as e:

        # Remove all the generated files
        for filename in os.listdir(SOURCE_FOLDER):
            filepath = os.path.join(SOURCE_FOLDER, filename)
            if os.path.isdir(filepath):
                shutil.rmtree(filepath)

        # Get back to the correct branch
        git_checkout(MAIN_BRANCH)
        raise e

    # Auto-remove this file and yml
    print("Success! Deleting generate.py and generate.yml...")
    os.remove(os.path.realpath(__file__))
    os.remove(GENERATE_FILE)
    print("Done.")


def git_checkout(branch):
    subprocess.check_call(["git", "checkout", branch], cwd=PROJECT_FOLDER)


def generate(module, archetype, config):

    # Move to the correct branch
    git_checkout("archetype/" + archetype)

    # Generate the archetype
    params = ["--{}={}".format(key, value) for key, value in config.items()]
    subprocess.check_call([sys.executable, "generate.py", *params], cwd=ARCHETYPE_FOLDER)

    # End the generation by renaming the module folder
    module_folder = os.path.join(SOURCE_FOLDER, module)
    os.rename(ARCHETYPE_FOLDER, module_folder)

    # Move back
    git_checkout(MAIN_BRANCH)


def get_config():

    # Read the generate file and call the corresponding actions
    with open(GENERATE_FILE, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    # Check configurations
    if not config[SOURCE]:
        raise ValueError("No configurations provided in generate.yml file!")
    return config


if __name__ == '__main__':

    main()
