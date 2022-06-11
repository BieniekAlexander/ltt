# Introduction
The backend components for the Language Training Toolkit.


# Roadmap
## Goals
- Use remote MongoDB server
## Known Issues
- 


# Setup
## Python Environment Setup
```
#!/bin/bash
ENV_NAME=ltt

if [ -z "$(conda env list | grep $ENV_NAME)" ] ; then
  conda create --name $ENV_NAME python=3.9 -y
  conda activate $ENV_NAME
  pip install -r requirements.txt
else
  conda activate $ENV_NAME
fi
```

## Development Environment Setup
### Adding project packages to the PYTHONPATH
```
#!/bin/bash
if [ ! -s .env ] ; then
  PYTHONPATH="$(pwd)/src"
  echo "PYTHONPATH=$PYTHONPATH" > .env
fi
```

### For CLI development
```
#!/bin/bash
set -a
. .env
set +a
```

### For VSCode
1. Create a workspace settings.json
```
#!/bin/bash
if [ ! -s ../.vscode/settings.json ] ; then
  mkdir -p ../.vscode
  echo "{}" > ../.vscode
fi
```

2. Add the following lines to your workspace settings.json
```
...
"terminal.integrated.env.linux": {
    "PYTHONPATH": "${workspaceFolder}/backend/src"
},
"python.envFile": "${workspaceFolder}/backend/.env"
...
```


# Running
## Preconditions
- requires MongoDB instance for backend data

## Running the Server
```
#!/bin/bash
mongod &              # run the local MongoDB server 
flask run --port=8000 # run the server
```


# Testing
## Preconditions
- Conda environment setup and activated

## Run tests
```
pytest
```


# Notes
## Useful Links
- [Python Project Structure Guide](https://docs.python-guide.org/writing/structure/)
- [Pytest Documentation](https://docs.pytest.org/en/6.2.x/)
- [CLI usage for Running tests with pytest](https://zetcode.com/python/pytest/)
- [Conda environment management](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)