import requests
import time
import os
import json

name = 'optimalmemes.org'

def secret():
    if not os.path.exists('secret'):
        raise Exception('Need secret file with digitalocean_token, digitalocean_ssh_name, godaddy_key, godaddy_secret')
    return json.loads(open('secret').read())

def bearer():
    return 'Bearer ' + secret()['digitalocean_token']

def sso_key():
    return 'sso-key ' + secret()['godaddy_key'] + ':' + secret()['godaddy_secret']

def droplets():
    r = requests.get('https://api.digitalocean.com/v2/droplets', headers={'Authorization':bearer()})
    r.raise_for_status()
    return r.json()['droplets']

def find_key_id():
    r = requests.get('https://api.digitalocean.com/v2/account/keys', headers={'Authorization':bearer()})
    r.raise_for_status()
    key_name = secret()['digitalocean_ssh_name']
    for ssh_key in r.json()['ssh_keys']:
        if ssh_key['name'] == key_name:
            return ssh_key['id']
    raise Exception('Cannot find ssh key named %s' %(key_name,))

def create_droplet():
    key_id = find_key_id()
    payload = {'name':name, 'region':'nyc1','size':'512mb','image':'ubuntu-16-04-x64','ssh_keys':[key_id],'backups':False,'ipv6':False,'user_data':None,'private_networking':None,'volumes':None,'tags':[]}
    r = requests.post('https://api.digitalocean.com/v2/droplets', data=json.dumps(payload), headers={'Content-Type':'application/json','Authorization':bearer()})
    if r.status_code >= 400:
        print(r.text)
    r.raise_for_status()

def have_droplet():
    for droplet in droplets():
        if droplet['name'] == name:
            return True
    return False

def get_droplet_ip():
    for droplet in droplets():
        if droplet['name'] == name and 'networks' in droplet and 'v4' in droplet['networks'] and len(droplet['networks']['v4']) > 0:
            return droplet['networks']['v4'][0]['ip_address']
    return None

def get_droplet_ip_or_create():
    if not have_droplet():
        print('Creating droplet')
        create_droplet()
        print('Droplet successfully created')
    for i in range(10):
        ip = get_droplet_ip()
        if ip != None:
            return ip
        time.sleep(5)

    raise Exception('Droplet did not return ip address')

def domains():
    r = requests.get('https://api.godaddy.com/v1/domains', headers={'Authorization':sso_key()})
    print(r.json())
    r.raise_for_status()

#print(get_droplet_ip_or_create())
print(domains())

