# Copyright 2012 Hewlett-Packard Development Company, L.P. All Rights Reserved.
#
# Author: Kiall Mac Innes <kiall@hpe.com>
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
import flask
from oslo_config import cfg

cfg.CONF.import_opt('enable_host_header', 'designate.api', group='service:api')


def factory(global_config, **local_conf):
    app = flask.Flask('designate.api.versions')

    @app.route('/', methods=['GET'])
    def version_list():
        if cfg.CONF['service:api'].enable_host_header:
            url_root = flask.request.url_root
        else:
            url_root = cfg.CONF['service:api'].api_base_uri

        return flask.jsonify({
            "versions": {
                "values": [{
                    'id': 'v2',
                    'status': 'CURRENT',
                    'links': [
                        {
                            'href': url_root.rstrip('/') + '/v2',
                            'rel': 'self',
                        }, {
                            'rel': 'help',
                            'href': 'https://docs.openstack.org/api-ref/dns'
                        }
                    ]
                }]
            }
        })

    return app
