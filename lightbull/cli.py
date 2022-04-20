import argparse
import json
import os
import sys

from rich.console import Console
from rich.table import Table

from .lightbull import Lightbull, LightbullError


class LightbullCLI:
    def run(self):
        # init rich console
        self._console = Console()
        self._error_console = Console(stderr=True)

        # parse arguments and connect to lightbull API
        self._parse_arguments()
        try:
            self._api = Lightbull(self._args.url, self._args.password)
        except (LightbullError, OSError) as e:
            self._fail("Cannot connect to lightbull API: {}".format(e))

        # call correct handler
        if self._args.command == "config":
            self._run_config()
        elif self._args.command == "shutdown":
            self._run_shutdown()
        elif self._args.command == "shows":
            self._run_shows()
        elif self._args.command == "visuals":
            self._run_visuals()
        elif self._args.command == "groups":
            self._run_groups()
        elif self._args.command == "parameters":
            self._run_parameters()
        else:
            self._print_help()

    def _parse_arguments(self):
        parser = argparse.ArgumentParser(description="Lightbull CLI")
        subparser = parser.add_subparsers(title="commands", dest="command")

        # global parameters
        parser.add_argument("-u", "--url", type=str, required=True, help="URL of the server")
        parser.add_argument("-p", "--password", type=str, required=True, help="Password for API")

        # the simple subcommands...
        subparser.add_parser("config")
        subparser.add_parser("shutdown")

        # shows
        cmd_shows = subparser.add_parser("shows")
        cmd_shows_subparser = cmd_shows.add_subparsers(title="actions", dest="action")
        # shows list
        cmd_shows_subparser.add_parser("list")
        # shows get
        cmd_shows_get = cmd_shows_subparser.add_parser("get")
        cmd_shows_get.add_argument("--id", type=str, required=True, help="ID of show")
        # shows new
        cmd_shows_new = cmd_shows_subparser.add_parser("new")
        cmd_shows_new.add_argument("--name", type=str, required=True, help="Name of show")
        cmd_shows_new.add_argument("--favorite", help="Set as favorite", action="store_true", dest="favorite")
        cmd_shows_new.add_argument(
            "--no-favorite", help="Do not set as favorite", action="store_false", dest="favorite"
        )
        # shows update
        cmd_shows_update = cmd_shows_subparser.add_parser("update")
        cmd_shows_update.add_argument("--id", type=str, required=True, help="ID of show")
        cmd_shows_update.add_argument("--name", type=str, help="Name of show")
        cmd_shows_update.add_argument("--favorite", help="Set as favorite", action="store_true", dest="favorite")
        cmd_shows_update.add_argument(
            "--no-favorite", help="Do not set as favorite", action="store_false", dest="favorite"
        )
        # shows delete
        cmd_shows_delete = cmd_shows_subparser.add_parser("delete")
        cmd_shows_delete.add_argument("--id", type=str, required=True, help="ID of show")

        # visuals
        cmd_visuals = subparser.add_parser("visuals")
        cmd_visuals_subparser = cmd_visuals.add_subparsers(title="actions", dest="action")
        # visuals get
        cmd_visuals_get = cmd_visuals_subparser.add_parser("get")
        cmd_visuals_get.add_argument("--id", type=str, required=True, help="ID of visual")
        # visuals new
        cmd_visuals_new = cmd_visuals_subparser.add_parser("new")
        cmd_visuals_new.add_argument("--name", type=str, required=True, help="Name of visual")
        cmd_visuals_new.add_argument(
            "--show-id", type=str, required=True, help="ID of show where the visual belongs to"
        )
        # visuals update
        cmd_visuals_update = cmd_visuals_subparser.add_parser("update")
        cmd_visuals_update.add_argument("--id", type=str, required=True, help="ID of visual")
        cmd_visuals_update.add_argument("--name", type=str, required=True, help="Name of visual")
        # shows delete
        cmd_visuals_delete = cmd_visuals_subparser.add_parser("delete")
        cmd_visuals_delete.add_argument("--id", type=str, required=True, help="ID of visual")

        # groups
        cmd_groups = subparser.add_parser("groups")
        cmd_groups_subparser = cmd_groups.add_subparsers(title="actions", dest="action")
        # groups get
        cmd_groups_get = cmd_groups_subparser.add_parser("get")
        cmd_groups_get.add_argument("--id", type=str, required=True, help="ID of group")
        # groups new
        cmd_groups_new = cmd_groups_subparser.add_parser("new")
        cmd_groups_new.add_argument(
            "--visual-id", type=str, required=True, help="ID of visual where the group belongs to"
        )
        cmd_groups_new.add_argument("--parts", type=str, required=True, help="List of parts (comma separated)")
        cmd_groups_new.add_argument("--effect-type", type=str, required=True, help="Effect type")
        # groups update
        cmd_groups_update = cmd_groups_subparser.add_parser("update")
        cmd_groups_update.add_argument("--id", type=str, required=True, help="ID of group")
        cmd_groups_update.add_argument("--parts", type=str, help="List of parts (comma separated)")
        cmd_groups_update.add_argument("--effect-type", type=str, help="Effect type")
        # groups delete
        cmd_groups_delete = cmd_groups_subparser.add_parser("delete")
        cmd_groups_delete.add_argument("--id", type=str, required=True, help="ID of group")

        # parameters
        cmd_parameters = subparser.add_parser("parameters")
        cmd_parameters_subparser = cmd_parameters.add_subparsers(title="actions", dest="action")
        # parameters get
        cmd_parameters_get = cmd_parameters_subparser.add_parser("get")
        cmd_parameters_get.add_argument("--id", type=str, required=True, help="ID of parameter")
        # parameters update
        cmd_parameters_update = cmd_parameters_subparser.add_parser("update")
        cmd_parameters_update.add_argument("--id", type=str, required=True, help="ID of parameter")
        cmd_parameters_update.add_argument("--current", type=str, help="Current value as JSON")
        cmd_parameters_update.add_argument("--default", type=str, help="Default value as JSON")

        self._args = parser.parse_args()
        self._print_help = parser.print_help

    def _run_config(self):
        config = self._api.config()

        table = Table(title="Parts", width=80)
        table.add_column("Name")
        for name in config["parts"]:
            table.add_row(name)
        self._console.print(table)

        self._console.print()

        table = Table(title="Effects", width=80)
        table.add_column("Name")
        table.add_column("Title")
        for name, title in config["effects"].items():
            table.add_row(name, title)
        self._console.print(table)

        self._console.print()

        table = Table(title="Features", width=80)
        table.add_column("Name")
        for name in config["features"]:
            table.add_row(name)
        self._console.print(table)

    def _run_shutdown(self):
        self._api.system.shutdown()

    def _run_shows(self):
        if self._args.action == "list":
            shows = self._api.shows.get_shows()
            table = Table(title="Shows", width=80)
            table.add_column("Name")
            table.add_column("ID")
            table.add_column("Favorite")
            for show in shows:
                table.add_row(show["name"], show["id"], ":star:" if show["favorite"] else "")
            self._console.print(table)
        elif self._args.action == "get":
            try:
                show = self._api.shows.get_show(self._args.id)

                self._console.print("[bold]Name: {}".format(show["name"]))
                self._console.print("[bold]Favorite: {}".format("Yes" if show["name"] else "No"))
                self._console.print()

                table = Table(title="Visuals", width=80)
                table.add_column("Name")
                table.add_column("ID")
                for visual in show["visuals"]:
                    table.add_row(visual["name"], visual["id"])
                self._console.print(table)

            except LightbullError as e:
                self._fail("Cannot get show: {}".format(e))
        elif self._args.action == "new":
            try:
                self._api.shows.new_show(self._args.name, self._args.favorite)
            except LightbullError as e:
                self._fail("Cannot create new show: {}".format(e))
        elif self._args.action == "update":
            try:
                self._api.shows.update_show(self._args.id, self._args.name, self._args.favorite)
            except LightbullError as e:
                self._fail("Cannot update show: {}".format(e))
        elif self._args.action == "delete":
            try:
                self._api.shows.delete_show(self._args.id)
            except LightbullError as e:
                self._fail("Cannot delete show: {}".format(e))
        else:
            self._print_help()

    def _run_visuals(self):
        if self._args.action == "get":
            try:
                visual = self._api.shows.get_visual(self._args.id)

                self._console.print("[bold]Name: {}".format(visual["name"]))
                self._console.print()

                table = Table(title="Groups")
                table.add_column("ID")
                table.add_column("Parts")
                table.add_column("Effect")
                table.add_column("Parameters")
                for groups in visual["groups"]:
                    param_list = []
                    for param in groups["effect"]["parameters"]:
                        param_list.append("{} ({})".format(param["name"], param["id"]))
                    table.add_row(
                        groups["id"],
                        os.linesep.join(groups["parts"]),
                        groups["effect"]["type"],
                        os.linesep.join(param_list),
                    )
                self._console.print(table)
            except LightbullError as e:
                self._fail("Cannot get visual: {}".format(e))
        elif self._args.action == "new":
            try:
                self._api.shows.new_visual(self._args.show_id, self._args.name)
            except LightbullError as e:
                self._fail("Cannot create new visual: {}".format(e))
        elif self._args.action == "update":
            try:
                self._api.shows.update_visual(self._args.id, self._args.name)
            except LightbullError as e:
                self._fail("Cannot update visual: {}".format(e))
        elif self._args.action == "delete":
            try:
                self._api.shows.delete_visual(self._args.id)
            except LightbullError as e:
                self._fail("Cannot delete visual: {}".format(e))
        else:
            self._print_help()

    def _run_groups(self):
        if self._args.action == "get":
            try:
                group = self._api.shows.get_group(self._args.id)

                self._console.print("[bold]Effect: {}".format(group["effect"]["type"]))

                self._console.print()

                table = Table(title="Parts")
                table.add_column("Name")
                for name in group["parts"]:
                    table.add_row(name)
                self._console.print(table)

                self._console.print()

                table = Table(title="Parameters")
                table.add_column("ID")
                table.add_column("Name")
                table.add_column("Key")
                table.add_column("Type")
                table.add_column("Default value")
                table.add_column("Current value")
                for parameter in group["effect"]["parameters"]:
                    table.add_row(
                        parameter["id"],
                        parameter["name"],
                        parameter["key"],
                        parameter["type"],
                        str(parameter["default"]),
                        str(parameter["current"]),
                    )
                self._console.print(table)
            except LightbullError as e:
                self._fail("Cannot get group: {}".format(e))
        elif self._args.action == "new":
            try:
                parts = self._args.parts.split(",")
                self._api.shows.new_group(self._args.visual_id, parts, self._args.effect_type)
            except LightbullError as e:
                self._fail("Cannot create new group: {}".format(e))
        elif self._args.action == "update":
            try:
                parts = self._args.parts.split(",") if self._args.parts else None
                self._api.shows.update_group(self._args.id, parts, self._args.effect_type)
            except LightbullError as e:
                self._fail("Cannot update group: {}".format(e))
        elif self._args.action == "delete":
            try:
                self._api.shows.delete_group(self._args.id)
            except LightbullError as e:
                self._fail("Cannot delete group: {}".format(e))
        else:
            self._print_help()

    def _run_parameters(self):
        if self._args.action == "get":
            try:
                parameter = self._api.shows.get_parameter(self._args.id)
                table = Table(title="Parameters")
                table.add_column("Name")
                table.add_column("Key")
                table.add_column("Type")
                table.add_column("Default value")
                table.add_column("Current value")
                table.add_row(
                    parameter["name"],
                    parameter["key"],
                    parameter["type"],
                    json.dumps(parameter["default"]),
                    json.dumps(parameter["current"]),
                )
                self._console.print(table)
            except LightbullError as e:
                self._fail("Cannot get parameter: {}".format(e))
        elif self._args.action == "update":
            try:
                try:
                    current = json.loads(self._args.current) if self._args.current else None
                    default = json.loads(self._args.default) if self._args.default else None
                except ValueError:
                    self._fail("Cannot parse JSON value for parameter")
                self._api.shows.update_parameter(self._args.id, current, default)
            except LightbullError as e:
                self._fail("Cannot update parameter: {}".format(e))
        else:
            self._print_help()

    def _fail(self, msg):
        self._error_console.print("[bold red]{}".format(msg))
        sys.exit(1)


def main():
    cli = LightbullCLI()
    cli.run()
