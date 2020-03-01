import logging
from datetime import datetime

from me import MailExtractor, is_online
# noinspection PyArgumentList
from me.utils import update_provider

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] \t %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ],
)
logging = logging.getLogger(__name__)

_app_version = 0.1
_app_name = "sMaile"


def banner():
    return """
--------------------
%s v%s
by blu3f1r3 
--------------------

Try -h for instructions and help
""" % (_app_name, _app_version)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--update", help="Update autoconfig files", action='store_true', required=False)
    parser.add_argument("-t", "--email", help="Target email", required=False)
    parser.add_argument("-p", "--password", help="login password", required=False)
    parser.add_argument("--max-output", type=int, help="limit printed outout", required=False)
    parser.add_argument("--json-output", help="output as json to given path", type=str, required=False)
    args = parser.parse_args()

    if args.update:
        update_provider()
        exit()

    if not args.email:
        print("Target email is required (-t/--email)")
    if not args.password:
        print("Target password is required (-p/--password)")
    if not args.email or not args.password:
        print('For help try -h')
        exit()

    print(banner())
    start_time = datetime.now()

    logging.debug('Testing internet connection')
    assert is_online(), "no internet connection"

    me = MailExtractor(
        target_email=args.email,
        target_password=args.password,
        as_json=True if args.json_output else False,
        output_file_path=getattr(args, 'json_output', None),
        output_print_max=getattr(args, 'max_output', None)
    )
