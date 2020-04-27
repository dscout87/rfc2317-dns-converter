import argparse
import ipaddress

parser = argparse.ArgumentParser(prog='rfc2317 CIDR converter')
parser.add_argument('--cidr', '-n', type=str, required=True,
                    help='CIDR - network address with prefix (ex. 192.168.0.0/24)')
args = parser.parse_args()


def cidr_to_zone_name(cidr):
    ipaddress.ip_network(cidr)

    ipv4_max_octets = 4
    network_addr, prefix = cidr.split('/')
    prefix_whole_part = int(prefix) // 8
    prefix_fraction_part = int(prefix) % 8

    octets_to_cut = ipv4_max_octets - prefix_whole_part
    if prefix_fraction_part > 0:
        octets_to_cut -= 1

    reverse_addr = f"{ipaddress.ip_address(network_addr).reverse_pointer}."
    reverse_addr_cutted = '.'.join(reverse_addr.split('.')[octets_to_cut:])

    if prefix_fraction_part > 0:
        leading_path = f"{reverse_addr_cutted.split('.')[0]}/{prefix}"
        trailing_path = '.'.join(reverse_addr_cutted.split('.')[1:])
        return f'{leading_path}.{trailing_path}'
    else:
        return reverse_addr_cutted


if __name__ == '__main__':
    print(cidr_to_zone_name(args.cidr))
