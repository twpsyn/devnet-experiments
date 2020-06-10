# Threading

Ny purpose here was to test out using concurrency in conjunction with netmiko to speed up operations.

Since netmiko can be a little slow in operation (not necessarily the fault of netmiko) it would be good to run netmiko tasks against several switches at the same time.

All of the scripts simply connect to five switches in a CML environment and obtain interface information. Nothing too complicated, but enough to see the effect of concurrency.

The sequential script (get_ifs_seq.py) does this against each switch in turn. Its average execution time was in the region of 32 seconds.

The threaded script (get_ifs_thread.py) uses a ThreadPoolExecutor to execute on all five switches at the same time. It's average execution time was of the order of 7 seconds.

The multi-processor script (get_ifs_proc) uses a ProcessPoolExecutor for the same. It also has an average execution time of around 7 seconds.

## Conclusion

My understanding of the difference between multi-thread and multi-process is that when a script is CPU bound then you'll want to use multi-process, when it's I/O bound then you want multi-thread.

As the bottleneck in scripting network changes is in the I/O to the network devices, I think I'll be going with threading.