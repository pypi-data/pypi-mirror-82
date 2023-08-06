# Paradox® HD77 Camera API

## Introduction

This is a python module that provides an interface for interacting with a Paradox® HD77 camera 
(and possibly other models).

This is licensed under the MIT license.

## Getting started

This API is not documented by Paradox®.

I used reverse engineering on the HD77 model (v1.25.7) to discover it and create the python functions to access it.

It does not work with the IP150 network module and has not yet been tested with other camera models.

I also discovered how to discover Paradox® devices on the network and created the code in the helpers folder 
(see the documentation below).

## Install

```python
pip install pypdxapi
```

## Quick Start

### API usage example

```python
import asyncio

from pypdxapi.camera import ParadoxHD77


async def main():
    """Show example of connecting to your Paradox HD77 camera."""
    async with ParadoxHD77(host='192.168.1.50', port=80, module_password='paradox') as hd77:
        hd77.login(usercode='1234', username='master')
        if hd77.is_authenticated():
            print(hd77.vod(action=1, channel_type='normal'))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### Discovery usage example

```python
from pypdxapi.helpers import discover_modules

modules = discover_modules()
```

For more information see docs.

## Disclaimer

The code was developed as a way of integrating personally owned Paradox® HD77 cameras and other modules, and it cannot 
be used for other purposes. It is not affiliated with any company and it doesn't have have commercial intent.

The code is provided AS IS and the developers will not be held responsible for failures in the camera, or any other 
malfunction.

Paradox® is a registered mark. Other brands are owned by their respective owners.