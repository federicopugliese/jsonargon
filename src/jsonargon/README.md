# Python Archetype


## Usage

Follow these instructions only after you have run the generate script.

- After having cloned the repository for the first time, 
launch `python local_env_setup.py`.
**See [Troubleshooting](troubleshooting) if anything goes wrong!**
    - This script will download the right python version, 
    create the virtual environment, activate it and install the dependencies and your package in
    development mode, so that you can import your modules from anywhere **in this virtual environment**, 
    e.g. as `from yourpackagename.yourmodule import yourfunction`, without modifying the `PYTHONPATH`.
- To activate the virtualenv, use `venv\Scripts\activate` on Windows or `source venv/bin/activate` on Linux/Mac.
    - This will make you use the right `python` with your package and dependencies.
- Write your code inside the `package/<yourpackagename>` folder. 
    - This will ensure that your code can be easily distributed and deployed. **Remember to add an `__init__.py` file in
    each submodule!** 
- To install (or uninstall) a package, use `python mpip.py` instead of normal `pip`.
    - This will ensure that you manage your packages inside your virtualenv and **it will force your** `requirements.txt`
    **file to be always up to date**.
    - If you need to exclude some requirements from this mechanism, add them to the list in `mpip.py` at line 36.
- Each time one of your collaborators adds a dependency, you will see a change in your `requirements.txt` file on Git. 
Simply launch again `python local_env_setup.py` to update your dependencies. 
    - **The script will just update the missing dependencies**. There are particular cases where this might lead to conflicts:
    please consider destroying your virtualenv first, and then launch `local-env-setup` again.
- To distribute your code as a real package, you can build a `tar.gz` or a `wheel`.
    - To create a **source distribution** with `tar.gz` format, move inside the `package` directory, 
    where `setup.py` is located, and issue `python setup.py sdist`.
        - This will create a `tar.gz` inside a `package/dist` folder. You can manage your versions
        changing the `0.0.0` in `setup.py`.
    - To create a **built distribution** in `whl`, issue `python setup.py bdist_wheel`.
- You can put non-code files that have to be read anyway by your code inside the `resources` folder (e.g. configurations).
    - This will ensure that these **file are accessible even when you distribute your package.**
    - To access the file, use `os.path.join(RESOURCES_LOCATION, "<path>", "<to>", "<file>")` 
        - Example: `os.path.join(RESOURCES_LOCATION, "readme.txt")`
        - Of course you have to `import os` and `from <yourpackagename> import RESOURCES_LOCATION`.
- You can put scripts to manage your code (e.g. deployment) inside the `devops` folder.
- You can also put tests inside the `package/tests` folder.
- Use the logging functionality to write logs
    - This provides a way to **configure output messages once, in a centralized manner**. You can see it on `__init__.py` file,
    on `_init_logger()` function.
        - Example: multiple forked processes writing on the same handler or both on `stdout` and on log files.
```
import logging

logger = logging.getLogger(__name__)

...

logger.info("Message")
logger.error("This is an error")
```


## Troubleshooting

If Python installation has some issues on Linux, make sure you have the mandatory dependencies by running this command:

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl libncurses5-dev libncursesw5-dev \
xz-utils libffi-dev liblzma-dev python-openssl
```

then, run again the installation.


If Packages installation (such as Tensorflow) has some issues on Windows, follow this instruction if you suspect 
that the error is related to a very long path: 

https://docs.python.org/3.7/using/windows.html#removing-the-max-path-limitation