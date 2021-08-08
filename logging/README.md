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


## Scrapli

Since netmiko was so easy, might as well look at scrapli. I don't particularly favour netmiko over scrapli, but scrapli currently doesn't have drivers for some of the kit that I need to work on, so netmiko comes first.

Scrapli also has built in logging abilities. It has the opinionated logger and the basic logger, as well as the channel logger.

For my money the [basic logger](scrapli_log_basic.py) is pretty awful when threading is in use, maybe worse than the global logging in netmiko because it appears to be forking additional threads or processes for the channel communications. It's near impossible to trace a single device in there.

The [opinionated logging](scrapli_log.py) however is quite nice. I like that it includes the IP of the device in each line.

[Channel logging](scrapli_log_chan.py) is the equivalent to the session logging in Netmiko. Gives you the logs as if you were sitting at the device.