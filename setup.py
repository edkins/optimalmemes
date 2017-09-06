
name = 'optimalmemes.org'

def resolve_name():
    raise Error('not implemented')

def start_droplet():
    response = start_droplet_through_api()
    add_known_host(response.ip, response.host_key)
    return response.ip

def droplet_ip():
    ip = find_droplet()
    if ip == None:
        return ip
    return start_droplet()

def server_ip():
    if not have_known_host():
        ip = droplet_ip()
        if resolve_name() != ip:
            godaddy_set_name_to(ip)

def ssh_in_and_do_things():
    server_ip()
    ssh()

