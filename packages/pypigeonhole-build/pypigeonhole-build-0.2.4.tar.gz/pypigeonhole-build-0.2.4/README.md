# Python Build Tools

![Python Package using Conda](https://github.com/psilons/pypigeonhole-build/workflows/Python%20Package%20using%20Conda/badge.svg)
![Test Coverage](coverage.svg)
[![PyPI version](https://badge.fury.io/py/pypigeonhole-build.svg)](https://badge.fury.io/py/pypigeonhole-build)
![Anaconda version](https://anaconda.org/psilons/pypigeonhole-build/badges/version.svg)
![Anaconda_platform](https://anaconda.org/psilons/pypigeonhole-build/badges/platforms.svg)
![License](https://anaconda.org/psilons/pypigeonhole-build/badges/license.svg)

**Linux version of shell scripts is not working yet.**

This is a Python SDLC tool to shorten the time we spend on SDLC without
sacrificing quality. It does so by hard-coding certain flexible parts. 
Flexibility could lead to confusion and low efficiency because there is
no standard and thus we cannot build tools on top of that to improve
efficiency. 

A good example for efficiency is Java's mature tool, [Maven](http://maven.apache.org/).


## Goals

- set up a standard project structure. 
- create reusable tools to minimize the necessary work for dependency management 
  and CI.
- Make routine steps efficient.
- Make out-of-routine steps not more painful, i.e., our code should not add 
  more hassle when you extend/modify it.
  
  
## Standard SDLC Process Acceleration

All scripts run in the project folder. Once Conda environment is created, 
run subsequent scripts in the environment as well (activate the environment).

- environment setup: ```pph_dev_env_setup.bat```
  >The existing conda environment with same env name will be deleted, and a new 
  environment will be created.
  
  >requirements.txt and environment.yaml are generated as well. Whenever 
  we change dependencies, we need to rerun this script to re-generate the 
  files.


- **coding**: We should spend most time on this. We leave out the IDE set up.
- compile: This is out of scope due to varieties, C/C++, PyInstaller, Cython, 
  or no compiling at all, etc. 
- unit test: ```pph_unittest.bat``` 
  >generate test coverage report and coverage badge.
  
  >The script is based on Python unittest package. You may create another 
  script for pytest or other packages.
  
  >In order to run test at the project root folder, we add a src reference in
  the __init__.py under test top package. Otherwise, tests can run only from
  the src folder.
  
  
- package: 
    - ```pph_package_pip.bat``` to pack Python libraries.
    - ```pph_package_conda.bat``` to pack both libraries and applications.
    - ```pph_pack_app_zip.bat``` to pack applications, include src, bin, and conf.
      Since this is a customized way, there is no associated upload tool and 
      users need to deal with uploading by themselves.
      
  The pip and zip output folder is dist, and the conda output folder is 
  dist_conda.
     
  Conda version is more flexible to customize because of the extra references to
  meta.yaml and build scripts. Please check conda-build documents.
- release: ```pph_release.bat``` to tag versions and bump the current version to the 
  next. 
  >We use major.minor.patch format in versions. The minor and patch 
  increments are single digit, bounded by 10. A major version with 81 
  minors/patches should be enough in normal cases. 
- upload: 
    - ```pph_upload_pip.bat``` to upload library to the pip central server.
    - ```pph_upload_pip_test.bat``` to upload library to the pip test central server.
    - ```upload.conda.bat``` to upload library to the conda central server.
  We leave out the complexity of local artifact server setup. Variations are:
    - local pip/anaconda channels, for testing.
    - http tunnel through local channels.
    - local/internal pip/anaconda official servers through vendor support.
    - remote pip/anaconda official/central servers through internet.
    - 3rd party vendors, such as Artifactory servers.
- install/deploy: 
    - lib installation: use pip and/or conda.
    - app deployment: conda can bundle scripts and Python code. So we use conda
      as the transport to deploy apps. 
      >There are many other ways, ground or cloud, to deploy apps, such as 
      kubernetes, Ansible, etc. We leave these out due to high available 
      customization (i.e., no predictable patterns).


## Usage

Add this project as one of the dependencies. The installation installs the
reusable scripts to <virtual env>\Scripts folder, in addition to the Python
code installed in <virtual env>\Lib\site_packages\pypigeonhole_build. The
Scripts folder should be in PATH so that we can call them. They assume we
are in the project folder. 

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

Pip can be customized in setup.py, if needed. This file can be reused except
the import and name in most cases.

Now we could follow the previous SDLC steps.

For any runs, we use ``` <script> 2>&1 | tee my.log ``` to save the log to
local file, since some commands clear command window screen, and so we lose 
screen prints.

A sample project is in a separate repo: 
[Project Template](https://github.com/psilons/pypigeonhole-proj-tmplt).
In fact, we set up this project in the same way mentioned here too.

For more info, see dep_setup.py and unit tests.

If these tools are not suitable, we just create other scripts local to the
project we work on. The existing scripts / Python code should not interfere
the extension.


## Side Notes and Future improvements

- Sometimes, windows is not stable due to locking. Rerun should work.
- package_data in setup.py is not supported (yet).
- dependency information is not populated to meta.yaml, used by conda-build
