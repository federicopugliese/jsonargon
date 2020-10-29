import os
import shutil
import subprocess
import sys

# Import the useful packages
try:
    import yaml
    from git import Repo
except ImportError:
    # Install the packages
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML==5.3.1", "gitpython==3.1.11"])
    import yaml
    from git import Repo


SOURCE = "src"
MAIN_BRANCH = "master"
ARCHETYPE_BRANCH_PREFIX = "archetype/"

PROJECT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
SOURCE_FOLDER = os.path.join(PROJECT_FOLDER, SOURCE)
ARCHETYPE_FOLDER = os.path.join(SOURCE_FOLDER, "archetype")
GENERATE_FILE = os.path.join(PROJECT_FOLDER, "generate.yml")

# Create this repo reference
repo = Repo(PROJECT_FOLDER)


def main():

    # Get configuration file
    config = get_config()

    # Generate all specified modules
    try:

        # For each specified module, generate from its archetype
        for module, specifications in config[SOURCE].items():
            generate(module, specifications["archetype"], specifications["config"])

        # Clean the branches (remove all the archetype branches)
        clean_branches()

    except Exception as e:

        # Remove all the generated files
        for filename in os.listdir(SOURCE_FOLDER):
            filepath = os.path.join(SOURCE_FOLDER, filename)
            if os.path.isdir(filepath):
                shutil.rmtree(filepath)

        # Get back to the correct branch
        repo.git.checkout(MAIN_BRANCH)
        raise e

    # Auto-remove this file and yml
    print("Success! Deleting generate.py and generate.yml...")
    os.remove(os.path.realpath(__file__))
    os.remove(GENERATE_FILE)
    print("Done.")


def clean_branches():

    # Sanity check - NEVER delete the branches from the project archetype itself!
    is_original_archetype = [url for url in repo.remote().urls if "mlreply/project-archetype.git" in url]
    if not is_original_archetype:

        # Remove all remote archetype branches
        for branch in repo.remote().refs:
            name = branch.remote_head
            if name.startswith(ARCHETYPE_BRANCH_PREFIX):
                repo.remote().push(":{}".format(name))

        # Remove local archetype branches
        archetypes = [branch for branch in repo.heads if branch.name.startswith(ARCHETYPE_BRANCH_PREFIX)]
        repo.delete_head([archetypes], force=True)

    else:

        raise PermissionError("You were trying to delete all the branches from the original archetype! "
                              "You have to fork this repository, not use it directly!")


def generate(module, archetype, config):

    print("---- Generating {} (archetype: {})".format(module, archetype))
    # Move to the correct branch
    repo.git.checkout(ARCHETYPE_BRANCH_PREFIX + archetype)

    # Generate the archetype
    params = ["--{}={}".format(key, value) for key, value in config.items()]
    subprocess.check_call([sys.executable, "generate.py", *params], cwd=ARCHETYPE_FOLDER)

    # End the generation by renaming the module folder
    module_folder = os.path.join(SOURCE_FOLDER, module)
    os.rename(ARCHETYPE_FOLDER, module_folder)

    # Move back
    repo.git.checkout(MAIN_BRANCH)


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
