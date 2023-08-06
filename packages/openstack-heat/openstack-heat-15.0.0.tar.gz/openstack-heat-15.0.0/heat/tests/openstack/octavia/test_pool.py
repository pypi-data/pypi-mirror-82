#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from unittest import mock
import yaml

from osc_lib import exceptions

from heat.common import exception
from heat.common.i18n import _
from heat.common import template_format
from heat.engine.resources.openstack.octavia import pool
from heat.tests import common
from heat.tests.openstack.octavia import inline_templates
from heat.tests import utils


class PoolTest(common.HeatTestCase):

    def test_resource_mapping(self):
        mapping = pool.resource_mapping()
        self.assertEqual(pool.Pool,
                         mapping['OS::Octavia::Pool'])

    def _create_stack(self, tmpl=inline_templates.POOL_TEMPLATE):
        self.t = template_format.parse(tmpl)
        self.stack = utils.parse_stack(self.t)
        self.pool = self.stack['pool']

        self.octavia_client = mock.MagicMock()
        self.pool.client = mock.MagicMock(return_value=self.octavia_client)

        self.pool.client_plugin().client = mock.MagicMock(
            return_value=self.octavia_client)

    def test_validate_no_cookie_name(self):
        tmpl = yaml.safe_load(inline_templates.POOL_TEMPLATE)
        sp = tmpl['resources']['pool']['properties']['session_persistence']
        sp['type'] = 'APP_COOKIE'
        self._create_stack(tmpl=yaml.safe_dump(tmpl))

        msg = _('Property cookie_name is required when '
                'session_persistence type is set to APP_COOKIE.')
        self.assertRaisesRegex(exception.StackValidationFailed,
                               msg, self.pool.validate)

    def test_validate_source_ip_cookie_name(self):
        tmpl = yaml.safe_load(inline_templates.POOL_TEMPLATE)
        sp = tmpl['resources']['pool']['properties']['session_persistence']
        sp['type'] = 'SOURCE_IP'
        sp['cookie_name'] = 'cookie'
        self._create_stack(tmpl=yaml.safe_dump(tmpl))

        msg = _('Property cookie_name must NOT be specified when '
                'session_persistence type is set to SOURCE_IP.')
        self.assertRaisesRegex(exception.StackValidationFailed,
                               msg, self.pool.validate)

    def test_create(self):
        self._create_stack()
        self.octavia_client.pool_show.side_effect = [
            {'provisioning_status': 'PENDING_CREATE'},
            {'provisioning_status': 'PENDING_CREATE'},
            {'provisioning_status': 'ACTIVE'},
        ]
        self.octavia_client.pool_create.side_effect = [
            exceptions.Conflict(409), {'pool': {'id': '1234'}}
        ]
        expected = {
            'pool': {
                'name': 'my_pool',
                'description': 'my pool',
                'session_persistence': {
                    'type': 'HTTP_COOKIE'
                },
                'lb_algorithm': 'ROUND_ROBIN',
                'listener_id': '123',
                'loadbalancer_id': 'my_lb',
                'protocol': 'HTTP',
                'admin_state_up': True,
                'tls_enabled': False,
            }
        }

        props = self.pool.handle_create()

        self.assertFalse(self.pool.check_create_complete(props))
        self.octavia_client.pool_create.assert_called_with(json=expected)
        self.assertFalse(self.pool.check_create_complete(props))
        self.octavia_client.pool_create.assert_called_with(json=expected)
        self.assertFalse(self.pool.check_create_complete(props))
        self.assertTrue(self.pool.check_create_complete(props))

    def test_create_missing_properties(self):
        for prop in ('lb_algorithm', 'listener', 'protocol'):
            tmpl = yaml.safe_load(inline_templates.POOL_TEMPLATE)
            del tmpl['resources']['pool']['properties']['loadbalancer']
            del tmpl['resources']['pool']['properties'][prop]
            self._create_stack(tmpl=yaml.safe_dump(tmpl))
            if prop == 'listener':
                self.assertRaises(exception.PropertyUnspecifiedError,
                                  self.pool.validate)
            else:
                self.assertRaises(exception.StackValidationFailed,
                                  self.pool.validate)

    def test_show_resource(self):
        self._create_stack()
        self.pool.resource_id_set('1234')
        self.octavia_client.pool_show.return_value = {'id': '1234'}

        self.assertEqual(self.pool._show_resource(), {'id': '1234'})

        self.octavia_client.pool_show.assert_called_with('1234')

    def test_update(self):
        self._create_stack()
        self.pool.resource_id_set('1234')
        self.octavia_client.pool_show.side_effect = [
            {'provisioning_status': 'PENDING_UPDATE'},
            {'provisioning_status': 'PENDING_UPDATE'},
            {'provisioning_status': 'ACTIVE'},
        ]
        self.octavia_client.pool_set.side_effect = [
            exceptions.Conflict(409), None]
        prop_diff = {
            'admin_state_up': False,
            'name': 'your_pool',
            'lb_algorithm': 'SOURCE_IP'
        }

        prop_diff = self.pool.handle_update(None, None, prop_diff)

        self.assertFalse(self.pool.check_update_complete(prop_diff))
        self.assertFalse(self.pool._update_called)
        self.octavia_client.pool_set.assert_called_with(
            '1234', json={'pool': prop_diff})
        self.assertFalse(self.pool.check_update_complete(prop_diff))
        self.assertTrue(self.pool._update_called)
        self.octavia_client.pool_set.assert_called_with(
            '1234', json={'pool': prop_diff})
        self.assertFalse(self.pool.check_update_complete(prop_diff))
        self.assertTrue(self.pool.check_update_complete(prop_diff))

    def test_delete(self):
        self._create_stack()
        self.pool.resource_id_set('1234')
        self.octavia_client.pool_show.side_effect = [
            {'provisioning_status': 'PENDING_DELETE'},
            {'provisioning_status': 'PENDING_DELETE'},
            {'provisioning_status': 'DELETED'},
        ]
        self.octavia_client.pool_delete.side_effect = [
            exceptions.Conflict(409),
            None]

        self.pool.handle_delete()

        self.assertFalse(self.pool.check_delete_complete(None))
        self.assertFalse(self.pool._delete_called)
        self.assertFalse(self.pool.check_delete_complete(None))
        self.assertTrue(self.pool._delete_called)
        self.octavia_client.pool_delete.assert_called_with('1234')
        self.assertTrue(self.pool.check_delete_complete(None))

    def test_delete_not_found(self):
        self._create_stack()
        self.pool.resource_id_set('1234')
        self.octavia_client.pool_show.side_effect = [
            {'provisioning_status': 'PENDING_DELETE'},
        ]
        self.octavia_client.pool_delete.side_effect = [
            exceptions.Conflict(409),
            exceptions.NotFound(404)]

        self.pool.handle_delete()

        self.assertFalse(self.pool.check_delete_complete(None))
        self.assertFalse(self.pool._delete_called)
        self.octavia_client.pool_delete.assert_called_with('1234')
        self.assertTrue(self.pool.check_delete_complete(None))

    def test_delete_failed(self):
        self._create_stack()
        self.pool.resource_id_set('1234')
        self.octavia_client.pool_delete.side_effect = (
            exceptions.Unauthorized(401))

        self.pool.handle_delete()
        self.assertRaises(exceptions.Unauthorized,
                          self.pool.check_delete_complete, None)
