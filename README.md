# LinodeDDNS
Update dynamic DNS records at Linode.com using the [Linode v4 Python library](https://github.com/linode/linode_api4-python).

Usage: linode-ddns.py foo.example.com

Sets the A and AAAA records for foo in example.com.

Install the Linode API:
```
pip3 install linode_api4
```

Use the Linode control panel to create a personal access token.  The
token should have the domain write privilege.  The script assumes the
Linode personal access token can be found in file
~/.ssh/linode_api_token_ddns.

Copy or link the systemd unit files to /etc/systemd/system. The
systemd unit files assume the script is cloned to
/usr/local/bin/LinodeDDNS. Edit the service unit with "systemctl edit
linode-ddns.service" to set the desired hostname record to update.
This will create an override file without changing the original file.

A hack is needed to force use of IPv4 or IPv6 connections:

https://github.com/psf/requests/issues/1691
https://stackoverflow.com/questions/33046733/force-requests-to-use-ipv4-ipv6
