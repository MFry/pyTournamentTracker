# pyTournamentTracker
### Tournament Tracker
Multi-tournament swiss-pairing tracker build on python.
# Table of Contents

*   [Quick Start](#first-time-start)
*   [Developer References](#references)
*   [Versions](#versions)
*   [Creators](#creators)
*   [Copyright and license](#copyright-and-license)

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
├── LICENSE
```
## References

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
*   [Python 3.5+](https://docs.python.org/3/whatsnew/3.5.html)
*   [PostgreSQL 9.5](https://wiki.postgresql.org/wiki/What's_new_in_PostgreSQL_9.5)

##Creators

Michal Frystacky

##Copyright and License
Code and documentation copyright 2016 Michal Frystacky. Code released under the [MIT license](https://github.com/MFry/pyTournamentTracker/blob/master/LICENSE).
