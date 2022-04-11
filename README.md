# Client VPN

This project aims to facilitate the use of the openconnect program to connect to a vpn

# Requirements

- [Python 3.7](https://www.python.org/downloads/release/python-370/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [Openconnect](https://pkgs.org/download/openconnect)

# How to use?

1. Clone this repo
    > $ git clone https://github.com/ronaldsantos63/client-vpn-openconnect.git
1. Install requirments with pipenv
    > $ pipenv install && pipenv install --dev
1. Build executable
    > $ ./setup.sh
1. Run client_vpn from dist folder