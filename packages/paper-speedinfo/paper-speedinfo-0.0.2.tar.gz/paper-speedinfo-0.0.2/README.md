# paper-speedinfo

Патч библиотеки [django-speedinfo](https://github.com/catcombo/django-speedinfo) для [paper-admin](https://github.com/dldevinc/paper-admin)

## Requirements
* Python >= 3.6
* Django >= 2.1

## Installation
Add `paper_speedinfo` before `speedinfo` to your INSTALLED_APPS setting.
```python
INSTALLED_APPS = [
    # ...
    'paper_speedinfo',
    'speedinfo',
    # ...
]

MIDDLEWARE = [
    # ...
    'speedinfo.middleware.ProfilerMiddleware',
    # ...
]

CACHES = {
    'default': {
        'BACKEND': 'speedinfo.backends.proxy_cache',
        'CACHE_BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SPEEDINFO_STORAGE = "speedinfo.storage.cache.storage.CacheStorage"
SPEEDINFO_EXCLUDE_URLS = [
    r'/admin/',
]
```


