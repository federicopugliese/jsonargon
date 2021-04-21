# Project Archetype

Use this archetype to either:

1. Start with a new project
1. Add new components to your project


## Start with your project

**You must have Python >= 3.7.0 installed on your machine 
([click here to download](https://www.python.org/downloads/release/python-374/))**, even if you will not use a Python project.

1. Create a new repo from this one. You have two ways - the first one is strongly suggested:
    1. Go to https://bitbucket.org/mlreply/project-creator/addon/pipelines/home and "Run Pipeline" from "master". Select the right one (at least "bitbucket").
    1. OR import this repository into a new one (***DO NOT FORK***)
        1. Click on the + on the left, under `IMPORT` select "Repository"
        1. Copy the clone link: https://bitbucket.org/mlreply/project-archetype.git
        1. Flag "requires authorization" and insert your credentials
1. Clone the resulting repository onto your machine
1. Be sure that you can `git pull` without asking your password
    1. If it asks for your password:
        1. Windows: run `git config credential.helper wincred`
        1. Unix: run `git config credential.helper cache`
        1. Try with `git pull` twice; the first time it might ask for your password, the second one it should not.
1. Follow the customization instructions


### Customization

**Please check your python version**. If your `python --version` command gives you a wrong Python, find the path to the
right one on your file system and use it directly (e.g. `/path/to/python ...`).

The Project Archetype is simple: **the first time you create your repository**, you have to:

1. Modify the `generate.yml` file to add all your modules. You can find an example in the Archetypes section of this README.
1. Run `generate.py` with the following command. 
1. Open and merge a Pull Request in Bitbucket from `feat/modules` to `dev` (closing the first branch).

```
python generate.py
```

If you run on any issue, please refer to the specific `src/archetype/README.md` on the `archetype/<archetype>` branch. 

This will generate a module (a folder) in the `src` directory for each entry specified in the `generate.yml`. 
This is useful when your project requires more than a package or component, e.g. frontend and backend and so on.

For instance, you can have multiple Python packages with different virtualenvs.


## Add new components to your project

1. On your computer, create a temporary `generate.yml` file
    1. Fill it with the new components you want, according to the Archetypes section of this README
1. Open the git bash where `generate.yml` is located
    1. Run `cat generate.yml | base64 -w0`
    1. Copy the output (with no trailing spaces!)
1. Go to https://bitbucket.org/mlreply/project-archetype/addon/pipelines/home
    1. Select "Run Pipeline" and choose branch "master"
    1. Select pipeline "custom: generate-components"
    1. Paste the copied output of previous step in `GENERATE_YML_BASE64`
    1. Run the pipeline (in case of errors, open the `source ./devops/pipelines/generate.sh` on the right to check)
1. Once the pipeline has succeeded, move to the Artifacts tab on the right
    1. Download the zip named `src/**`
    1. Open it (typically with right click -> 7zip -> open) or extract it
    1. Pick the content of the inner `src` folder. It will have the folders of your modules!

## Archetypes

You can have multiple modules in your project, each one with a different archetype. 

When you run the generate script, this will call the specific archetype's generate script. This script will change all the placeholders in this archetype with the names you need and it will delete itself, since
it is not required anymore.

The following archetypes are supported, with their config to add in the `generate.yml`:

### Python

This archetype is used to build a generic Python package.

It has support for Docker.

```
src:
  ...
  <modulename>:
    archetype: python
    config:
      package: <packagename>
      description: "<Your package description>"
      python-version: <python complete version, e.g. 3.7.4>
  ...
```

Example:

```
src:

  backend:
    archetype: python
    config:
      package: mailer
      description: "A package to manage mails"
      python-version: 3.7.4

```

The module name might be the same as the package name. This is simply the name of the folder containing all the required code to work with your package.

The package name must be lower case, without underscores 
(see guidelines [PEP8](https://www.python.org/dev/peps/pep-0008/#package-and-module-names)).

It will also save the required python version for your package in `package/python.cfg`. ***NEVER 
ALTER THIS FILE IF YOU DO NOT NEED TO CHANGE YOUR REQUIRED VERSION OF PYTHON.***


### Flask

This archetype is used to build a Python package running Flask.

It has support for Gunicorn and Docker as well.

```
src:
  ...
  <modulename>:
    archetype: flask
    config:
      package: <packagename>
      description: "<Your package description>"
      python-version: <python complete version, e.g. 3.7.4>
  ...
```

Please refer to the Python archetype for details on the fields.


### Demo Flask

This archetype is used to build a demo by MLReply, i.e. a Python package running Flask, with a standard frontend and a backend.

It has support for Google Cloud.

```
src:
  ...
  <modulename>:
    archetype: demo-flask
    config:
      package: <packagename>
      description: "<Your package description>"
      python-version: <python complete version, e.g. 3.7.4>
      gcp-project: <Google Cloud project id where the demo will run, e.g. mlr-demo-something>
      input: {text,image,video}
      output: {text,image,video} 
  ...
```

Input and output will be used to create a custom frontend to managed the demo input and output; the GCP project is the one created to host the demo.

Please refer to the Flask archetype for details on the other fields.
