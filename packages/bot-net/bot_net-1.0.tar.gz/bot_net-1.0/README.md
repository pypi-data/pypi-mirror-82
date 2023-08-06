---
description: >-
  Bot-Net is one of the most useful, powerful and complete offensive
  penetration testing tool
---

# Bot-Net

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://raw.githubusercontent.com/FabrizioFubelli/Bot-Net/master/LICENSE) [![Docker Pulls](https://img.shields.io/docker/pulls/offensive/Bot-Net.svg)](https://hub.docker.com/r/offensive/Bot-Net)

![](https://raw.githubusercontent.com/offensive-hub/Bot-Net/master/resources/Bot-Net.jpg)

## Offensive penetration testing tool \(Open Source\)

Bot-Net provides easy ways to execute many kinds of information gatherings and attacks.

* Fully Open Source
* Written in Python
* Continuously updated and extended

### Features

* [x] Localhost Web GUI
* [x] Sniffing
* [x] Website crawling
* [x] Web page parsing
* [ ] SQL injection
* [ ] Injected database management
* [ ] Brute force attacks
* [ ] Cluster between other Bot-Nets
* [ ] Multiple asynchronous requests
* [ ] Multiple targets management
* [ ] Useful CTF features

### ![](https://raw.githubusercontent.com/offensive-hub/Bot-Net/master/resources/logos/pypi.png)   PyPI installation
```shell
sudo pip3 install Bot-Net
```

### Run

* **GUI:** `Bot-Net -g`
* **Command line:** `Bot-Net <arguments>`

### Debug

* Run django \(examples\):
  * `Bot-Net --django runserver`
  * `Bot-Net --django help`
  * `Bot-Net --django "help createsuperuser"`

### Project layout

```text
[root]
  |
  |-- app/              # Main application package
  |    |
  |    |-- arguments/       # User input arguments parser (100%)
  |    |
  |    |-- attack/          # Attack modality package (0%)
  |    |-- defense/         # Defense modality package (0%)
  |    |
  |    |-- gui/             # Graphical User Interface package (100%)
  |    |
  |    |-- helpers/         # Helper methods package (100%)
  |    |
  |    |-- managers/        # Managers package
  |    |    |
  |    |    |-- cluster/        # Cluster managers package (0%)
  |    |    |-- crypto/         # Encryption managers package (70%)
  |    |    |-- injection/      # Injection managers package (60%)
  |    |    |-- parser/         # Parser managers package (100%)
  |    |    |-- request/        # Request managers package (70%)
  |    |    |-- sniffer/        # Sniffer managers package (95%)
  |    |
  |    |-- services/        # Services package
  |    |    |
  |    |    |-- logger.py       # Logger service (100%)
  |    |    |-- multitask.py    # MultiTask service (100%)
  |    |    |-- serializer.py   # PickleSerializer and JsonSerializer serivces (100%)
  |    |
  |    |-- storage/         # Storage directory
  |    |
  |    |-- env.py           # Environment variables management
  |
  |-- .env              # Environment variables
  |
  |-- Bot-Net.py    # Main executable
```

### Links

* PyPI: [https://pypi.org/project/Bot-Net](https://pypi.org/project/Bot-Net/)
* GitHub: [https://github.com/Abhayindia/BOT-NET](https://github.com/Abhayindia/BOT-NET)

### Authors

* [Abhay Chaudhary]
