#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Creates a text file on remote host

description: This module creates a text file with specified content on remote host.

options:
    path:
        description: Path to the file to create on remote host
        required: true
        type: str
    content:
        description: Content to write to the file
        required: true
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create a file with content
  my_own_module:
    path: /tmp/test.txt
    content: "Hello, World!"
'''

RETURN = r'''
path:
    description: The path of the created file
    type: str
    returned: always
content:
    description: The content written to the file
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    # Check if file exists and has same content
    file_exists = os.path.exists(path)
    file_content = ''
    
    if file_exists:
        with open(path, 'r') as f:
            file_content = f.read()
    
    # If file doesn't exist or content differs, file needs to be changed
    if not file_exists or file_content != content:
        result['changed'] = True
        
        if module.check_mode:
            module.exit_json(**result)
        
        # Write content to file
        with open(path, 'w') as f:
            f.write(content)
        result['path'] = path
        result['content'] = content
    else:
        result['path'] = path
        result['content'] = content

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
