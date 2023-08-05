### Python Build Utilities

![Python Package using Conda](https://github.com/psilons/pypigeonhole-build/workflows/Python%20Package%20using%20Conda/badge.svg)
![Test Coverage](coverage.svg)
[![PyPI version](https://badge.fury.io/py/pypigeonhole-build.svg)](https://badge.fury.io/py/pypigeonhole-build)
![Anaconda version](https://anaconda.org/psilons/pypigeonhole-build/badges/version.svg)
![Anaconda_platform](https://anaconda.org/psilons/pypigeonhole-build/badges/platforms.svg)
![License](https://anaconda.org/psilons/pypigeonhole-build/badges/license.svg)

This is a Python SDLC tool to shorten the time we spend on SDLC without
sacrificing quality. It does so by hard-coding certain parts. Freedom could
lead to confusion and low efficiency. We borrow the idea from Java's mature
tool, [Maven](http://maven.apache.org/).

Our goals are:

- Make simple/routine steps efficient
- Make out of routine steps possible, i.e., our code should not add more
  hassle when you expand it.

A sample project is in a separate repo: 
[Project Template](https://github.com/psilons/pypigeonhole-proj-tmplt)

#### This library does the following:

- Hard code src and test folders for source code and testing code. 
>We don't think the freedom naming of these 2 folders help us anything.

>We want to separate src and test completely, not one inside another.

- For applications, we hard code bin folder for start-up and other scripts.
  We hard code conf folder for configurations.

- We isolate to one place to specify dependencies (along with the name and
  version), this place is src
To avoid duplicated dependency information in setup.py and Anaconda 
environment.yaml.

Now we specify The dependencies in dep_setup.py. setup.py calls this to get the
needed info.

We also added scope to indicate whether dependencies are needed during runtime.

#### Usage
** *nix shell scripts are not fully tested! **

Add dependencies in the dep_setup.py. Each dependency has the following fields:
- name: required. If name == python, the "python_requires" field in the 
  setup.py will be touched.
- version: default to latest. Need full format: '==2.5'
- scope: default to DEV, could be DEV/INSTALL. INSTALL dependencies show in the
  "install_requires" field. DEV dependencies show up in the "test_require" 
  field.
- installer: default to PIP, could be PIP/CONDA. Extendable to other 
  installers.
- url: this is for github+https.

If Conda is used, need to set the CONDA.env field, which is mapped to the first
line in the environment.yaml. CONDA.channels can be alternated too (default to
None).

Pip can be customized in setup.py, so no change. 

To generate environment.yaml, add src to PYTHONPATH and run

```python dep_setup.py conda```

To generate environment.txt, add src to PYTHONPATH and run

```python dep_setup.py pip```

This file is different from the one generated from pip, it does not have
dependent libraries.

To setup local dev environment, run 

```dbin\py_dev_env_setup```

This will create a new conda environment with the name specified in CONDA.env.
The old environment will be deleted.

There is a *nix port on windows,

```conda install conda-build unxutils```

We could use the tee command to save command output to logs.


For more info, see dep_setup.py and unit tests.
