# Tradologics Controller (command-line tool)

<a href="https://tradologics.com/opensource"><img alt="npm Version" src="https://img.shields.io/badge/By-Tradologics-7269a6"></a>
<a href="https://pypi.python.org/pypi/tctl"><img alt="Python Version" src="https://img.shields.io/badge/python-3.6+-blue.svg?style=flat"></a>
<a href="https://pypi.python.org/pypi/tctl"><img alt="PyPi Version" src="https://img.shields.io/pypi/v/tctl.svg?maxAge=60"></a>



Meet `tctl` (stands for Tradologics Controller) - Tradologics command-line utility.

`tctl` simplfies your development workflow by allowing for communication with Tradologics directly from the command-line, thus removing even more friction.


## Install (Dev environment) via Github

```bash
$ pip3 install -U git+https://github.com/tradologics/tctl.git@dev
```

Next, run `tctl config` to set up your `tctl` to work with your account by providing it with your account's API key and Secret key.

---

## Conventions

- Appending `--raw` to your command will display the API's raw response. Otherwise, a tabular data will be displayed
- The pipe character (`|`) means "or". For example, `list|ls` means that you can use either `list` or `ls`.
- Items `[` wrapped by `]` are optional.

### Flag identifiers

- `--account|-a` [account-id]
- `--order|-o` [order-id]
- `--broker|-b` [broker-id]
- `--tradehook|-t` [tradehook-id]
- `--strategy|-s` [strategy-id]
- `--monitor|-m` [monitor-id]
- `--exchange|-e` [exchange-mic]

---

## Available commands

\* More detailed documentation coming soon.

- [x] `$ tctl --version` - Displays installed tctl version
- [x] `$ tctl --help` - Displays tctl options
- [x] `$ tctl config` - Initialize, authorize, and configure the tctl tool
- [x] `$ tctl logo` - Displays Tradologics logo as ASCII art :)

### Get list of brokers

- [x] `$ tctl brokers list|ls`

### Broker accounts

- [x] `$ tctl accounts list|ls`
- [x] `$ tctl accounts info --account|-a account-id`
- [x] `$ tctl accounts new`
- [x] `$ tctl accounts update --account|-a account-id`
- [x] `$ tctl accounts delete|rm --account|-a account-id`

### Trading

- [x] `$ tctl positions list|ls [--account|-a my-account]`
- [x] `$ tctl trades list|ls [--account|-a my-account]`

- [x] `$ tctl orders list|ls [--account|-a my-account]`
- [x] `$ tctl orders new [--account|-a my-account]`
- [x] `$ tctl orders info --order|-o order-id`
- [x] `$ tctl orders update --order|-o order-id`
- [x] `$ tctl orders delete|rm --order|-o order-id`

### Strategies

- [x] `$ tctl strategies list|ls`
- [x] `$ tctl strategies new`
- [x] `$ tctl strategies update --strategy|-s strategy-id`
- [x] `$ tctl strategies delete|rm --strategy|-s strategy-id`
- [x] `$ tctl strategies status --strategy|-s strategy-id`
- [x] `$ tctl strategies log --strategy|-s strategy-id --lines|-l number`
- [x] `$ tctl strategies set-mode --strategy|-s strategy-id --mode|-m backtest|paper|live`
- [x] `$ tctl strategies start --strategy|-s strategy-id`
- [x] `$ tctl strategies stop --strategy|-s strategy-id`
- [x] `$ tctl strategies deploy --strategy|-s strategy-id`
- [x] `$ tctl strategies stats --strategy|-s strategy-id [--start YYYY-MM-DD [--end YYYY-MM-DD]]`


### Tradehooks

- [x] `$ tctl tradehooks list|ls`
- [x] `$ tctl tradehooks new`
- [x] `$ tctl tradehooks info --tradehook|-t tradehook-id`
- [x] `$ tctl tradehooks update --tradehook|-t tradehook-id`
- [x] `$ tctl tradehooks attach --tradehook|-t tradehook-id [--strategy|-s [strategy-id]]`
- [x] `$ tctl tradehooks delete|rm --tradehook|-t tradehook-id`

### Market data

- [x] `$ tctl assets list|ls [--delisted|-d]`
- [x] `$ tctl assets info --asset|-a asset-identifier [--history|-h]`
- [x] `$ tctl exchanges list|ls`
- [x] `$ tctl exchanges list|ls --exchange|-e exchange-mic`
- [x] `$ tctl exchanges calendar --exchange|-e exchange-mic [--start YYYY-MM-DD [--end YYYY-MM-DD]]`
- [x] `$ tctl assets bar --asset|-a asset-identifier [--start YYYY-MM-DD [--end YYYY-MM-DD]]`
- [x] `$ tctl assets bars`

### Monitoring

- [x] `$ tctl monitors list|ls --strategy|-s strategy-id [--type|-t position|price]`
- [x] `$ tctl monitors new [--type|-t position|price]`
- [x] `$ tctl monitors delete|rm --monitor|-m monitor-id`


### Tokens

- [x] `$ tctl tokens list|ls`
- [x] `$ tctl tokens info --token|-t token-id [--full]`
- [x] `$ tctl tokens new`
- [x] `$ tctl tokens extend --token|-t token-id`
- [x] `$ tctl tokens delete|rm --token|-t token-id`
