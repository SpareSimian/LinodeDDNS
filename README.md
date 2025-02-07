# LinodeDDNS
Update dynamic DNS records at Linode.com using the [Linode v4 Python library](https://github.com/linode/linode_api4-python).

usage: linode-ddns.py foo.example.com

Sets the A and AAAA records for foo in example.com.
Assumes a personal access token can be found in file ~/.ssh/linode_api_token_ddns.
Token should have the domain write privilege.

A hack is needed to force use of IPv4 or IPv6 connections:

https://github.com/psf/requests/issues/1691
https://stackoverflow.com/questions/33046733/force-requests-to-use-ipv4-ipv6
