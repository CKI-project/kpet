# Copyright (c) 2019 Red Hat, Inc. All rights reserved. This copyrighted
# material is made available to anyone wishing to use, modify, copy, or
# redistribute it subject to the terms and conditions of the GNU General Public
# License v.2 or later.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""The "arch" command"""
import re

from kpet import misc, data, cmd_misc


def build(cmds_parser, common_parser):
    """Build the argument parser for the arch command"""
    _, action_subparser = cmd_misc.build(
        cmds_parser,
        common_parser,
        "arch",
        help='Architecture to test on',
    )
    list_parser = action_subparser.add_parser(
        "list",
        help='Output a list of known architecture names',
        parents=[common_parser],
    )
    list_parser.add_argument('-t', '--tree', metavar='REGEX',
                             default=None,
                             help='Limit output to architectures with trees '
                             'matching the REGEX.')
    list_parser.add_argument('regex', nargs='?', default=None,
                             help='Regular expression fully matching '
                                  'names of architectures to output.')


def main(args):
    """Main function for the `arch` command"""
    if not data.Base.is_dir_valid(args.db):
        misc.raise_invalid_database(args.db)
    database = data.Base(args.db)
    if args.action == 'list':
        regex = re.compile(args.regex or ".*")
        tree_regex = re.compile(args.tree or ".*")

        tree_arches = set()
        for name, value in database.trees.items():
            if tree_regex.fullmatch(name):
                tree_arches |= set(value['arches'])

        for arch in sorted(filter(regex.fullmatch, tree_arches)):
            print(arch)

    else:
        misc.raise_action_not_found(args.action, args.command)
