# dictfilter

## installation

```shell
pip install dictfilter
```

## usage

```python
bsg = {
    'class': 'Battlestar',
    'model': 'Jupiter',
    'name': 'Galactica',
    'crew': {
        'commander': 'William Adama',
        'xo': 'Saul Tigh',
        'cag': 'Kara Thrace',
    }
}

result = query(some_data, ['class', 'name', 'crew.commander'])

# {
#     'class': 'Battlestar',
#     'name': 'Galactica',
#     'crew': {
#         'commander': 'William Adama',
#     }
# }
```

## django integration

Register the dictfilter middleware in `settings.py`:

```python
MIDDLEWARE = [
    ...
    'dictfilter.django.middleware.DictFilterMiddleware',
]
```

By default, every 2xx series response will be filtered based on a comma-separated `fields` parameter in the query string.
