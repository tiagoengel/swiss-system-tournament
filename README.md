Udacity Tournament Results
==

> Python implementation of a Swiss-system tournament

## Prerequisites
To execute this project you will need these:
- [git](https://git-scm.com/downloads)
- [vagrant](https://www.vagrantup.com)

## Usage

Clone the project:

```shell
git clone https://github.com/tiagoengel/swiss-system-tournament
cd swiss-system-tournament
```

Create and log into the vagrant vm:

```shell
cd vagrant
vagrant up
vagrant ssh
```

Once you are inside the vm, create the database and run the tests.
```shell
cd /vagrant
psql -f tournament/tournament.sql
python tournament/tournament_test.py
```