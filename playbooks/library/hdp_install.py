#!/usr/bin/python

DOCUMENTATION = '''
---
init cluster using hdp blueprint : 
http://docs.hortonworks.com/HDPDocuments/Ambari-2.4.1.0/bk_ambari-reference/content/ch_using_ambari_blueprints.html
'''

EXAMPLES = '''

'''

import socket
import xml.etree.ElementTree as ET
import xml.dom.minidom
import requests

def main():
    module = AnsibleModule(
        argument_spec=dict(
            ambari_host=dict(required=True, type='str'),
            ambari_port=dict(required=False, type='int', default=7180),
            ambari_username=dict(required=True, type='str'),
            ambari_password=dict(required=True, type='str', no_log=True),
            hdp_cluster_name=dict(required=True, type='str'),
            hdp_hosts=dict(required=True, type='list'),
            services=dict(required=True, type='list'),
            parcel_url=dict(required=False, type='str'),
            parcel_version=dict(required=False, type='str'),
        )
    )

    ambari_host = module.params.get('ambari_host')
    ambari_port = module.params.get('ambari_port')
    ambari_username = module.params.get('ambari_username')
    ambari_password = module.params.get('ambari_password')
    hdp_cluster_name = module.params.get('hdp_cluster_name')
    services = module.params.get('services')
    hdp_hosts = module.params.get('hdp_hosts')
    parcel_url = module.params.get('parcel_url')
    parcel_version = module.params.get('parcel_version')

    #module.fail_json(changed=False, msg=hosts)

#    if not HAS_AMBARI_API:
#        module.fail_json(changed=False, msg='python module ambari_api required for this ansible module')

    try:
        changed = False

        api = ApiResource(ambari_host, server_port=ambari_port, username=ambari_username, password=ambari_password)

        # 1 - create cluster
        cluster = create_cluster(module, api, hdp_cluster_name)
        # 2 - add hosts
        create_hosts(module, api, cluster, hdp_hosts)
        # 3 - set parcels
        set_parcels(module, api, cluster, parcel_url, parcel_version)
#        return
        # 4 - create services & roles
        # [ "hdfs", "zookeeper", "yarn", "oozie", "hive", "hue", "impala", "spark_on_yarn"]
        create_services(module, api, cluster, services)
        # 5 - restart services
#        service.restart()

        # restart all if changed is true
        cluster.stop().wait()
        cluster.start().wait()


        module.exit_json(changed=changed)

    except ApiException as e:
        module.fail_json(changed=False, msg="Problem when installing cluster : %s" % e)
def create_cluster(module, api, hdp_cluster_name):
    cluster = None
    try:
        cluster = api.get_cluster(hdp_cluster_name)
    except ApiException as e:
        if 'not found' in e._message:
            cluster = api.create_cluster(hdp_cluster_name)
    return cluster

def create_hosts(module, ambari_api, cluster, hdp_hosts):
    # create missing cm host
    ambari_hosts = [x.hostname for x in ambari_api.get_all_hosts()]
    missing_ambari_host = [x for x in hdp_hosts if x not in ambari_hosts]
    for h in missing_ambari_host:
        ambari_api.create_host(h, h, socket.gethostbyname(h))

    # add mising hosts to cluster
    cluster_hosts = [x for x in ambari_api.get_all_hosts() if x.hostname in hdp_hosts]
    existing_cluster_hosts = [x.hostId for x in cluster.list_hosts()]
    missing_cluster_host = [x for x in cluster_hosts if x.hostId not in existing_cluster_hosts]
    cluster.add_hosts([x.hostId for x in missing_cluster_host])


def create_services(module, ambari_api, cluster, services):
    existing_services = [x.type for x in cluster.get_all_services()]
    for service in services:
        if service['name'].upper() not in existing_services:
            cluster.create_service(service['name'], service['name'].upper())
        if service['roles']:
            cluster_service = cluster.get_service(service['name'])
            existing_roles = cluster_service.get_all_roles()
            existing_hosts = [x.hostRef.hostId for x in existing_roles]
            for role in service['roles']:
                for host in role['hosts']:
                    host = _get_host_by_hostname(ambari_api, host)
                    if host.hostId not in existing_hosts:
                        role_id = service['name']+role['name']+host.hostId.replace('-', '').replace('.', '')
                        cluster_service.create_role(role_id, role['name'].upper(),host.hostId)

def _get_host_by_hostname(ambari_api, hostname):
    # create missing cm host
    ambari_hosts = ambari_api.get_all_hosts()
    for h in ambari_hosts:
        if h.hostname == hostname:
            return h
    return None

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()