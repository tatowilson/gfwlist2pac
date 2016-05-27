#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pkgutil
import urllib.parse as urlpar
import json
import logging
import urllib.request as urlreq
from argparse import ArgumentParser
import base64

__all__ = ['main']


gfwlist_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                        help='path to gfwlist', metavar='GFWLIST')
    parser.add_argument('-f', '--file', dest='output', required=True,
                        help='path to output pac', metavar='PAC')
    parser.add_argument('-p', '--proxy', dest='proxy', required=True,
                        help='the proxy parameter in the pac file, '
                             'for example, "SOCKS5 127.0.0.1:1080;"',
                        metavar='PROXY')
    parser.add_argument('--user-rule', dest='user_rule',
                        help='user rule file, which will be appended to'
                             ' gfwlist')
    parser.add_argument('--precise', dest='precise', action='store_true',
                        help='use adblock plus algorithm instead of O(1)'
                             ' lookup')
    return parser.parse_args()

def get_data_from_file(file_path):
    with open(file_path, 'r') as f:
        builtin_rules = f.read()
        return builtin_rules


def decode_gfwlist(content):
    # decode base64 if have to
    try:
        if '.' in content:
            raise Exception()
        return base64.b64decode(content).decode('utf-8')
    except:
        return content


def get_hostname(something):
    try:
        # quite enough for GFW
        if not something.startswith('http:'):
            something = 'http://' + something
        r = urlpar.urlparse(something)
        return r.hostname
    except Exception as e:
        logging.error(e)
        return None


def add_domain_to_set(s, something):
    hostname = get_hostname(something)
    if hostname is not None:
        s.add(hostname)


def combine_lists(content, user_rule=None):
    gfwlist = get_data_from_file('resources/builtin.txt').splitlines(False)
    gfwlist.extend(content.splitlines(False))
    if user_rule:
        gfwlist.extend(user_rule.splitlines(False))
    return gfwlist


def parse_gfwlist(gfwlist):
    domains = set()
    for line in gfwlist:
        if line.startswith(('!','[','@')):
            # ignore white list
            continue
        if line.find('.*') >= 0:
            continue
        elif line.find('*') >= 0:
            line = line.replace('*', '/')
        if line.startswith(('|','.')):
            line = line.lstrip('|.')
        add_domain_to_set(domains, line)
    return domains


def reduce_domains(domains):
    # reduce 'www.google.com' to 'google.com'
    # remove invalid domains
    tld_content = get_data_from_file("resources/tld.txt")
    tlds = set(tld_content.splitlines(False))
    new_domains = set()
    for domain in domains:
        domain_parts = domain.split('.')
        last_root_domain = None
        for i in range(0, len(domain_parts)):
            root_domain = '.'.join(domain_parts[len(domain_parts) - i - 1:])
            if i == 0:
                if not tlds.__contains__(root_domain):
                    # root_domain is not a valid tld
                    break
            last_root_domain = root_domain
            if tlds.__contains__(root_domain):
                continue
            else:
                break
        if last_root_domain is not None:
            new_domains.add(last_root_domain)
    return new_domains


def generate_pac_fast(domains, proxy):
    # render the pac file
    proxy_content = get_data_from_file('resources/proxy.pac')
    domains_dict = {}
    for domain in domains:
        domains_dict[domain] = 1
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__DOMAINS__',
                                          json.dumps(domains_dict, indent=2))
    return proxy_content


def generate_pac_precise(rules, proxy):
    def grep_rule(rule):
        if rule:
            if rule.startswith(('!','[')):
                return None
            return rule
        return None
    # render the pac file
    proxy_content = get_data_from_file('resources/abp.js')
    rules = list(filter(grep_rule, rules))
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__RULES__',
                                          json.dumps(rules, indent=2))
    return proxy_content


def main():
    args = parse_args()
    user_rule = None
    if (args.input):
        with open(args.input, 'r') as f:
            content = f.read()
    else:
        print('Downloading gfwlist from %s' % gfwlist_url)
        content = urlreq.urlopen(gfwlist_url, timeout=10).read().decode('utf-8')
    if args.user_rule:
        userrule_parts = urlpar.urlsplit(args.user_rule)
        if not userrule_parts.scheme or not userrule_parts.netloc:
            # It's not an URL, deal it as local file
            with open(args.user_rule, 'r') as f:
                user_rule = f.read()
        else:
            # Yeah, it's an URL, try to download it
            print('Downloading user rules file from %s' % args.user_rule)
            user_rule = urlreq.urlopen(args.user_rule, timeout=10).read().decode('utf-8')

    content = decode_gfwlist(content)
    gfwlist = combine_lists(content, user_rule)
    if args.precise:
        pac_content = generate_pac_precise(gfwlist, args.proxy)
    else:
        domains = parse_gfwlist(gfwlist)
        domains = reduce_domains(domains)
        pac_content = generate_pac_fast(domains, args.proxy)
    with open(args.output, 'w') as f:
        f.write(pac_content)


if __name__ == '__main__':
    main()

