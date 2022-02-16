# Fortigates

The FortiOS CLI isn't going to be easy to parse in a script. That may not matter for the purposes of creating objects and adding them to groups: we could just push config without regard for what already exists, but that could lead to us trying to create network objects that already exist, and we could leave extra hosts in our groups. So ideally we want to apply some intelligence which requires getting config as well as pushing it.

So the way to go will probably be the FortiOS REST API, however some CLI action will be beneficial to generate the API key if it hasn't already been created.