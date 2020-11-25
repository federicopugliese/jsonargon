# Project Archetype

Use this archetype to start with your project. **You must have Python >= 3.7.0 installed on your machine 
([click here to download](https://www.python.org/downloads/release/python-374/))**, even if you will not use a Python project.

1. Import this repository into a new one (***DO NOT FORK***)
1. Clone the resulting repository onto your machine
1. Follow the customization instructions


## Customization

**Please check your python version**. If your `python --version` command gives you a wrong Python, find the path to the
right one on your file system and use it directly (e.g. `/path/to/python ...`).

The Project Archetype is simple: **the first time you create your repository**, you have to:

1. Modify the `generate.yml` file to add all your modules. You can find an example in the Archetypes section of this README.
3. Run `generate.py` with the following command. 

```
python generate.py
```

If you run on any issue, please refer to the specific `src/archetype/README.md` on the `archetype/<archetype>` branch. 

This will generate a module (a folder) in the `src` directory for each entry specified in the `generate.yml`. 
This is useful when your project requires more than a package or component, e.g. frontend and backend and so on.

For instance, you can have multiple Python packages with different virtualenvs.

The `generate.py` will also commit and push for you


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
  ...
  backend:
    archetype: python
    config:
      package: mailer
      description: "A package to manage mails"
      python-version: 3.7.4
  ...
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
