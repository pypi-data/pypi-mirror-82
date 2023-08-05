# iplist

Expand ip ranges to list of ips

## Setup

To install:
```shell
git clone https://gitlab.com/Zer1t0/iplist
cd iplist/
make
```


## Examples

Expand CDIR range:
```shell
iplist 10.0.0.0/24
```

Expand ips between start and end ip:
```shell
iplist 10.0.0.0-10.0.0.255
```

Send ranges from stdin:
```shell
cat ip_ranges.txt | iplist
```
