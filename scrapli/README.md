# Scrapli Testing

Testing speed difference between [Scrapli](https://github.com/carlmontanari/scrapli) and [Netmiko](https://github.com/ktbyers/netmiko).

I have two IOSv routers running in GNS3, and they need some interface configuration and routes adding.  
Under normal circumstances some form of parallel processing would be used, but not for this test - the scripts will configure the routers sequentially.

## Results

Routers were reloaded without saving config between runs:

```console
(venv) matt@slappy scrapli $ python netmikotest.py 
Took 3.117312431335449 seconds to complete
(venv) matt@slappy scrapli $ python netmikotest.py 
Took 2.9584999084472656 seconds to complete
(venv) matt@slappy scrapli $ python scraplitest.py 
Took 11.287449598312378 seconds to complete
```

This doesn't seem right, Scrapli is supposed to be "blazing fast".

Once the ssh2 transport is selected the test is quicker:

```console
(venv) matt@slappy scrapli $ python scraplitest.py 
Took 2.8908116817474365 seconds to complete
(venv) matt@slappy scrapli $ python scraplitest.py 
Took 3.1362390518188477 seconds to complete
(venv) matt@slappy scrapli $
```

The default transport is `system` which should be whatever ssh is used on the host system. It should be openssh on my system. The `ssh2` transport should in theory be no quicker since it simply has a different wrapper to that, but it is quicker.

So using the ssh2 transport in Scrapli, the two are broadly comparable in this test at least.