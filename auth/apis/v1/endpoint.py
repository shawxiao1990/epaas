# -*- coding: utf-8 -*-
from auth.models import Endpoint, Server


def get_endpoints():
    endpoints = Endpoint.query.all()
    return endpoints


def endpoint_schema():
    endpoints_map = {}
    endpoints = get_endpoints()
    for endpoint in endpoints:
        print(endpoint.servers)
        serverList_json = {}
        roleList_json = {}
        for server in endpoint.servers:
            serverList_json[server.name] = server.ip
            roleList_json[server.name] = server.roles.split(',')
        endpoint_json = {
            'id': endpoint.id,
            'path': endpoint.path,
            'roles': endpoint.roles.split(','),
            'serverList': serverList_json,
            'roleList': roleList_json
        }
        endpoints_map[endpoint.name] = endpoint_json
    return endpoints_map
