# Copyright 2018 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import hashlib

from oslo_config import cfg

from qinling import config as qinling_config
from qinling.utils import etcd_util

QINLING_CONF = None


def md5(file=None, content=None):
    hash_md5 = hashlib.md5()

    if file:
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    elif content:
        hash_md5.update(content)

    return hash_md5.hexdigest()


def get_etcd_client():
    """Use qinling's default CONF to connect to etcd."""
    global QINLING_CONF

    if not QINLING_CONF:
        QINLING_CONF = cfg.ConfigOpts()
        QINLING_CONF(args=[], project='qinling')
        QINLING_CONF.register_opts(qinling_config.etcd_opts,
                                   qinling_config.ETCD_GROUP)

    return etcd_util.get_client(conf=QINLING_CONF)
