# Bootstrap

Bringing together the results from templating and threading, as well as the netmiko example from the VIRL/CML dicumentation, this script configures up 5 switches in a VIRL environment to give them hostnames, management IPs and enable ssh.

One thing I have noticed is that netmiko doesn't seem to handle console messages very well when connected to a device console, so that gets disabled before the script applies any true configuration.

It largely works, but sometimes the netmiko redispatch fails. I haven't worked out why that is. It may be that the default hostname on the IOSv_L2 images in VIRL has an underscore in it and that throws the prompt parser.

Regardless, the script appears to work on a second run, so it's not a major issue.