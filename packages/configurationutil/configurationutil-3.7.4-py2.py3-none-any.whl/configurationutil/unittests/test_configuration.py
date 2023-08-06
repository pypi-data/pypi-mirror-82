# encoding: utf-8

import os
import json
import shutil
import unittest
from fdutil.path_tools import pop_path
from configurationutil import configuration
from jsonschema import SchemaError, ValidationError
from fdutil.parse_json import write_json_to_file


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.0'
        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()  # Calling this here to ensure config re-inited following deletion in cleanup!

        self.cleanup_path = pop_path(pop_path(configuration.Configuration().config_path)) + os.sep
        self.addCleanup(self.clean)

    def tearDown(self):
        pass

    def clean(self):
        try:
            shutil.rmtree(self.cleanup_path)

        except OSError:
            pass

    # Instantiation
    def test_instantiation(self):
        configuration.APP_NAME = u'PyTestApp2'
        self.cfg2 = configuration.Configuration()

        self.assertEqual(self.cfg1, self.cfg2,
                         msg=u'Configuration instantiation: Classes do not match, should be singleton!')

        self.assertEqual(self.cfg1.app_name, self.cfg2.app_name,
                         msg=u'Configuration instantiation: app_name does not match!')

        self.assertEqual(self.cfg1.app_version, self.cfg2.app_version,
                         msg=u'Configuration instantiation: app_version does not match!')

        self.assertEqual(self.cfg1.app_author, self.cfg2.app_author,
                         msg=u'Configuration instantiation: app_author does not match!')

    def test_instantiation_invalid_version(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'invalid_version.2'

        with self.assertRaises(ValueError):
            self.cfg1 = configuration.Configuration()
            self.cfg1.__init__()

    def test_instantiation_invalid_master_config(self):

        # make config invalid
        pth = self.cfg1.config_path

        with open(os.path.join(pth, u'master_config.json')) as f:
            cfg = json.load(f)

        fn, ext = u'master_config.json'.split(u'.')

        cfg[u'invalid_node'] = u'invalid_node_data'

        write_json_to_file(content=cfg,
                           output_dir=pth,
                           filename=fn,
                           file_ext=ext)

        with self.assertRaises(ValidationError):
            self.cfg1 = configuration.Configuration()
            self.cfg1.__init__()

    # Registration
    def test_check_registration(self):

        self.cfg1.register(config=u'test_check_registration',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_check_registration'))
        self.assertFalse(self.cfg1.check_registration(u'test_check_registration_missing'))

    def test_register(self):

        self.cfg1.register(config=u'test_register',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_register'))

    def test_register_valid_schema(self):

        self.cfg1.register(config=u'test_register_valid_schema',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_register_valid_schema'))

    def test_register_invalid_schema(self):
        with self.assertRaises(SchemaError):
            self.cfg1.register(config=u'test_invalid_schema',
                               config_type=configuration.CONST.json,
                               template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                               schema=os.path.join(pop_path(__file__), u'resources', u'invalid_schema.json'))

    def test_register_invalid_config_template(self):
        with self.assertRaises(ValidationError):
            self.cfg1.register(config=u'test_invalid_template',
                               config_type=configuration.CONST.json,
                               template=os.path.join(pop_path(__file__), u'resources', u'invalid_template.json'),
                               schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

    def test_unregister(self):

        self.cfg1.register(config=u'test_unregister',
                           config_type=configuration.CONST.json)

        self.cfg1.unregister(config=u'test_unregister')

        self.assertFalse(self.cfg1.check_registration(u'test_unregister'))

    # Getters
    def test_get(self):
        self.cfg1.register(config=u'test_get',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_get'] = {u'testitem': u'Get some config!'}

        self.assertEqual(self.cfg1[u'test_get.testitem'], u'Get some config!',
                         u'Get failed as we cannot retrieve the value we tried to set!')

    def test_get_multi_key(self):
        self.cfg1.register(config=u'test_get_multi_key',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_get_multi_key'] = {
            u'data': {
                u'testitem': u'Get some data config!'
            }
        }

        self.assertEqual(self.cfg1[u'test_get_multi_key.data.testitem'], u'Get some data config!',
                         u'Get failed as we cannot retrieve the nested value we tried to set!')

        self.cfg1[u'test_get_multi_key'] = {
            u'data': {
                u'test_data': {
                    u'item1': u'Get some data config 2!'
                }
            }
        }

        self.assertEqual(self.cfg1[u'test_get_multi_key.data.test_data.item1'], u'Get some data config 2!',
                         u'Get failed as we cannot retrieve the multiple nested value we tried to set!')

    def test_get_multi_key_dict(self):
        self.cfg1.register(config=u'test_get_multi_key',
                           config_type=configuration.CONST.json)

        test_data = {
            u'a1': [1, 2, 3],
            u'a2': 123,
            u'a3': u'some data',
            u'a4': {u'b1': u'b1 data', u'b2': u'b2 data'}
        }

        self.cfg1[u'test_get_multi_key'] = {
            u'data': {
                u'item3': test_data
            }
        }

        self.assertDictEqual(self.cfg1[u'test_get_multi_key.data.item3'], test_data,
                             u'Get failed as we cannot retrieve the nested dict value we tried to set!')

        self.assertEqual(self.cfg1[u'test_get_multi_key.data.item3.a4.b2'], u'b2 data',
                         u'Get failed as we cannot retrieve the value nested in the dict we tried to set!')

    def test_get_all_items(self):
        self.cfg1.register(config=u'test_get_all_items',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_get_all_items'] = {
            u'item': u'Get some config!',
            u'item2': u'Get some more config!'
        }

        expected_output = {u'item': u'Get some config!',
                           u'item2': u'Get some more config!'}

        self.assertDictEqual(self.cfg1[u'test_get_all_items'], expected_output)

    def test_get_missing_item(self):
        self.cfg1.register(config=u'test_get_missing_item',
                           config_type=configuration.CONST.json)

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_get_missing_item.testitem']

    def test_get_master_config_unavailable(self):
        with self.assertRaises(KeyError):
            _ = self.cfg1[u'master_config']

    def test_get_config_file_removed(self):
        self.cfg1.register(config=u'test_get_remove_file',
                           config_type=configuration.CONST.json)

        cfg_type = configuration.CFG_TYPES.get(configuration.CONST.json)
        os.remove(os.path.join(self.cfg1.config_path, u'test_get_remove_file.' + cfg_type.get(u'ext')))

        self.cfg1[u'test_get_remove_file'] = {u'item': u'Get some config!'}

        self.assertEqual(self.cfg1[u'test_get_remove_file.item'], u'Get some config!',
                         u'Get failed as we cannot retrieve the value we tried to set!')

    # Setters
    def test_set(self):
        self.cfg1.register(config=u'test_set',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_set.testitem'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_set.testitem'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

    def test_set_multi_item(self):
        self.cfg1.register(config=u'test_set_multi_item',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_set_multi_item.data.item1'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_set_multi_item.data.item1'], u'Set some config!',
                         u'Set multi item failed as we cannot retrieve the value we tried to set!')

        self.cfg1[u'test_set_multi_item.data.more_data.item1'] = u'Set some more config!'

        self.assertEqual(self.cfg1[u'test_set_multi_item.data.more_data.item1'], u'Set some more config!',
                         u'Set multi item more data failed as we cannot retrieve the value we tried to set!')

    def test_set_multi_item_dict(self):
        self.cfg1.register(config=u'test_set_multi_item_dict',
                           config_type=configuration.CONST.json)

        test_data = {
            u'a': u'a _data',
            u'b': 123,
            u'c': [u'this', u'is', u'a', u'list'],
            u'd': {u'nested': 456, u'data': 789}
        }

        self.cfg1[u'test_set_multi_item_dict.data.item1'] = test_data

        self.assertEqual(self.cfg1[u'test_set_multi_item_dict.data.item1'], test_data,
                         u'Set multi item dict failed as we cannot retrieve the value we tried to set!')

        self.assertListEqual(self.cfg1[u'test_set_multi_item_dict.data.item1.c'], [u'this', u'is', u'a', u'list'],
                             u'Set multi item get list failed as we cannot retrieve the value we tried to set!')

        self.assertEqual(self.cfg1[u'test_set_multi_item_dict.data.item1.d.nested'], 456,
                         u'Set multi item dict failed as we cannot retrieve the value we '
                         u'tried to set in the nested dict!')

    def test_set_all_items(self):
        self.cfg1.register(config=u'test_set_all_items',
                           config_type=configuration.CONST.json)

        full_cfg = {
            u'key1': u'value1',
            u'key2': u'value2'
        }

        self.cfg1[u'test_set_all_items'] = full_cfg

        self.assertEqual(self.cfg1[u'test_set_all_items.key1'], u'value1',
                         u'Set failed as we cannot retrieve the first value we tried to set!')

        self.assertEqual(self.cfg1[u'test_set_all_items.key2'], u'value2',
                         u'Set failed as we cannot retrieve the second value we tried to set!')

        self.assertDictEqual(self.cfg1[u'test_set_all_items'], full_cfg,
                             u'Set failed as we cannot retrieve the full config we tried to set!')

    def test_set_invalid_config(self):

        # Register a config that has a schema
        self.cfg1.register(config=u'test_set_invalid_config',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_set_invalid_config'))

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_set_invalid_config.cfg2']

        # Try and add an invalid config value
        with self.assertRaises(ValidationError):
            self.cfg1[u'test_set_invalid_config.cfg2'] = 123

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_set_invalid_config.cfg2']

    def test_set_update_existing(self):
        self.cfg1.register(config=u'test_set_update_existing',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_set_update_existing.testitem'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_set_update_existing.testitem'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        self.cfg1[u'test_set_update_existing.testitem'] = u'Update some config!'

        self.assertEqual(self.cfg1[u'test_set_update_existing.testitem'], u'Update some config!',
                         u'Set failed as we cannot retrieve the value we tried to update!')

    def test_set_update_existing_multi_item(self):
        self.cfg1.register(config=u'test_set_update_existing_multi_item',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_set_update_existing_multi_item.data.item1'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_set_update_existing_multi_item.data.item1'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        self.cfg1[u'test_set_update_existing_multi_item.data.item1'] = u'Update some config!'

        self.assertEqual(self.cfg1[u'test_set_update_existing_multi_item.data.item1'], u'Update some config!',
                         u'Set failed as we cannot retrieve the value we tried to update!')

    def test_set_update_existing_multi_item_dict(self):
        self.cfg1.register(config=u'test_set_update_existing_multi_item_dict',
                           config_type=configuration.CONST.json)

        test_data = {
            u'a': u'a _data',
            u'b': 123,
            u'c': [u'this', u'is', u'a', u'list'],
            u'd': {u'nested': 456, u'data': 789}
        }

        self.cfg1[u'test_set_update_existing_multi_item_dict.data.item1'] = test_data

        self.assertDictEqual(self.cfg1[u'test_set_update_existing_multi_item_dict.data.item1'], test_data,
                             u'Set multi item dict failed as we cannot retrieve the value we tried to set!')

        self.cfg1[u'test_set_update_existing_multi_item_dict.data.item1.a'] = u'Update A data'

        self.assertEqual(self.cfg1[u'test_set_update_existing_multi_item_dict.data.item1.a'], u'Update A data',
                         u'Set failed as we cannot retrieve the value we tried to update!')

        self.cfg1[u'test_set_update_existing_multi_item_dict.data.item1.b'] = {u'update': 123}

        self.assertDictEqual(self.cfg1[u'test_set_update_existing_multi_item_dict.data.item1.b'], {u'update': 123},
                             u'Set failed as we cannot retrieve the value we tried to update!')

    # Deleter
    def test_del(self):
        self.cfg1.register(config=u'test_del',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_del.testitem'] = u'Del some config!'

        del self.cfg1[u'test_del.testitem']

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_del.testitem']

    def test_del_multi_item(self):
        self.cfg1.register(config=u'test_del_multi_item',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_del_multi_item'] = {
            u'data': {
                u'item1': u'Del some config!',
                u'item2': u'Del this item'
            }
        }

        del self.cfg1[u'test_del_multi_item.data.item2']

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_del_multi_item.data.item2']

        self.assertDictEqual(self.cfg1[u'test_del_multi_item.data'], {u'item1': u'Del some config!'},
                             u'Failed to check the dict where we deleted an item')

    def test_del_multi_item_dict(self):
        self.cfg1.register(config=u'test_del_multi_item_dict',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_del_multi_item_dict'] = {
            u'data': {
                u'item1': u'Del some config!',
                u'data_dict': {
                    u'a': u'Del some config!',
                    u'b': u'Del this item'
                }
            }
        }

        del self.cfg1[u'test_del_multi_item_dict.data.data_dict']

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_del_multi_item_dict.data.data_dict']

        self.assertDictEqual(self.cfg1[u'test_del_multi_item_dict.data'], {u'item1': u'Del some config!'},
                             u'Failed to check the dict where we deleted an item')

    def test_del_all_items(self):
        self.cfg1.register(config=u'test_del_all_items',
                           config_type=configuration.CONST.json)

        with self.assertRaises(ValueError):
            del self.cfg1[u'test_del_all_items']

    def test_del_invalid_config(self):

        # Register a config that has a schema
        self.cfg1.register(config=u'test_set_invalid_config',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_set_invalid_config'))

        self.assertEqual(self.cfg1[u'test_set_invalid_config.cfg1'], {})

        # Try and add an invalid config value
        with self.assertRaises(ValidationError):
            del self.cfg1[u'test_set_invalid_config.cfg1']

        self.assertEqual(self.cfg1[u'test_set_invalid_config.cfg1'], {})

    # Find
    def test_find(self):

        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.testitem1'] = {u'A': 1, u'B': 2, u'C': 3}
        self.cfg1[u'test_find.testitem2'] = {u'A': 1, u'B': 5, u'C': 6}
        self.cfg1[u'test_find.testitem3'] = {u'A': 7, u'B': 2, u'C': 6}

        filters = [(u'C', 6)]

        expected_output = {
            u'testitem2': {u'A': 1, u'B': 5, u'C': 6},
            u'testitem3': {u'A': 7, u'B': 2, u'C': 6}
        }

        self.assertEqual(self.cfg1.find(u'test_find', filters), expected_output,
                         u'Find C = 6 failed!')

    def test_find_multi_item(self):

        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.test'] = {}
        self.cfg1[u'test_find.test.item1'] = {u'A': 1, u'B': 2, u'C': 3}
        self.cfg1[u'test_find.test.item2'] = {u'A': 1, u'B': 5, u'C': 6}
        self.cfg1[u'test_find.test.item3'] = {u'A': 7, u'B': 2, u'C': 6}

        filters = [(u'C', 6)]

        expected_output = {
            u'item2': {u'A': 1, u'B': 5, u'C': 6},
            u'item3': {u'A': 7, u'B': 2, u'C': 6}
        }

        self.assertEqual(self.cfg1.find(u'test_find', filters), {},
                         u'Find should not recurse')

        self.assertEqual(self.cfg1.find(u'test_find.test', filters), expected_output,
                         u'Find not returning correct answers for multi item depth')

    def test_find_no_filters(self):

        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.testitem1'] = {u'A': 1, u'B': 2, u'C': 3}
        self.cfg1[u'test_find.testitem2'] = {u'A': 1, u'B': 5, u'C': 6}
        self.cfg1[u'test_find.testitem3'] = {u'A': 7, u'B': 2, u'C': 6}

        self.assertEqual(self.cfg1.find(u'test_find'), self.cfg1[u'test_find'],
                         u'Find no filters failed')

    def test_find_no_filters_multi_item(self):

        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.testitem1'] = {u'A': 1, u'B': 2, u'C': 3}
        self.cfg1[u'test_find.testitem2'] = {u'A': 1, u'B': 5, u'C': 6}
        self.cfg1[u'test_find.testitem3'] = {u'A': 7, u'B': 2, u'C': 6}

        self.assertEqual(self.cfg1.find(u'test_find.testitem1'), {u'A': 1, u'B': 2, u'C': 3},
                         u'Find no filters failed')

    def test_find_no_subkey(self):

        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.testitem1'] = 2
        self.cfg1[u'test_find.testitem2'] = 6
        self.cfg1[u'test_find.testitem3'] = {u'A': 7, u'B': 2, u'C': 6}

        msg = u'Find no key failed'

        filters = [(2, None)]
        filters2 = [(2, None), (6, None, u'OR')]
        filters3 = [(u'A', 7), (6, None, u'OR')]

        self.assertEqual(self.cfg1.find(u'test_find', filters), {u'testitem1': 2}, msg)
        self.assertEqual(self.cfg1.find(u'test_find', filters2), {u'testitem1': 2, u'testitem2': 6}, msg)
        self.assertEqual(self.cfg1.find(u'test_find', filters3), {u'testitem2': 6,
                                                                  u'testitem3': {u'A': 7, u'B': 2, u'C': 6}}, msg)

    def test_find_invalid_key(self):

        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.testitem1'] = {u'A': 1, u'B': 2, u'C': 3}
        self.cfg1[u'test_find.testitem2'] = {u'A': 1, u'B': 5, u'C': 6}
        self.cfg1[u'test_find.testitem3'] = {u'A': 7, u'B': 2, u'C': 6}

        filters = [(u'C', 6)]

        with self.assertRaises(KeyError):
            self.cfg1.find(u'test_find_invalid', filters)

    def test_find_invalid_key_multi_item(self):
        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.testitem1'] = {u'A': 1, u'B': 2, u'C': 3}
        self.cfg1[u'test_find.testitem2'] = {u'A': 1, u'B': 5, u'C': 6}
        self.cfg1[u'test_find.testitem3'] = {u'A': 7, u'B': 2, u'C': 6}

        filters = [(u'C', 6)]

        with self.assertRaises(KeyError):
            self.cfg1.find(u'test_find.testitem4', filters)

        with self.assertRaises(KeyError):
            self.cfg1.find(u'test_find.testitem1.A', filters)

    # Versions
    def test_validate_version(self):
        self.assertTrue(configuration.Configuration.validate_version(u'1'), u'Valid version failed validation')
        self.assertTrue(configuration.Configuration.validate_version(u'1.2'), u'Valid version failed validation')
        self.assertTrue(configuration.Configuration.validate_version(u'1.2.3'), u'Valid version failed validation')
        self.assertTrue(configuration.Configuration.validate_version(u'1.2.0'), u'Valid version failed validation')

        self.assertFalse(configuration.Configuration.validate_version(u'1.2.3.0'), u'Invalid version passed validation')
        self.assertFalse(configuration.Configuration.validate_version(u'invalid'), u'Invalid version passed validation')
        self.assertFalse(configuration.Configuration.validate_version(u'a.b.c'), u'Invalid version passed validation')
        self.assertFalse(configuration.Configuration.validate_version(u'a.2.3'), u'Invalid version passed validation')
        self.assertFalse(configuration.Configuration.validate_version(u'1.b.3'), u'Invalid version passed validation')

    def test_normalise_version(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.assertEqual(u'1', self.cfg1.normalise_version(u'1'), u'Normalise version failed')
        self.assertEqual(u'1', self.cfg1.normalise_version(u'1.0'), u'Normalise version failed')
        self.assertEqual(u'1', self.cfg1.normalise_version(u'1.0.0'), u'Normalise version failed')
        self.assertEqual(u'0.1', self.cfg1.normalise_version(u'0.1'), u'Normalise version failed')
        self.assertEqual(u'0.1', self.cfg1.normalise_version(u'0.1.0'), u'Normalise version failed')
        self.assertEqual(u'0.0.1', self.cfg1.normalise_version(u'0.0.1'), u'Normalise version failed')
        self.assertEqual(u'1.10', self.cfg1.normalise_version(u'1.10'), u'Normalise version failed')
        self.assertEqual(u'1.10', self.cfg1.normalise_version(u'1.10.0'), u'Normalise version failed')

    def test_split_version(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.assertEqual([1, 2, 3], self.cfg1.split_version(u'1.2.3'), u'Split version failed')
        self.assertEqual([1, 10, 3], self.cfg1.split_version(u'1.10.3'), u'Split version failed')
        self.assertEqual([1, 2, 0], self.cfg1.split_version(u'1.2.0'), u'Split version failed')

    def test_split_versions(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        versions = [
            u'1.2.3',
            u'1.10.3',
            u'1.2.0'
        ]

        expected_output = [
            [1, 2, 3],
            [1, 10, 3],
            [1, 2, 0]
        ]

        self.assertEqual(expected_output, self.cfg1.split_versions(versions), u'Split versions failed')

    def test_join_version(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.assertEqual(u'1.2.3', self.cfg1.join_version([1, 2, 3]), u'Join version failed')
        self.assertEqual(u'1.10.3', self.cfg1.join_version([1, 10, 3]), u'Join version failed')
        self.assertEqual(u'1.2.0', self.cfg1.join_version([1, 2, 0]), u'Join version failed')

    def test_join_versions(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        versions = [
            [1, 2, 3],
            [1, 10, 3],
            [1, 2, 0]
        ]

        expected_output = [
            u'1.2.3',
            u'1.10.3',
            u'1.2.0'
        ]

        self.assertEqual(expected_output, self.cfg1.join_versions(versions), u'Join versions failed')

    def test_get_previous_versions(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        expected_output = [u'1']

        self.assertEqual(expected_output, self.cfg1.previous_versions,
                         u'Get previous versions does not match')

    def test_get_last_version(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        expected_output = u'1.1'

        self.assertEqual(self.cfg1.last_version, expected_output,
                         u'Get last version does not match')

    def test_get_last_version_none(self):

        expected_output = None

        self.assertEqual(self.cfg1.last_version, expected_output,
                         u'Get last version none does not match')

    # Upgrade
    def test_upgrade_instantiation(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.assertEqual(self.cfg1.app_name, configuration.APP_NAME,
                         msg=u'Configuration instantiation: app_name does not match!')

        self.assertEqual(self.cfg1.app_version, u'1.1',
                         msg=u'Configuration instantiation: app_version does not match!')

        self.assertEqual(self.cfg1.app_author, configuration.APP_AUTHOR,
                         msg=u'Configuration instantiation: app_author does not match!')

    def test_upgrade(self):
        self.cfg1.register(config=u'test_upgrade',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade'))

        self.cfg1[u'test_upgrade.new_item'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_upgrade.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade'))

        self.assertEqual(self.cfg1[u'test_upgrade.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

    def test_upgrade_upgradable_false(self):
        self.cfg1.register(config=u'test_upgrade_upgradable_false',
                           config_type=configuration.CONST.json,
                           upgradable=False)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_upgradable_false'))

        self.cfg1[u'test_upgrade_upgradable_false.new_item'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_upgrade_upgradable_false.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_upgradable_false',
                           config_type=configuration.CONST.json,
                           upgradable=False)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_upgradable_false'))

        self.assertEqual(self.cfg1[u'test_upgrade_upgradable_false'], {},
                         u'Config not reset to template when upgradeable=False!')

    def test_upgrade_template(self):
        self.cfg1.register(config=u'test_upgrade_template',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template'))

        self.cfg1[u'test_upgrade_template.new_item'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_upgrade_template.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'upgrade_template.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template'))

        self.assertEqual(self.cfg1[u'test_upgrade_template.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_upgrade_template.template_item']

    def test_upgrade_template_nested(self):
        self.cfg1.register(config=u'test_upgrade_template_nested',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'upgrade_template_nested.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_nested'))

        self.cfg1[u'test_upgrade_template_nested.c.y.p'] = u'ax'
        self.cfg1[u'test_upgrade_template_nested.c.y.r'] = u'ab'
        self.cfg1[u'test_upgrade_template_nested.d'] = 5
        self.cfg1[u'test_upgrade_template_nested.f'] = [123, 456, 789, 777, 987]

        self.assertEqual(self.cfg1[u'test_upgrade_template_nested'],
                         {
                             u'a': 1,
                             u'b': 2,
                             u'c': {
                                 u'x': 5,
                                 u'y': {
                                     u'p': u'ax',
                                     u'q': u'bb',
                                     u'r': u'ab'
                                 },
                                 u'z': 7
                             },
                             u'd': 5,
                             u'f': [
                                 123,
                                 456,
                                 789,
                                 777,
                                 987
                             ]
                         },
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_nested',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources',
                                                 u'upgrade_template_nested_update.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_nested'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_nested'],
                         {
                             u'a': 1,
                             u'b': 2,
                             u'c': {
                                 u'x': 5,
                                 u'y': {
                                     u'p': u'ax',
                                     u'q': u'bb',
                                     u'r': u'ab'
                                 },
                                 u'z': 7
                             },
                             u'd': 5,
                             u'f': [
                                 123,
                                 456,
                                 789,
                                 777,
                                 987
                             ]
                         },
                         u'Set failed as we cannot retrieve the value we tried to set!')

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_upgrade_template_nested.template_item']

    def test_upgrade_template_merge(self):
        self.cfg1.register(config=u'test_upgrade_template_merge',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_merge'))

        self.cfg1[u'test_upgrade_template_merge.new_item'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_upgrade_template_merge.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_merge',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'upgrade_template.json'),
                           upgrade_merge_template=True)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_merge'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_merge.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        self.assertEqual(self.cfg1[u'test_upgrade_template_merge.template_item'], u'template data',
                         u'Set failed as we cannot retrieve the value we tried to set!')

    def test_upgrade_template_merge_nested(self):
        self.cfg1.register(config=u'test_upgrade_template_nested',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'upgrade_template_nested.json'),
                           upgrade_merge_template=True)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_nested'))

        self.cfg1[u'test_upgrade_template_nested.c.y.p'] = u'ax'
        self.cfg1[u'test_upgrade_template_nested.c.y.r'] = u'ab'
        self.cfg1[u'test_upgrade_template_nested.d'] = 5
        self.cfg1[u'test_upgrade_template_nested.f'] = [123, 456, 789, 777, 987]

        self.assertEqual(self.cfg1[u'test_upgrade_template_nested'],
                         {
                             u'a': 1,
                             u'b': 2,
                             u'c': {
                                 u'x': 5,
                                 u'y': {
                                     u'p': u'ax',
                                     u'q': u'bb',
                                     u'r': u'ab'
                                 },
                                 u'z': 7
                             },
                             u'd': 5,
                             u'f': [
                                 123,
                                 456,
                                 789,
                                 777,
                                 987
                             ]
                         },
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_nested',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources',
                                                 u'upgrade_template_nested_update.json'),
                           upgrade_merge_template=True)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_nested'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_nested'],
                         {
                             u'a': 1,
                             u'b': 7,
                             u'c': {
                                 u'x': 5,
                                 u'y': {
                                     u'p': u'ax',
                                     u'q': u'cc',
                                     u'r': u'ab'
                                 },
                                 u'z': 0
                             },
                             u'd': 5,
                             u'e': 88,
                             u'f': [
                                 123,
                                 456,
                                 789,
                                 777,
                                 987
                             ]
                         },
                         u'Set failed as we cannot retrieve the value we tried to set!')

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_upgrade_template_nested.template_item']

    def test_upgrade_template_carry_forward(self):
        self.cfg1.register(config=u'test_upgrade_template_carry_forward',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_carry_forward'))

        self.cfg1[u'test_upgrade_template_carry_forward.new_item'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_upgrade_template_carry_forward.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        self.cfg1[u'test_upgrade_template_carry_forward.template_item'] = u'Set some config in the template!'

        self.assertEqual(self.cfg1[u'test_upgrade_template_carry_forward.template_item'],
                         u'Set some config in the template!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_carry_forward',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'upgrade_template.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_carry_forward'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_carry_forward.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        self.assertEqual(self.cfg1[u'test_upgrade_template_carry_forward.template_item'],
                         u'Set some config in the template!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

    def test_upgrade_schema(self):
        self.cfg1.register(config=u'test_upgrade_schema',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_schema'))

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_schema',
                           config_type=configuration.CONST.json,
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_schema'))

        self.assertEqual(self.cfg1[u'test_upgrade_schema.cfg1'], {},
                         u'Upgrade: Add required param failed to keep existing param')

    def test_upgrade_schema_remove_param(self):
        self.cfg1.register(config=u'test_upgrade_schema_remove_param',
                           config_type=configuration.CONST.json,
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_only.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_schema_remove_param'))

        self.cfg1[u'test_upgrade_schema_remove_param.cfg1'] = {}

        self.assertEqual(self.cfg1[u'test_upgrade_schema_remove_param.cfg1'], {},
                         u'Upgrade: Add required param failed to keep existing param')

        self.cfg1[u'test_upgrade_schema_remove_param.cfg2'] = u'some data'

        self.assertEqual(self.cfg1[u'test_upgrade_schema_remove_param.cfg2'], u'some data',
                         u'Upgrade: Add required param failed to keep existing param')

        with self.assertRaises(ValidationError):
            self.cfg1[u'test_upgrade_schema_remove_param.cfg3'] = u'some more data'

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_schema_remove_param',
                           config_type=configuration.CONST.json,
                           schema=os.path.join(pop_path(__file__), u'resources',
                                               u'valid_schema_only_change_remove.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_schema_remove_param'))

        with self.assertRaises(KeyError):
            _ = self.cfg1[u'test_upgrade_schema_remove_param.cfg1']

        self.assertEqual(self.cfg1[u'test_upgrade_schema_remove_param.cfg2'], u'some data',
                         u'Upgrade: Add required param failed to keep existing param')

        self.cfg1[u'test_upgrade_schema_remove_param.cfg3'] = u'some more data'

        self.assertEqual(self.cfg1[u'test_upgrade_schema_remove_param.cfg3'], u'some more data',
                         u'Upgrade: Add required param failed to keep existing param')

    def test_upgrade_schema_param_carried_forward(self):
        self.cfg1.register(config=u'test_upgrade_schema_param_carried_forward',
                           config_type=configuration.CONST.json,
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_only.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_schema_param_carried_forward'))

        self.cfg1[u'test_upgrade_schema_param_carried_forward.cfg1'] = {}

        self.assertEqual(self.cfg1[u'test_upgrade_schema_param_carried_forward.cfg1'], {},
                         u'Upgrade: Add required param failed to keep existing param')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_schema_param_carried_forward',
                           config_type=configuration.CONST.json,
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_only.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_schema_param_carried_forward'))

        self.assertEqual(self.cfg1[u'test_upgrade_schema_param_carried_forward.cfg1'], {},
                         u'Upgrade: Add required param failed to keep existing param')

    def test_upgrade_template_schema(self):
        self.cfg1.register(config=u'test_upgrade_template_schema_add_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_add_required_param'))

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_schema_add_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_add_required_param'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_add_required_param.cfg1'], {},
                         u'Upgrade: Add required param failed to keep existing param')

    def test_upgrade_template_schema_defaults(self):
        self.cfg1.register(config=u'test_upgrade_template_schema_defaults',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template_defaults.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_defaults_before.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_defaults'))

        self.assertIn(u'cfg1', self.cfg1[u'test_upgrade_template_schema_defaults'])
        self.assertNotIn(u'cfg2', self.cfg1[u'test_upgrade_template_schema_defaults'])

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_defaults.cfg1'],
                         {
                             u'item_1': u'Some Text',
                             u'item_3': {
                                 u'random': u'object'
                             }
                         },
                         u'Upgrade defaults: initial template wrong')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_schema_defaults',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template_defaults.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_defaults_after.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_defaults'))

        self.assertIn(u'cfg1', self.cfg1[u'test_upgrade_template_schema_defaults'])
        self.assertIn(u'cfg2', self.cfg1[u'test_upgrade_template_schema_defaults'])

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_defaults.cfg1'],
                         {
                             u'item_1': u'Some Text',
                             u'item_2': 123,
                             u'item_3': {
                                 u'random': u'object'
                             }
                         },
                         u'Upgrade defaults: cfg1 wrong')

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_defaults.cfg2'],
                         {
                             u'item_1': u'Some Default Text',
                             u'item_2': 123,
                             u'item_3': {
                                 u'default': u'object'
                             }
                         },
                         u'Upgrade defaults: cfg2 wrong')

    def test_upgrade_template_schema_add_required_param(self):
        self.cfg1.register(config=u'test_upgrade_template_schema_add_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_add_required_param'))

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_schema_add_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template_change_add.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_change_add.json'),
                           upgrade_merge_template=True)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_add_required_param'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_add_required_param.cfg1'], {},
                         u'Upgrade: Add required param failed to keep existing param')

        self.assertEqual(u'default', self.cfg1[u'test_upgrade_template_schema_add_required_param.cfg3'],
                         u'Upgrade: Add required param failed')

    def test_upgrade_template_schema_remove_required_param(self):
        self.cfg1.register(config=u'test_upgrade_template_schema_remove_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_remove_required_param'))

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_schema_remove_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources',
                                                 u'valid_template_change_remove.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_change_remove.json'),
                           upgrade_merge_template=True)

        self.assertEqual(u'new default', self.cfg1[u'test_upgrade_template_schema_remove_required_param.cfg3'],
                         u'Upgrade: remove required param failed')

    def test_upgrade_template_schema_modify_required_param(self):
        self.cfg1.register(config=u'test_upgrade_template_schema_modify_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_modify_required_param'))

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_schema_modify_required_param',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__),
                                                 u'resources',
                                                 u'valid_template_change_modify.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema_change_modify.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_modify_required_param'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_modify_required_param.cfg1_x'], {},
                         u'Upgrade: Modify required param failed.')

    def test_upgrade_template_schema_param_carried_forward(self):
        self.cfg1.register(config=u'test_upgrade_template_schema_param_carried_forward',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade_template_schema_param_carried_forward'))

        self.cfg1[u'test_upgrade_template_schema_param_carried_forward.cfg2'] = u'carry forward'

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_param_carried_forward.cfg2'], u'carry forward',
                         u'Upgrade: add carry forward param failed')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade_template_schema_param_carried_forward',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertEqual(self.cfg1[u'test_upgrade_template_schema_param_carried_forward.cfg2'], u'carry forward',
                         u'Upgrade: carry forward param failed')

    # Paths
    @unittest.skip(u'test_get_temp_path: Test needs writing!')
    def test_get_temp_path(self):
        # TODO: write this test
        self.assertTrue(False, u'Write test for get_temp_path')


if __name__ == u'__main__':
    unittest.main()

    # TODO: Add file checking to unit tests to ensure save is working!
