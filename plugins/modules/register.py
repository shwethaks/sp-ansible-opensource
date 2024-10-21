#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2024,Tom page <tpage@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# ibm.spectrum_protect.register:
#    node: "{{ physical_node }}"
#    url: "{{ tcp_node_address }}"
#    username: "{{ username }}"
#    password: "{{ password }}"
#    state: present

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'], 'supported_by': 'community'}


DOCUMENTATION = '''
---
module: register
author: "Tom page (@Tompage1994)"
short_description: Register or Deregister a node from IBM Spectrum Protect
description:
    - Register or Deregister a node from IBM Spectrum Protect
options:
    node:
      description:
        - The Node to register or deregister
      required: True
      type: str
      aliases:
        - name
    node_password:
      description:
        - Specifies the client node password
        - If you authenticate passwords locally with the IBM Storage Protect server, you must specify a password.
        - The minimum length of the password is 15 characters unless a different value is specified by using the SET MINPWLENGTH command.
        - The maximum length of the password is 64 characters.
      type: str
    node_password_expiry:
      description:
        - Specifies the number of days the password remains valid
        - You can set the password expiration period 0 - 9999 days. A value of 0 means that the password never expires.
        - If you do not specify this parameter, the server common-password expiration period is used which is 90 days unless changed by issuing the SET PASSEXP command.
      type: int
    session_security:
      description:
        - Specifies whether the node must use the most secure settings to communicate with an IBM Storage Protect server.
        - The system will default to "transitional"
      choices: ["strict", "transitional"]
      type: str
    state:
      description:
        - Desired state of the registration.
        - 'present' and 'registered' have the same effect.
        - 'absent' and 'deregistered' have the same effect.
      default: "registered"
      choices: ["present", "absent", "registered", "deregistered"]
      type: str

extends_documentation_fragment: ibm.storage_protect.auth
'''


EXAMPLES = '''
- name: Register node
  ibm.spectrum_protect.register:
    node: "{{ physical_node }}"
    node_password: P@ssword
    node_password_expiry: 90
    hostname: "{{ tcp_node_address }}"
    username: "{{ username }}"
    password: "{{ password }}"
    state: registered

- name: Deregister node
  ibm.spectrum_protect.register:
    node: "{{ physical_node }}"
    hostname: "{{ tcp_node_address }}"
    username: "{{ username }}"
    password: "{{ password }}"
    state: deregistered
'''

from ..module_utils.storage_protect_api import StorageProtectModule

