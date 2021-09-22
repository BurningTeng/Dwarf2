from dwarf_debugger.lib.tool import Tool


class Injector(Tool):
    def parse_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--script",
            type=str,
            help="Path to an additional script to load with dwarf and frida js api"
        )

        parser.add_argument(
            "-bs", "--break-start", action='store_true', help="break at start")

        parser.add_argument(
            "-ds",
            "--debug-script",
            action='store_true',
            help="debug outputs from frida script")

    def get_script(self):
        if self.arguments.script is not None:
            import os
            if os.path.exists(self.arguments.script):
                return open(self.arguments.script, 'r').read()


def main():
    Injector()
