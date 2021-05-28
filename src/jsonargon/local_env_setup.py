import glob
import os
import re
import subprocess
import sys
import urllib.request

COMPONENT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PACKAGE_FOLDER = os.path.join(COMPONENT_FOLDER, "package")
VERSION_FILE = os.path.join(PACKAGE_FOLDER, "python.cfg")
COMPONENT_NAME = os.path.basename(os.path.normpath(COMPONENT_FOLDER))

VENV_FOLDER = os.path.join(COMPONENT_FOLDER, "venv-" + COMPONENT_NAME)
VENV_TEMPLATE = "(" + ") || (".join(["{python_path} -m venv " + VENV_FOLDER,
                                     "virtualenv -p {python_path} " + VENV_FOLDER,
                                     "pip install virtualenv && virtualenv -p {python_path} " + VENV_FOLDER]) + ")"
VENV_UPDATE = "{activate_command} && pip install -e " + PACKAGE_FOLDER

HOME_FOLDER = os.path.expanduser("~")
PROGRAMS_DIR = os.path.join(HOME_FOLDER, "bin")

PYTHON_URL_TEMPLATE = "https://www.python.org/ftp/python/{version}/{installer_name}"


class PythonUtils(object):

    def __init__(self, version):
        self.version = version
        self.reduced_version = re.sub("\.[0-9]+$", "", self.version)
        self.python_dir = os.path.join(PROGRAMS_DIR, "Python-{version}".format(version=self.version))

    def _get_installer_name(self):
        raise NotImplementedError()

    def _get_python_path(self):
        raise NotImplementedError()

    def _install_python(self, python_dir, installer_path):
        raise NotImplementedError()

    def _get_venv_activate_command(self):
        raise NotImplementedError()

    def _is_python_installed(self):
        # Check the python version
        python_path = self._get_python_path()
        try:
            result = subprocess.run("{python_path} --version".format(python_path=python_path), check=False, capture_output=True)
            return True if result.returncode == 0 else False
        except FileNotFoundError:
            return False

    def _download_installer(self):
        # Get url to download installer from
        installer_name = self._get_installer_name()
        python_url = PYTHON_URL_TEMPLATE.format(version=self.version, installer_name=installer_name)

        # Make the installation folder
        python_dir = self.python_dir
        os.makedirs(python_dir, exist_ok=True)

        # Download the python installer
        installer_path = os.path.join(python_dir, installer_name)
        print("Downloading python from {url} to {installer}".format(url=python_url, installer=installer_path))
        urllib.request.urlretrieve(python_url, installer_path)
        print("Done.")
        return installer_path

    def install_if_not_installed(self):
        # Check the python version: if not installed, install it
        if self._is_python_installed():
            print("Python {} is already installed. Skipping installation".format(self.version))
        else:
            installer_path = self._download_installer()
            print("Installing python (this will require some time)...")
            self._install_python(self.python_dir, installer_path)
            print("Done.")

    def update_virtualenv(self):
        # Create the virtualenv if it does not exist
        if os.path.exists(VENV_FOLDER):
            print("Virtualenv already exists")
        else:
            # Create the virtualenv with the template command
            print("Creating the virtual environment...")
            python_path = self._get_python_path()
            subprocess.run(VENV_TEMPLATE.format(python_path=python_path), check=True, shell=True)

        # Install requirements
        print("Installing requirements...")
        activate_command = self._get_venv_activate_command()
        subprocess.run(VENV_UPDATE.format(activate_command=activate_command), check=True, shell=True)
        print("Done.")


