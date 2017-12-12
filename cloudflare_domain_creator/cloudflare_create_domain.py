import argparse
import CloudFlare


def _split_domain(domain):
    splited_domain = domain.split(".")

    root_domain = ".".join(splited_domain[-2:])
    subdomain = ".".join(splited_domain[0:-2])

    return root_domain, subdomain


def _get_cloud_flare_obj():
    return CloudFlare.CloudFlare()


def _get_domain_id(cf, domain):

    try:
        zone = cf.zones.get(params={'name': domain, 'per_page': 1})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        print(e)

    return zone[0]['id']


def create_subdomain(domain, sub_domain):
    cf = _get_cloud_flare_obj()
    zone_id = _get_domain_id(cf, domain)

    # Create new subdomain
    r = cf.zones.dns_records.post(zone_id, data={
        'name': sub_domain,
        'type': 'CNAME',
        'content': domain
    })


def remove_subdomain(domain, sub_domain):
    cf = _get_cloud_flare_obj()
    zone_id = _get_domain_id(cf, domain)

    r = cf.zones.dns_records.get(zone_id,
                                           params={'name': "{}.{}".format(
                                               sub_domain,
                                               domain
                                           )})
    subdomain_id = r[0]['id']

    cf.zones.dns_records.delete(zone_id, subdomain_id)


def main():
    parser = argparse.ArgumentParser()
    create_parser = parser.add_subparsers(dest='action')

    parser_a = create_parser.add_parser('create')
    parser_a.add_argument('domain')

    parser_b = create_parser.add_parser('remove')
    parser_b.add_argument('domain')

    kwargs = vars(parser.parse_args())

    if kwargs['action'] == None:
        print("Invalid action or domain")
        return

    domain, subdomain = _split_domain(kwargs['domain'])

    if kwargs['action'] == "create":
        create_subdomain(domain, subdomain)
    elif kwargs['action'] == "remove":
        remove_subdomain(domain, subdomain)
    else:
        print("Invalid action!")


if __name__ == '__main__':
    main()
