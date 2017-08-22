import json

def parse_type( instance_file ):
  with open( instance_file ) as json_data:
    inst = json.load(json_data)
    instance_meta = {}
    instance_meta["region"] = inst.get('region', 'us-west-2')
    instance_meta["type"] = inst.get('type', 'ec2instance')

    return [ instance_meta, inst ]

def get_user_data(snippet_files):
    userdata_list = []

    for snippet in snippet_files:
        with open(snippet) as f:
            data_line = f.read()

        userdata_list.append(data_line)
    userdata_string = "\n".join(userdata_list)

    return userdata_string

def user_data_build(instance_name, snippet_files):
    build_user_data = get_user_data(snippet_files)

    user_data = ("#!/bin/bash\n"
                 "host_name={instance_name}\n"
                 "{build_user_data}\n"
                 ).format(instance_name=instance_name, build_user_data=build_user_data)

    return user_data


