import sys
from typing import *

from openapi_parser.exporter import PackageWriter
from openapi_parser.model import HavingId
from openapi_parser.parser.loader import *

JUSTIFICATION_SIZE = 140
def main(args: Optional[List[str]] = None):
    if (args is None):
        args = sys.argv[1:]
    
    if (len(args) < 1):
        print(f"Not enough arguments, usage: python -m openapi_parser SCHEMA [DESTINATION] [PACKAGE_NAME]", file=sys.stderr)
        return 1
    
    schema_file = args.pop(0)
    parser = OpenApiParser.open(schema_file)
    parser.load_all()
    
    for path, mdl in parser.loaded_objects.items():
        print(('# ' + type(mdl).__name__ + (f" '{mdl.id}'" if isinstance(mdl, HavingId) else '')).ljust(JUSTIFICATION_SIZE, ' ') + f" -- '{path}'")
    print('# ' + '=' * JUSTIFICATION_SIZE)
    print('')
    
    package_writer = PackageWriter(parser, *args)
    package_writer.write_package(clean=True)
    
    return 0

if (__name__ == '__main__'):
    exit_code = main()
    exit(exit_code)
