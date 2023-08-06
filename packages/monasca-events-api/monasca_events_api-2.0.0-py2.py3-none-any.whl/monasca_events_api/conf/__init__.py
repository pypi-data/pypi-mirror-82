# Copyright 2017 FUJITSU LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import pkgutil

from oslo_config import cfg
from oslo_log import log
from oslo_utils import importutils

LOG = log.getLogger(__name__)
CONF = cfg.CONF


def load_conf_modules():
    """Load all modules that contain configuration.

    Method iterates over modules of :py:mod:`monasca_events_api.conf`
    and imports only those that contain following methods:

    - list_opts (required by oslo_config.genconfig)
    - register_opts (required by :py:currentmodule:)

    """
    imported_modules = []
    for modname in _list_module_names():
        mod = importutils.import_module('monasca_events_api.conf.' + modname)
        required_funcs = ['register_opts', 'list_opts']
        for func in required_funcs:
            if not hasattr(mod, func):
                msg = ("The module 'monasca_events_api.conf.%s' should have a"
                       " '%s' function which returns"
                       " the config options."
                       % (modname, func))
                LOG.warning(msg)
            else:
                imported_modules.append(mod)

    LOG.debug('Found %d modules that contain configuration',
              len(imported_modules))

    return imported_modules


def _list_module_names():
    module_names = []
    package_path = os.path.dirname(os.path.abspath(__file__))
    for _, modname, ispkg in pkgutil.iter_modules(path=[package_path]):
        if not (modname == "opts" and ispkg):
            module_names.append(modname)
    return module_names


def register_opts(conf):
    """Register all conf modules opts.

    This method allows different modules to register
    opts according to their needs.

    """
    for mod in load_conf_modules():
        mod.register_opts(conf)


def list_opts():
    """List all conf modules opts.

    Goes through all conf modules and yields their opts

    """
    for mod in load_conf_modules():
        mod_opts = mod.list_opts()
        yield mod_opts[0], mod_opts[1]
