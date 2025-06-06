#!/usr/bin/env python3
"""
test for the Jsonval module.
"""

import unittest
import sys

from base_test import PschedTestBase

from pscheduler.jsonval import json_validate
from pscheduler.jsonval import json_validate_from_standard_template
from pscheduler.jsonval import json_standard_template_max_schema


class TestJsonval(PschedTestBase):
    """
    Jsonval tests.
    """

    def test_jsonval(self):
        """Test jsonval"""
        sample = {
            "schema": 10,
            "when": "2015-06-12T13:48:19.234",
            "howlong": "PT10M",
            "sendto": "bob@example.com",
            "x-factor": 3.14,
            "protocol": "udp",
            "ipv": 6,
            "ip": "fc80:dead:beef::",
            "archspec": { "data": { "bar": "baz" } },
        }

        schema = {
            "local": {
                "protocol": {
                    "type": "string",
                    "enum": ['icmp', 'udp', 'tcp']
                }
            },
            "type": "object",
            "properties": {
                "schema": {"$ref": "#/pScheduler/Cardinal"},
                "when": {"$ref": "#/pScheduler/Timestamp"},
                "howlong": {"$ref": "#/pScheduler/Duration"},
                "sendto": {"$ref": "#/pScheduler/Email"},
                "ipv": {"$ref": "#/pScheduler/ip-version"},
                "ip": {"$ref": "#/pScheduler/IPAddress"},
                "protocol": {"$ref": "#/local/protocol"},
                "x-factor": {"type": "number"},
                "archspec": {"$ref": "#/pScheduler/ArchiveSpecification"},
            },
            "required": ["sendto", "x-factor"]
        }

        # missing an attr
        valid, message = json_validate(sample, schema)

        self.assertFalse(valid)

        self.assertTrue(message in [
            # Different versions of JSONSchema return different errors
            '''At /archspec: 'archiver' is a required property''',
            '''At /archspec: {'data': {'bar': 'baz'}} is not valid under any of the given schemas'''
            ])

        # add it in now
        sample['archspec']['archiver'] = 'tar'

        valid, message = json_validate(sample, schema)

        self.assertEqual((valid, message), (True, 'OK'))


        # Bad schemas

        valid, message = json_validate(sample, schema, max_schema=5)
        self.assertEqual((valid, message), (False, "Schema version 10 is not supported (highest is 5)."))

        sample['schema'] = "This is bad."
        valid, message = json_validate(sample, schema, max_schema=5)
        self.assertEqual((valid, message), (False, "Schema value must be an integer."))


    def test_hostname(self):
        schema = {
            'type': 'object',
            'properties': {
                'value': {'$ref': '#/pScheduler/HostName'}
            }
        }

        for (test, expected) in [
                # First element length
                ('', False),
                ('a', True),
                ('a' * 62, True),
                ('a' * 63, True),
                ('a' * 64, False),
                ('_' + 'a' * 61, True),
                ('_' + 'a' * 62, True),
                ('_' + 'a' * 63, False),

                # First element content
                ('foo123', True),
                ('foo123.', True),
                ('foo-123', True),
                ('_foo123', True),
                ('foo_123', False),
                ('@foo123', False),
                ('foo@123', False),
                ('.bar.org', False),
                ('.bar.org.', False),

                # Second and subsequent element length
                ('foo.123456789-123456789-123456789-123456789-123456789-123456789-123.bar.org', True),
                ('foo.123456789-123456789-123456789-123456789-123456789-123456789-1234.bar.org', False),

                # Second and subsequent element content
                ('foo.bar.org', True),
                ('foo.bar-baz.org', True),
                ('_foo.bar.org', True),
                ('_foo.bar.org.', True),
                ('foo._bar.org.', False),
        ]:
            valid, message = json_validate({ 'value': test }, schema)
            self.assertEqual(valid, expected, f'''{test} - Should be {'valid' if expected else 'invalid'}''')


    def test_json_validate_from_standard_template(self):

        template = {
            "local": {
            },
            "versions": {
                "1": {
                    "type": "object",
                    "properties": {
                        "schema": {"$ref": "#/pScheduler/Cardinal"},
                        "foo":    {"$ref": "#/pScheduler/String"},
                    }
                },
                "2": {
                    "type": "object",
                    "properties": {
                        "schema": {"$ref": "#/pScheduler/Cardinal"},
                        "foo":    {"$ref": "#/pScheduler/String"},
                        "bar":    {"$ref": "#/pScheduler/String"},
                    }
                }
            }
        }


        (result, error) = json_validate_from_standard_template({ "schema": 1, "foo": "Hello, world!" }, template)
        self.assertEqual(result, True)

        (result, error) = json_validate_from_standard_template({ "schema": 1, "bar": "Hello, world!" }, template)
        self.assertEqual(result, False)

        (result, error) = json_validate_from_standard_template({ "schema": 9, "foo": "Hello, world!" }, template)
        self.assertEqual(result, False)



    def test_json_standard_template_max_schema(self):

        self.assertRaises(
            ValueError,
            json_standard_template_max_schema, {}
        )

        self.assertRaises(
            ValueError,
            json_standard_template_max_schema, { "versions": {} }
        )

        self.assertEqual(
            json_standard_template_max_schema({ "versions": { "1": {} } }),
            1
        )

        self.assertEqual(
            json_standard_template_max_schema({ "versions": { "1": {}, "2": {} } }),
            2
        )

        self.assertRaises(
            ValueError,
            json_standard_template_max_schema, { "versions": { "1": {}, "3": {} } }
        )





if __name__ == '__main__':
    unittest.main()