class WindowsPythonUtils(PythonUtils):

    WINDOWS_COMMAND_TEMPLATE = "{installer_path} /quiet TargetDir={python_dir} InstallAllUsers=0 Include_launcher=0 InstallLauncherAllUsers=0 Include_test=0 Shortcuts=0"

    def _get_installer_name(self):
        is_64_bit = sys.maxsize > 2 ** 32
        installer_template = "python-{version}-amd64.exe" if is_64_bit else "python-{version}.exe"
        return installer_template.format(version=self.version)

    def _get_python_path(self):
        python_path = os.path.join(self.python_dir, "python.exe")
        return sanitize_path(python_path)

    def _is_python_installed(self):
        # If not installed, check that there is no another patch version with the same <major.minor>
        is_installed = super()._is_python_installed()
        if not is_installed:
            print("Python {} required by the package is not installed with this tool, but let's check for a compatible version.".format(self.version))

            # Check the current python
            python_path = sanitize_path(sys.executable)
            result = subprocess.run("{python_path} --version".format(python_path=python_path), check=False, capture_output=True)
            existing_version = re.sub("[^0-9\.]", "", result.stdout.decode("utf-8"))
            if result.returncode == 0 and self.reduced_version in existing_version:
                # If the (reduced) version is correct, update the python dir
                print("You are launching with an acceptable version of Python ({existing_version}). "
                      "Windows cannot install new versions that share the same <major.minor>.".format(existing_version=existing_version))
                python_dir, _ = os.path.split(sys.executable)
                self.version = existing_version
                self.python_dir = python_dir
                return True

            # Check the previously installed python version with this script
            search_path = "Python-{reduced_version}.*".format(reduced_version=self.reduced_version)
            old_versions = glob.glob(os.path.join(PROGRAMS_DIR, search_path, "python.exe"))
            if old_versions:
                # Pick the first matching version
                folder = old_versions[0]
                existing_version = folder.split("/")[-2].split("-")[-1]
                print("Another version of the same <major.minor> Python exists ({existing_version}). "
                      "Windows cannot install the new one. You will use the old one.".format(existing_version=existing_version))
                # Update the versions
                self.version = existing_version
                is_installed = True
        return is_installed

    def _install_python(self, python_dir, installer_path):
        # Execute the installation command
        command = self.WINDOWS_COMMAND_TEMPLATE.format(installer_path=installer_path,
                                                       python_dir=python_dir)
        subprocess.run(command, check=True)

    def _get_venv_activate_command(self):
        return "call " + os.path.join(VENV_FOLDER, "Scripts", "activate.bat")


class UnixPythonUtils(PythonUtils):

    UNIX_COMMAND_TEMPLATE = " && ".join(["tar -xvzf {installer_path}",
                                         "rm {installer_path}",
                                         "cd {python_dir}",
                                         "./configure --prefix {home} && make && make altinstall"])

    def _get_installer_name(self):
        return "Python-{version}.tgz".format(version=self.version)

    def _get_python_path(self):
        python_exe = "python${reduced_version}".format(reduced_version=self.reduced_version)
        python_path = os.path.join(self.python_dir, python_exe)
        return sanitize_path(python_path)

    def _install_python(self, python_dir, installer_path):
        # Execute the installation command
        command = self.UNIX_COMMAND_TEMPLATE.format(installer_path=installer_path,
                                                    python_dir=python_dir,
                                                    home=HOME_FOLDER)
        subprocess.run(command, check=True, shell=True)

    def _get_venv_activate_command(self):
        return "source " + os.path.join(VENV_FOLDER, "bin", "activate")


def sanitize_path(path):
    # Double quote the path in case of spaces
    return "\"{}\"".format(path) if " " in path else path


def get_python_utils():

    # Get the version
    with open(VERSION_FILE) as f:
        version = f.read()

    # Get the OS abstraction
    os_name = os.name
    if os_name == "nt":  # Windows
        python_utils = WindowsPythonUtils(version)
    elif os_name == "posix":  # Unix
        python_utils = UnixPythonUtils(version)
    else:
        raise Exception("Operating System of type {} not supported.".format(os_name))

    return python_utils


if __name__ == '__main__':

    # Get python utils according to OS
    python_utils = get_python_utils()

    # Install python version if not already installed
    python_utils.install_if_not_installed()

    # Create the virtualenv (if not already done)
    python_utils.update_virtualenv()

