import os
import shutil
import subprocess
import sys

# Import the useful packages
from pathlib import Path

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
DEVOPS_FOLDER = os.path.join(PROJECT_FOLDER, "devops")
GENERATE_FILE = os.path.join(PROJECT_FOLDER, "generate.yml")
BITBUCKET_FILE = os.path.join(PROJECT_FOLDER, "bitbucket-pipelines.yml")

ARCHETYPE_FILES = [
    os.path.realpath(__file__),
    GENERATE_FILE,
    BITBUCKET_FILE,
    os.path.join(DEVOPS_FOLDER, "branches"),
    os.path.join(DEVOPS_FOLDER, "pipelines")
]

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
    print("Success! Deleting archetype files...")
    clean_files()
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


def clean_files():

    # Remove files used for the archetype
    for file in ARCHETYPE_FILES:
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

    # Create a blank pipeline
    Path(os.path.join(PROJECT_FOLDER, "bitbucket-pipelines.yml")).touch()


def generate(module, archetype, config):

    print("---- Generating {} (archetype: {})".format(module, archetype))
    # Move to the correct branch
    repo.git.checkout(ARCHETYPE_BRANCH_PREFIX + archetype)

    # Generate the archetype
    try:
        params = ["--{}={}".format(key, value) for key, value in config.items()]
        params.append("--modulename="+module)
        subprocess.check_call([sys.executable, "generate.py", *params], cwd=ARCHETYPE_FOLDER)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Error during generation. Look before the 'CalledProcessError' "
                           "in this log to see the real error!") from e

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
