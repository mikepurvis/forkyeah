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

import subprocess

OPS='''add
apply
checkout
clean
commit
diff
fetch
push
remote
reset
tag'''

class Git:
    def _invoke(self, op, *args, **kwargs):
        stdin = kwargs.get('stdin', None)
        cmd = ('git', op) + args
        if stdin:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            p.communicate(stdin)
            return p.returncode
        else:
            return subprocess.call(cmd)

def make_git_op(op):
    def func(self, *args, **kwargs):
        return self._invoke(op, *args, **kwargs)
    return func

for op in OPS.split():
    setattr(Git, op, make_git_op(op))

git = Git()

