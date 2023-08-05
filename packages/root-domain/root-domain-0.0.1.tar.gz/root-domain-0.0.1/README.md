# root-domain

This tool allows to extract the root domain from subdomains. 
Useful for parse lists of subdomains and retrieve the root domains.

Moreover you also can adjust the depth of the domains extracted with `-d` and `-D`

## Setup

To install:
```shell
git clone https://gitlab.com/Zer1t0/root-domain
cd root-domain/
python3 setup.py install
```

## Examples
Get root domain:
```shell
./root-domain.py a.b.c.d.e.google.com
google.com
```
Get subdomain with depth 2 (first subdomain):
```shell
/root-domain.py a.b.c.d.e.google.com -d 2
e.google.com
```

Get subdomains until depth 4:
```shell
./root-domain.py a.b.c.d.e.google.com -D 4
google.com
e.google.com
d.e.google.com
c.d.e.google.com
```

Get subdomains with depth between 3 and 4:
```shell
./root-domain.py a.b.c.d.e.google.com -d 3 -D 4
d.e.google.com
c.d.e.google.com
```
