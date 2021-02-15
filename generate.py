import os
import shutil
import subprocess
import sys

from pathlib import Path

try:
    # Import the useful packages
    import yaml
    from git import Repo
except ImportError:
    # Install the packages
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML==5.3.1", "gitpython==3.1.11"])
    import yaml
    from git import Repo


SOURCE = "src"
MAIN_BRANCH = "master"
FIRST_BRANCH = "feat/modules"
ARCHETYPE_BRANCH_PREFIX = "archetype/"
PIPELINES_BRANCH_PREFIX = "pipelines"

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
    os.path.join(DEVOPS_FOLDER, "pipelines"),
    os.path.join(DEVOPS_FOLDER, "tests")
]

# Create this repo reference
repo = Repo(PROJECT_FOLDER)


def main(test=False):

    # Get configuration file
    config = get_config()

    # Generate all specified modules
    try:

        # For each specified module, generate from its archetype
        for module, specifications in config[SOURCE].items():
            generate(module, specifications["archetype"], specifications["config"])

        # Clean the branches (remove all the archetype branches)
        clean_branches(test=test)

        # Create the first branch
        print("Creating the first commit...")
        repo.git.checkout(MAIN_BRANCH)
        branch = repo.create_head(FIRST_BRANCH)
        branch.checkout()
        repo.git.add("-A")
        repo.git.commit("-m", "First commit")
        origin = repo.remote()
        origin.push(FIRST_BRANCH)
        print("Done!")

        # Create PR
        repo_name = list(origin.urls)[0].split("/")[-1].split(".git")[0]  # get .../repo_name.git
        print(f"Create and merge a Pull Request from feat/modules to dev here: https://bitbucket.org/mlreply/{repo_name}/pull-requests/new")

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


def clean_branches(test=False):

    def is_to_be_cleaned(branch_name):
        return branch_name.startswith(ARCHETYPE_BRANCH_PREFIX) or branch_name.startswith(PIPELINES_BRANCH_PREFIX)

    # Sanity check - NEVER delete the branches from the project archetype itself!
    is_original_archetype = [url for url in repo.remote().urls if "mlreply/project-archetype.git" in url]
    if not is_original_archetype:

        # Remove all remote archetype branches
        print("Cleaning branches...")
        for branch in repo.remote().refs:
            name = branch.remote_head
            if is_to_be_cleaned(name):
                repo.remote().push(":{}".format(name))

        # Remove local archetype branches
        archetypes = [branch for branch in repo.heads if is_to_be_cleaned(branch.name)]
        repo.delete_head([archetypes], force=True)
        print("Done.")

    else:

        # Raise error (or just print a message in case of tests)
        error = "You were trying to delete all the branches from the original archetype! " \
                "You have to IMPORT this repository, not to use it directly!"
        if test:
            # Just print an error message
            print(error)
        else:
            raise PermissionError(error)


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
