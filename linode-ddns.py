#!/usr/bin/env python3

# usage: linode-ddns.py foo.example.com
# Sets the A and AAAA records for foo in example.com.
# Assumes a personal access token can be found in file ~/.ssh/linode_api_token_ddns.
# Token should have the domain write privilege.

import argparse
parser = argparse.ArgumentParser(description='Update DNS address records at Linode for a domain name to match public IP address of this host.')
parser.add_argument('domain_to_set', help='the fully-qualified domain name (FQDN) to associate with this host\'s public address')
args = parser.parse_args()

import socket
import requests.packages.urllib3.util.connection as urllib3_cn

import os
from linode_api4 import LinodeClient

# use 5 minute TTL for dynamic DNS, short but not crazy short
ddns_ttl_sec = 5 * 60

def allow_only_ipv4():
    return socket.AF_INET

def allow_only_ipv6():
    return socket.AF_INET6

def get_domain_record(domain, name, type):
    for record in domain.records:
        # note that name can be empty, for records referring to the
        # domain itself
        if (record.name == name) and (record.type == type):
            # print(f"record: {record.id} '{record.name}' {record.type} {record.target}")
            return record
    return None

def create_client():
    # read the token from ~/.ssh/linode_api_token_ddns
    home_dir = os.path.expanduser("~")
    token_file = os.path.join(home_dir, ".ssh", "linode_api_token_ddns")
    with open(token_file, 'r') as file:
        token = file.readline().rstrip('\n')
    # Create a Linode API client
    return LinodeClient(token)

def find_best_domain(client, fqdn):
    domains = client.domains()
    longest_match = 0
    domain_id = 0
    domain_name = ""
    for domain in domains:
        name = "." + domain.domain
        length = len(name)
        if args.domain_to_set.endswith(name) and (length > longest_match):
            best = domain
            longest_match = length
    if 0 == length:
        raise ValueError("no domain found in Linode account for this host name")
    return best

# Python 3.9 introduced string removesuffix method, this is for older versions of Python
def removesuffix(s, suffix):
    if s.endswith(suffix):
        return s[:-len(suffix)]
    return s
    
def create_or_update_record(record_type, allow_family):
    # first select address family (IPv4 or IPv6) BEFORE we open a socket
    urllib3_cn.allowed_gai_family = allow_family
    client = create_client()
    domain = find_best_domain(client, args.domain_to_set)
    domain_name = domain.domain
    base_name = removesuffix(args.domain_to_set, '.' + domain_name)
    # print(f"domain name {domain_name} found")
    record = get_domain_record(domain, base_name, record_type)
    if None == record:
        # create new record
        print(f"Creating {base_name} {record_type} record in domain {domain_name}")
        domain.record_create(record_type, name=base_name, ttl_sec=ddns_ttl_sec, target="[remote_addr]")
    else:
        print(f"Updating {base_name} {record_type} record in domain {domain_name}")
        record.target = "[remote_addr]"
        # update with new value
        result = record.save()

create_or_update_record('A', allow_only_ipv4)
create_or_update_record('AAAA', allow_only_ipv6)
