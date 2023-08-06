# RocketLaunchLive-API (rocketlaunchlive)
PyPi Integration to the RocketLaunch.live free API access (next 5 launches)

## Available Methods

There is one available method which is available using the free access to https://rocketlaunch.live using their endpoint https://fdo.rocketlaunch.live/json/launches/next/5

### get_next_launches(session (optional), key (optional))
Returns the next 5 rocket launches from the endpoint in JSON format.

Session can be sent as an optional aiohttp session if you are managing your session within an application.

Key can be sent as optional string for the API key if you are a paid RocketLaunchLive subscriber. You can subscribe at https://rocketlaunch.live.

Note: This library was built specifically for integration to Home Assistant.
