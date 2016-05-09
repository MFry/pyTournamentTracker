# pyTournamentTracker
### Tournament Tracker
Multi-tournament swiss-pairing tracker build on python.
# Table of Contents

    *   [Quick Start](#quick-start)
    *   Developers 
    *   Versions
    
### Dependencies

### First Time Start
```
vagrant up
vagrant ssh  
```
<a name="quick-start"></a>Once you are logged into the vm
``` bash
source /vagrant/tournament/virtualenv/bin/activate
cd /vagrant/tournamnet/
make -f Makefile
python sample_run.py    
```

### What's included

```
pyTournamentTracker/
├──vagrant/
|   ├── tournament/
|   |   ├── __init__.py
|   |   ├── Makefile
|   |   ├── requirements.txt
|   |   ├── sample_run.py
|   |   ├── test_basic.py
|   |   ├── tournament.py
|   |   ├── tournament.sql
|   ├── postgresql_provisions.sh
|   ├── provision.sh
|   ├── python_provisions.sh
```

#### Source Folder

``` bash
cd /vagrant/tournament/
```

#### Activate Virtual Environment

``` bash
source /vagrant/tournament/virtualenv/bin/activate
```

#### Python dependencies

``` bash
make -f Makefile
```

### Run Test
```bash
python test_basic.py
```

### Run Sample Code
```bash
python sample_run.py
```

## Versions
The provided vagrant VM takes care of all the project dependencies such as:
*   Python 3.5+
*   PostgreSQL 9.5