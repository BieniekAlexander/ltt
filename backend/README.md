# Introduction
Backend


# Setup
## Development Environment Setup
### Adding project packages to the PYTHONPATH
```
#!/bin/bash
if [ -z ".env" ] ; then #TODO what's the flag for this condition?
  PYTHONPATH="$(pwd)/backend/"
  echo "PYTHONPATH=\$PYTHONPATH" > .env
fi
```

### For CLI development: export the PYTHONPATH
```
source .env
```


### For VSCode: supply the PYTHONPATH


# Running
## Preconditions
- mongodb running

## Running the Server
```
flask run --port=8000	# run the server
```
