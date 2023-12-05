from urllib.parse import urlparse


def parse_url(url):
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    subdomain = parsed_url.hostname.split('.')[0] if parsed_url.hostname.count('.') > 1 else ''
    host_name = '.'.join(parsed_url.hostname.split('.')[-2:]) if parsed_url.hostname.count('.') > 1 else parsed_url.hostname
    return protocol, subdomain, host_name
