"""
Blueprint
"""
import argparse
import json
import os
import sys

from jinja2 import Environment
from jinja2 import FileSystemLoader


def parse_context():
    # Make sure context file exists.
    if not os.path.isfile('context.json'):
        return {}

    context = {}
    try:
        f = open('context.json')
    except IOError:
        sys.exit()
    else:
        try:
            context = json.load(f)
        except ValueError as e:
            print("\033[91mError decoding context.json:\033[0m {}".format(e))
            sys.exit()
        else:
            for key, value in context.items():
                if len(value) == 0:
                    # Ask to fill in for the missing values.
                    context[key] = input('{} = '.format(key))
            return context
    return context


def generate_output(context, templates_dir, output_dir):
    env = Environment(loader=FileSystemLoader(templates_dir))

    for root, dirs, files in os.walk(templates_dir):
        for name in files:
            # Create corresponding root folder.
            base_dir = '/'.join(root.split('/')[1:])
            new_root = os.path.relpath(os.path.join(output_dir, base_dir))
            try:
                os.makedirs(new_root)
            except OSError:
                pass

            # Generate corresponding file.
            file_path = os.path.join(base_dir, name)
            template = env.get_template(file_path)
            output = template.render(context)
            new_file_path = os.path.join(new_root, name)
            with open(new_file_path, 'w') as f:
                f.write(output)

            print("\033[92m>>> {}\033[0m".format(file_path))


def cmdline():
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Render templates using Jinja2.")
    parser.add_argument(
        '-i',
        '--templates-dir',
        dest='templates_dir',
        default='templates',
    )
    parser.add_argument(
        '-o',
        '--outout-dir',
        dest='output_dir',
        default='output',
    )
    args = parser.parse_args()

    context = parse_context()
    generate_output(context, args.templates_dir, args.output_dir)
