# Bluetooth-p2p-folder-sync
A python script for syncing two folders in different systems via bluetooh peer to peer connection. A Third Year of Computer Science, of the subject Computer Networks project.

# Steps to run
```sh
cd /path/to/your/project
```

```sh
pyenv local 3.12.3
```

To isolate dependencies in your code, use `pyenv-virtualenv`:

**If not already installed**
```sh
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
```

**Reload your shell**
```sh
source ~/.bashrc  # or ~/.zshrc
```

**Create virutal environment**
pyenv virtualenv 3.12.3 my_project_env

**Set the virtual environment locally for the project**
```sh
pyenv local my_project_env
```

**Activate it**
```sh
pyenv activate my_project_env
```

**Run the project**

In your project folder do:
```sh
python3 main.py
```