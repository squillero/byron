# MEMO

> ┏━┏━━┓━━━━━━━━━━━━━━━━━━┓
> ┃━┃┏┓┃━━━━━━━━━━━━━━━━━━┃
> ┃━┃┗┛┗┓┏┓━┏┓┏━┓┏━━┓┏━┓━━┃
> ┃━┃┏━┓┃┃┃━┃┃┃┏┛┃┏┓┃┃┏┓┓━┃
> ┃━┃┗━┛┃┃┗━┛┃┃┃━┃┗┛┃┃┃┃┃━┃
> ┃━┗━━━┛┗━┓┏┛┗┛━┗━━┛┗┛┗┛━┃
> ┃━┏━━━━━━┛┃━━━━━━━━━━━━━┃
> ┗━┗━━━━━━━┛━━━━━━━━━━━━━┛

## Publish

```shell
bumpver update
poetry build
poetry publish

bumpver update; poetry build; poetry publish
```

## Coverage

```
coverage run --branch -m pytest
coverage html
```