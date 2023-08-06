# CTFdumper

### Dumps the Submissions from a CTFd website.

---
## Installation

1. Clone this repo.
2. `python3 setup.py install`

## Usage

### CLI

```
  ___  ____  ____  ____  _  _  _  _  ____  ____  ____
 / __)(_  _)(  __)(    \/ )( \( \/ )(  _ \(  __)(  _ \
( (__   )(   ) _)  ) D () \/ (/ \/ \ ) __/ ) _)  )   /
 \___) (__) (__)  (____/\____/\_)(_/(__)  (____)(__\_)


usage: ctfdumper [-h] [-t THREADS] [-u USERNAME] -o OUTPUT url

Dumps the submissions from a CTFD website

positional arguments:
  url                   the url for the CTFD site example
                        "https://demo.ctf.org"

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        the number of threads to use when dumping data
  -u USERNAME, --username USERNAME
                        the username to login as
  -o OUTPUT, --output OUTPUT
                        location to save the csv file of the submission data
```

### Within Python Script

```
from ctfdumper.ctfdumper import CTFDumper

dumper = CTFDumper(url, thread=num_of_threads)

# username and password are the credentials for login into the CTFd website
# returns a pandas DataFrame with all of the submissions

submissions = dumper.get_submissions(username, password)
```
