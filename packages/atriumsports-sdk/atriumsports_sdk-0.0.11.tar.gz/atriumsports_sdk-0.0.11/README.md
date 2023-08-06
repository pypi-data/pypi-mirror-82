# Atrium Sports API SDK

Python module to make use of the Atrium Sports Datacore API


Datacore REST API
```python
from atriumsports import AtriumSports

atrium = AtriumSports({
    'sport': 'basketball',
    'credential_id': 'XXXXX',
    'credential_secret': 'YYYY',
    'organizations': ['b1e34'],
})
datacore = atrium.client('datacore')
response = datacore.get('/o/b1a23/competitions', limit=500)
for data in response.data():
    print(data)
```

Datacore Streaming API

```python
from atriumsports import AtriumSports

atrium = AtriumSports({
    'sport': 'basketball',
    'credential_id': 'XXXXX',
    'credential_secret': 'YYYY',
    "environment": "sandpit",
})
stream_api = atrium.client('datacore-stream')

def on_connect_callback_function(client):
    """ example callback when connected """
    print("connected")

def on_read_callback_function(client, topic, message):
    """ example callback when message read """
    print("{}: {}".format(topic, message))

connected = stream_api.connect({
    "fixture_id": 'f71dfdd6-51f1-11ea-8889-22953e2ee7e2',  #fixture_id
    "scopes": [   # Scopes
        "write:stream_events",
        "read:stream_events"
    ],
    "on_read": on_read_callback_function,
    "on_connect": on_connect_callback_function
})
if not connected:
    print(stream_api.error())
else:
    stream_api.publish(
        "write:stream_events",
        {
            "type": "event",
            "data": {
                "eventClass": "sport",
                "eventId": "c2404cc0-9f75-11e8-98d0-529269fb1459",
                "entityId": "c24048a6-9f75-11e8-98d0-529269fb1459",
                "personId": "c2405b2a-9f75-11e8-98d0-529269fb1459",
                "eventType": "2pt",
                "subType": "jumpshot",
                "clock": "PT08:23",
                "shotClock": "PT12.3",
                "periodId": 2,
                "success": True,
                "timestamp": "2018-08-14T16:45:34.34",
                "clientId": "c2408302-9f75-11e8-98d0-529269fb1459",
                "clientType": "TestApi:1.1.2"
            }
        }
    )
    time.sleep(40)

    stream_api.disconnect()

```
