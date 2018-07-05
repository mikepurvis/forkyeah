# Copyright 2018 Mike Purvis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from forkyeah.git import git
from forkyeah import DEFAULT_CONFIG_FILE

from datetime import datetime
import os
import requests
import yaml


def fetch_upstream(config, fork_branch):
    if git.remote('add', 'upstream', config['repo']) != 0:
        # Upstream already existed; just make sure we have the right URL.
        git.remote('set-url', 'upstream', config['repo'])

    # Switch to the branch that our fork is on.
    if git.checkout('-b', fork_branch) != 0:
        git.checkout(fork_branch)

    # Freshen the upstream and reset us to the current upstream ref, first
    # assuming it's a branch, then trying tag or hash.
    git.fetch('upstream')
    if git.reset('--hard', 'remotes/upstream/%s' % config['ref'], '--') != 0:
        git.reset('--hard', config['ref'])

def apply_patch(patch):
    diff = ''

    if patch['patch'].startswith('http'):
        # Patch is found at the supplied URL, fetch it.
        diff = requests.get(patch['patch']).text.encode('utf-8')
    reverse = patch.get('reverse', False)

    args = ['-3', '--whitespace=nowarn']
    if reverse:
       args.append('--reverse') 

    if git.apply(*args, stdin=diff) != 0:
        # Merge failed, show the current state.
        git.diff('--exit-code')
        return False

    git.add('-A')
    git.commit('-F', '-', stdin=patch['name'])
    return True

def tag_and_push(fork_config):
    tag_name = datetime.now().strftime(fork_config['tag'])
    git.tag(tag_name)
    git.push(fork_config['repo'], fork_config['branch'], '-f')
    git.push(fork_config['repo'], tag_name)
    
def main():
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        print("Config file %s not found in current directory, nothing to do!" % DEFAULT_CONFIG_FILE)
        return False

    with open(DEFAULT_CONFIG_FILE) as f:
        config = yaml.load(f)

    fetch_upstream(config['upstream'], config['fork']['branch'])

    for patch in config['fork']['apply']:
        if not apply_patch(patch):
            break
        print('')

    return tag_and_push(config['fork'])
