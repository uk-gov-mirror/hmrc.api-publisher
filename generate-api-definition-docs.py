#!/usr/bin/env python

import json
import argparse
#
# Generates documentation from a JSON schema
# Usage example
# `python generate-api-definition-docs.py app/resources/api-definition-schema.json > docs/api-definition.md`
# Will generate markdown and output to STDOUT
parser = argparse.ArgumentParser(description='Generate documentation from a JSON schema')
parser.add_argument('schema_file', metavar='FILE', help='JSON file containing the JSON schema')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

args = parser.parse_args()


def output(text):
    print(text)


def output_row(name, definition, is_required):
    """
    Output a table row markdown detailing information about JSON key
    :param name: Name of the JSON key
    :param definition: dict, the JSON schema definition for the key
    :param is_required: Is the key Optional or Required
    :return: None
    """
    data_type = definition.get('type')
    enum = definition.get('enum')
    default = definition.get('default', '')
    values = ''

    if data_type == 'array':
        data_type = definition.get('items').get('type') + '[]'
        if definition.get('items').get('type') == 'string':
            enum = definition.get('items').get('enum')

    if data_type == 'object' or data_type == 'object[]':
        values = '[{}](#{})'.format(name.lower(), name)

    if isinstance(enum, list):
        values = '<br>'.join(enum)

    output(
        '| `{}` | `{}` | {} | {} | {} | {}'.format(
            name,
            data_type,
            is_required,
            values,
            default,
            definition.get('description', '')
        )
    )


def output_object(name, schema_object, **kwargs):
    """
    Output the markdown for a JSON schema object
    :param name: Name of the object/key
    :param schema_object: JSON schema definition
    :return: None
    """
    required = schema_object.get('required', [])
    children = []

    output('{} {}'.format('#' * kwargs.get('level', 2), name))
    output(schema_object.get('description', ''))
    output('')
    output(
        '| {} | {} | {} | {} | {} | {}'.format('key', 'type', 'required', 'values', 'default', 'description')
    )
    output('| --- | --- | --- | --- | --- | --- |')
    for name, definition in schema_object['properties'].items():
        is_required = 'Required' if name in required else 'Optional'
        if definition.get('type') == 'object':
            children.append({'name': name, 'definition': definition})
        if definition.get('type') == 'array' and definition.get('items').get('type') == 'object':
            children.append({'name': name, 'definition': definition.get('items')})
        output_row(name, definition, is_required)

    for child in children:
        output_object(child['name'], child['definition'], level=3)


with open(args.schema_file) as file:
    schema = json.load(file)

output('Generated from [JSON schema]({})'.format(args.schema_file))
output_object('Root', schema)
