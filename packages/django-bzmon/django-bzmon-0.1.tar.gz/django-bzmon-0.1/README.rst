=====
BZMon
=====

BZMon is a Django app to provide access to system monitoring status through API.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "bzmon" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bzmon',
    ]

2. Include the bzmon URLconf in your project urls.py like this::

    path('bzmon/', include('bzmon.urls')),

3. Add BZMON_CONFIG to your django settings.py like this::

    BZMON_CONFIG = {
        "token": {
            "required": True,
            "token": "token"
        },
        "monitor": {
            "memory": True,
            "storage": True
        },
        "memory": {
            "warn": True,
            "warn_level": 500
        },
        "storage": [
                {
                    "path": str(BASE_DIR),
                    "warn": True,
                    "warn_level": 500
                },
                {
                    "path": "/unexist",
                    "warn": True,
                    "warn_level": 500
                }
            ],
        "contacts": [
            {
                "name": "Bo Zhao",
                "email": "bo.zhao@leicester.ac.uk"
            }
        ]
    }

4. Visit http://127.0.0.1:8000/bzmon/?token=token to get .