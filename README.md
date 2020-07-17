# avato-tflite-dynamic

Python client library for TFLite dynamic instance of the Avato platform.

## Installation

After cloning the repository you can use different installation methods:

### Poetry

To install with poetry just run:
```
poetry install
```

#### Notes:

1. If you get an error during the installation try to delete the `poetry.lock` file

2. Poetry installs the library in its own virtualenv, if you want to use it in your
global python installation disable virtualenvs in poetry

```
poetry config settings.virtualenvs.create false
```

### Pip

To install with pip just run:

```
pip install .
```

## Usage:

To use the library just import the `avato` and `avato_tflite_dynamic` modules and start interacting with the platform!

**Example-1**: *instance creation*

``` python
from avato import Client
from avato_tflite_dynamic import TFLITEDYNAMIC_Instance

client = Client(
    api_token="SECRET_TOKEN",
    instance_types=[TFLITEDYNAMIC_Instance]
)
instance = client.create_instance(
    "genesis", TFLITEDYNAMIC_Instance.type, ["friend@decentriq.ch"]
)
client.get_instances()
instance.delete()
```

For more examples check out the `tests` directory


## Testing

To start the testing process install `nox` with `pip install nox` and the run it
in the project directory. *N.B. make sure you have an available avato-backend*

**nox**
```
nox
```
