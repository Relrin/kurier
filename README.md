# kurier
A cross-platform GUI client for testing AMQP-based APIs

This application was written for my needs in developing and testing AMQP-based microservices, that will behave like the Postman application. For example, I'm using it for development microservices in the [Open Matchmaking](https://github.com/OpenMatchmaking) project.

# Features
- Postman-like client, but for using with AMQP-based APIs
- Validating queues, exchanges and routing keys for existing in the virtual host
- Saving and restoring valid requests from the history
- Search old requests in the history by the request exchange and the routing key

# Requirements
- Python >= 3.12
- wxPython >= 4.2

# Screenshots
<img src="https://github.com/Relrin/kurier/blob/master/screenshots/windows-app.png" width="400"> | <img src="https://github.com/Relrin/kurier/blob/master/screenshots/mac-app.png" width="425">
:----------------------------------------------------------------------------:|:-------------------------:
  Windows                                                                     | Mac OS X 

# Building an application
For building an executable for your OS you will need to do the following steps:

1) Install the Python 3. You can download the latest stable release of from [Python language website](https://www.python.org/) and install it manually or via other suitable package manager to you.
2) Clone the git repository on your local machine:
```bash
git clone https://github.com/Relrin/kurier.git
cd kurier
```  
3) Create a virtual environment for all our stuff:
- For **virtualenv** use this:
  ```bash
  virtualenv --python=`which python3` venv
  ```
- For standard python **venv**:
  ```bash
  python3 -m venv venv
  ```
- For **virtualenvwrapper**:
  ```bash
  mkvirtualenv --python=`which python3` venv
  ```
4) Activate the virtual environent:
- Windows
  ```bash
  ./venv/Scripts/activate
  ```
- Mac OS X
  ```bash
  source venv/bin/activate
  ```
5) Install the requirements:
```bash
pip install -r requirements.txt
pip install -r requirements-build.txt
```
6) And run the build from the root of the cloned repository
```bash
pyinstaller --clean --workpath=build/temp --distpath=build/dist --onefile --nowindowed --noconsole --name=Kurier ./kurier/main.py 
```
7) Get the prepared executable for your OS in the `build/dist` directory

**Note**: In the case of the error with virtual environments on Mac OS X that *"This program needs access to the screen. Please run with a Framework build of python, and only when you are logged in on the main display of your Mac."* you will need to build CPython with Framework support on OS X. For more information read [this](https://wiki.wxpython.org/wxPythonVirtualenvOnMac) article.

# License
The kurier project is published under BSD license. For more details read the [LICENSE](https://github.com/Relrin/kurier/blob/master/LICENSE) file.