def main():
    argument_spec = dict(
        node=dict(required=True, aliases=['name']),
        node_password=dict(no_log=True),
        node_password_expiry=dict(type='int', no_log=False),
        user_id=dict(),
        contact=dict(),
        policy_domain=dict(),
        compression=dict(choices=['client', 'true', 'false'], default='client'),
        can_archive_delete=dict(type='bool'),
        can_backup_delete=dict(type='bool'),
        option_set=dict(),
        force_password_reset=dict(type='bool'),
        node_type=dict(choices=['client', 'nas', 'server', 'objectclient'], default='client'),
        url=dict(),
        utility_url=dict(),
        max_mount_points=dict(type='int'),
        auto_rename_file_spaces=dict(choices=['client', 'true', 'false'], default='false'),
        keep_mount_points=dict(type='bool'),
        max_transaction_group=dict(type='int'),
        data_write_path=dict(choices=['any', 'lan', 'lanfree'], default='any'),
        data_read_path=dict(choices=['any', 'lan', 'lanfree'], default='any'),
        target_level=dict(),
        session_initiation=dict(choices=['clientorserver', 'serveronly'], default='clientorserver'),
        session_ip=dict(),
        session_port=dict(),
        email=dict(),
        deduplication=dict(choices=['clientorserver', 'serveronly'], default='clientorserver'),
        backup_initiation=dict(choices=['all', 'root'], default='all'),
        repl_state=dict(choices=['enabled', 'disabled']),
        backup_repl_rule_default=dict(choices=['ALL_DATA', 'ACTIVE_DATA', 'ALL_DATA_HIGH_PRIORITY', 'ACTIVE_DATA_HIGH_PRIORITY', 'DEFAULT', 'NONE']),
        archive_repl_rule_default=dict(choices=['ALL_DATA', 'ACTIVE_DATA', 'ALL_DATA_HIGH_PRIORITY', 'ACTIVE_DATA_HIGH_PRIORITY', 'DEFAULT', 'NONE']),
        space_repl_rule_default=dict(choices=['ALL_DATA', 'ACTIVE_DATA', 'ALL_DATA_HIGH_PRIORITY', 'ACTIVE_DATA_HIGH_PRIORITY', 'DEFAULT', 'NONE']),
        recover_damaged=dict(type='bool'),
        role_override=dict(choices=['client', 'server', 'other', 'usereported'], default='usereported'),
        authentication=dict(choices=['local', 'ldap'], default='local'),
        session_security=dict(choices=['transitional', 'strict'], default='transitional'),
        split_large_objects=dict(type='bool'),
        min_extent_size=dict(type='int', choices=[50, 250, 750], default=50),
        state=dict(choices=['present', 'absent', 'registered', 'deregistered'], default='present'),
    )

    required_by={
        'backup_repl_rule_default': 'repl_state',
        'archive_repl_rule_default': 'repl_state',
        'space_repl_rule_default': 'repl_state',
    }

    module = StorageProtectModule(argument_spec=argument_spec, supports_check_mode=True, required_by=required_by)

    node = module.params.get('node')
    state = module.params.get('state')
    exists, existing = module.find_one('node', node)

    if state == 'absent' or state == 'deregistered':
        module.deregister_node(node, exists=exists)
    else:
        options_params = {
            'node_password_expiry': 'PASSExp',
            'user_id': 'USerid',
            'contact': 'CONtact',
            'policy_domain': 'DOmain',
            'compression': 'COMPression',
            'can_archive_delete': 'ARCHDELete',
            'can_backup_delete': 'BACKDELete',
            'option_set': 'CLOptset',
            'force_password_reset': 'FORCEPwreset',
            'node_type': 'Type',
            'url': 'URL',
            'utility_url': 'UTILITYUrl',
            'max_mount_points': 'MAXNUMMP',
            'auto_rename_file_spaces': 'AUTOFSRename',
            'keep_mount_points': 'KEEPMP',
            'max_transaction_group': 'TXNGroupmax',
            'data_write_path': 'DATAWritepath',
            'data_read_path': 'DATAReadpath',
            'target_level': 'TARGETLevel',
            'session_initiation': 'SESSIONINITiation',
            'session_ip': 'HLAddress',
            'session_port': 'LLAddress',
            'email': 'EMAILADdress',
            'deduplication': 'DEDUPlication',
            'backup_initiation': 'BACKUPINITiation',
            'repl_state': 'REPLState',
            'backup_repl_rule_default': 'BKREPLRuledefault',
            'archive_repl_rule_default': 'ARREPLRuledefault',
            'space_repl_rule_default': 'SPREPLRuledefault',
            'recover_damaged': 'RECOVERDamaged',
            'role_override': 'ROLEOVERRIDE',
            'auth_method': 'AUTHentication',
            'session_security': 'SESSIONSECurity',
            'split_large_objects': 'SPLITLARGEObjects',
            'min_extent_size': 'MINIMUMExtentsize',
        }

        not_on_update = ['node_type', 'backup_repl_rule_default', 'archive_repl_rule_default', 'space_repl_rule_default']

        node_password = module.params.get('node_password')
        if node_password:
            module.warn(
                'The node_password field has encrypted data and may inaccurately report task is changed.'
            )

        options = f"{node_password if node_password else ''}"

        for opt in options_params.keys():
            value = module.params.get(opt)
            if value is not None and not (exists and opt in not_on_update):
                value = str(value)
                if value.lower() == 'true':
                    value = 'Yes'
                elif value.lower() == 'false':
                    value = 'No'
                if opt == 'min_extent_size':
                    value = f'{value}KB'
                options += f" {options_params[opt]}={value}"

        module.register(node, options, exists, existing)


if __name__ == "__main__":
    main()
