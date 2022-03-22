<p align="center">
  <img src="https://github.com/tyler-conrad/flyeye/raw/master/demo.gif"/>
</p>

## How to install mlocate package

1. Install mlocate package

```shell
sudo apt-get update
sudo apt-get install mlocate
```

2. Update the search database
```shell
sudo updatedb
```

## Setup

3. Install Python3:
```shell
sudo pip install python3
```

4. Install Kivy:
  -  [Here](https://kivy.org/doc/stable/gettingstarted/installation.html)

## Usage

```shell
mlocate /home/tyler/Desktop | python3 main.py
```


Tested on:
- Ubuntu 20.04.3 LTS
- Kivy v2.0.0rc4, git-d74461b, 20201015
- Python 3.8.10 (default, Nov 26 2021, 20:14:08)