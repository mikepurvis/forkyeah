import sys
from setuptools import find_packages, setup

install_requires = [
    'requests',
    'setuptools',
    'empy',
    'PyYAML',
]
long_description = '''
The purpose of this project is to facilitate the management of forks of upstream
repositories, where the fork is basically a tag or hash from upstream with a
one or more patches applied to it. These patches may be stored locally, or
fetched over the network for example using the diff link which GitHub supplies
for each PR, or from a gist.

The configuration file is `fork.yaml` and looks like the following:

```
upstream:
  repo: https://github.com/ros-controls/ros_control.git
  ref: 0.13.0

fork:
  repo: git@gitlab.yourcompany.com:forks/ros_control.git
  branch: fork-latest
  tag: fork-%Y%m%d-%H%M%S
  apply:
  - patch: https://github.com/ros-controls/ros_control/pull/301.diff
    name: "Upstream PR 301: CompositeController template."
  - patch: https://github.com/ros-controls/ros_control/commit/a65fb8cc.diff
    name: "Revert a65fb8cc to resolve merge conflicts."
    reverse: True
  - patch: https://github.com/ros-controls/ros_control/pull/302.diff
    name: "Upstream PR 302: Variadic Controller template."
  - patch: http://gitlab.clearpathrobotics.com/snippets/72/raw
    name: "Un-deprecate MultiInterfaceController."
```

The intention is that this `fork.yaml` config file is stored in an orphan branch
of the fork repo, and that that orphan branch is the default, so that when you
want to update it you simply make and commit changes (add, remove, reorder patches,
or change the version used as the starting point) and then rerun:

```
forkyeah
```

The tool will handle checking out the given baseline, switching to the fork-latest
branch, applying the patches, creating a new tag according to the template, and
pushing everything to the defined fork repo.
'''

setup(
    name='forkyeah',
    version='0.0.1',
    packages=['forkyeah'],
    install_requires=install_requires,
    author='Mike Purvis',
    author_email='mpurvis@clearpath.ai',
    maintainer='Mike Purvis',
    maintainer_email='mpurvis@clearpath.ai',
    description='forkyeah is a small tool for managing patches on an upstream git repo.',
    license='Apache 2.0',
    test_suite='test',
    entry_points={
        'console_scripts': [
            'forkyeah = forkyeah.cli:main',
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)
