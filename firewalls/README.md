# Firewalls scripting

The scenario I'm working towards here is one based on experience of firewalling access to MS Office 365. Every month I'd be sent a new list of IPs that needed to be allowed, the IPs came from list on the Microsoft website and was available as JSON, so I had thought "wouldn't it be nice if the firewalls were set up in such a way that we could parse that JSON download and update object groups which were used in the rule base.

So, my plan here is for a few different types of firewall have scripts that'll do just that, create objects and update object groups.

Maybe in the future we'll look at some kind of state keeping so that we can remove hosts that are no longer needed.