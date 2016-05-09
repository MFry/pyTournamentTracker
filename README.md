# pyTournamentTracker
### Tournament Tracker
Multi-tournament swiss-pairing tracker build on python.
## Usage
### First Time Start
```
vagrant up
vagrant ssh  
```
Once you are logged into the vm
``` bash
source /vagrant/tournament/virtualenv/bin/activate
cd /vagrant/tournamnet/
make -f Makefile
python sample_run.py    
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