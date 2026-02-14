#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Boehringer Ingelheim
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: maas_config

author:
  - Patrick Pfurtscheller (@pfurtschellerp)
short_description: Manage MAAS configuration parameters.
description:
  - This module allows you to manage MAAS configuration parameters by setting their values.
version_added: 1.1.0
extends_documentation_fragment:
  - maas.maas.cluster_instance
seealso: []
options:
  name:
    description:
      - Setting to be changed.
    type: str
    required: True
  value:
    description:
      - Desired value of the configuration parameter.
    type: str
    required: True
"""

EXAMPLES = r"""
- name: Set maas_name configuration parameter
  maas.maas.config:
    cluster_instance: my-cluster-instance
    name: maas_name
    value: new-maas-name
"""

RETURN = r"""
record:
  description:
    - Set configuration parameter.
  returned: success
  type: dict
  sample:
    name: maas_name
    value: new-maas-name
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, errors
from ..module_utils.client import Client
from ..module_utils.cluster_instance import get_oauth1_client


def run(module, client: Client):
    name = module.params["name"]
    value = module.params["value"]
    changed = False

    current_value = client.get(
        "/api/2.0/maas/op-get_config", query={"name": name}
    ).json

    if current_value != value:
        changed = True
        if not module.check_mode:
            client.post(
                "/api/2.0/maas/op-set_config",
                data={"name": name, "value": value},
            )

    record = {"name": name, "value": value}

    return (changed, record)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("cluster_instance"),
            name=dict(type="str", required=True),
            value=dict(type="str", required=True),
        ),
    )

    try:
        client = get_oauth1_client(module.params)
        changed, record = run(module, client)
        module.exit_json(changed=changed, record=record)
    except errors.MaasError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
