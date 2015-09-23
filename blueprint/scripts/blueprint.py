"""
Blueprint
"""
import argparse
import json
import os
import shutil
import sys

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined
from jinja2 import TemplateError
from termcolor import cprint


def parse_context(context_path):
    # Check if context file exists.
    if not os.path.isfile(context_path):
        return {}

    context = {}
    try:
        f = open(context_path)
    except IOError:
        sys.exit()
    else:
        try:
            context = json.load(f)
        except ValueError as e:
            cprint("Error decoding context file: {}".format(e), 'red')
            sys.exit()
        else:
            for key, value in context.items():
                if len(value) == 0:
                    # Ask to fill in for the missing values.
                    context[key] = input('{} = '.format(key))
            return context
    return context


def generate_output(context, templates_dir, output_dir):
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        undefined=StrictUndefined
    )

    for root, dirs, files in os.walk(templates_dir):
        for name in files:
            # Create corresponding root folder.
            common_prefix = os.path.commonprefix([root, templates_dir])
            relative_root = root[len(common_prefix):]

            # Strip potential traling separator.
            if relative_root.startswith(os.sep):
                relative_root = relative_root[len(os.sep):]
            new_root = os.path.join(output_dir, relative_root)

            try:
                os.makedirs(new_root)
            except OSError:
                pass

            # Generate corresponding file.
            file_path = os.path.join(root, name)
            relative_file_path = os.path.join(relative_root, name)
            new_file_path = os.path.join(new_root, name)

            if name.endswith('.bp'):
                template = env.get_template(relative_file_path)
                try:
                    output = template.render(context)
                except TemplateError as e:
                    cprint("> {}: {}".format(
                        relative_file_path, e.message), 'red')
                else:
                    # Strip bp extension from file name.
                    new_file_path = new_file_path[:-3]
                    with open(new_file_path, 'w') as f:
                        f.write(output)
                    cprint("> {}".format(relative_file_path), 'green')
            else:
                shutil.copy(file_path, new_file_path)
                cprint("> {}".format(relative_file_path), 'white')


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
    parser.add_argument(
        '-c',
        '--context',
        dest='context_path',
        default='context.json',
    )
    args = parser.parse_args()

    context = parse_context(args.context_path)
    generate_output(context, args.templates_dir, args.output_dir)
