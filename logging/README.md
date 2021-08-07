# Logging

I sat down this evening with a goal of getting a grip with logging in netmiko. I anticipated hours spent getting to know the logging module and coming out of the end of it with a snippet of code to use.

Turns out I just needed to add `session_log` to the connection parameters.

We can add a debug level log using the logging module and something along these lines:

```python
logging.basicConfig(
    filename="logs/netmiko_global.log",
    level=logging.DEBUG,
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
)
logger = logging.getLogger("netmiko")
```
however it gets very confusing with multiple threads so may not be much use. The session log is probably all that's needed.