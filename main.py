import argparse
import logging
import os
import pwd
import stat
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    parser = argparse.ArgumentParser(
        description="List and change the permission mode of a file or directory."
    )
    parser.add_argument('path', type=str, help="Path to the file or directory to manage permissions.")
    parser.add_argument(
        '--set-permissions', type=str, nargs=2, metavar=('USER', 'PERMISSIONS'),
        help="Set permissions. PERMISSIONS is an octal mode such as 640 (applied as the full mode with os.chmod) or a set of owner bits such as rwx. USER is recorded in the log; the mode is applied to the path. Example: --set-permissions user 640 or --set-permissions user rwx"
    )
    parser.add_argument(
        '--remove-permissions', type=str, metavar='USER',
        help="Remove permissions. If USER is a set of bits such as rw, those bits are cleared from the mode. Otherwise all owner permission bits are removed for the named user."
    )
    parser.add_argument('--list-permissions', action='store_true', help="List current permissions for the file or directory.")
    parser.add_argument('--version', action='version', version='file-access-control 1.0', help="Show the version of the tool.")
    return parser

def _mode(path):
    return stat.S_IMODE(Path(path).stat().st_mode)

def list_permissions(path):
    logging.info(f"Listing permissions for: {path}")
    logging.info(f"Permissions: {oct(_mode(path))}")

def _parse_set_mode(current, permissions):
    p = permissions.strip().lower()
    if p and all(c in '01234567' for c in p) and len(p) in (3, 4):
        return int(p, 8)
    if p and all(c in 'rwx' for c in p):
        owner = 0
        if 'r' in p: owner |= stat.S_IRUSR
        if 'w' in p: owner |= stat.S_IWUSR
        if 'x' in p: owner |= stat.S_IXUSR
        return (current & ~0o700) | owner
    raise ValueError(f"Permissions must be an octal mode such as 640 or a set of bits such as rwx, got: {permissions}")

def set_permissions(path, user, permissions):
    before = _mode(path)
    after = _parse_set_mode(before, permissions)
    os.chmod(path, after)
    after = _mode(path)
    logging.info(f"Setting permissions '{permissions}' for user '{user}' on: {path}")
    logging.info(f"Mode before: {oct(before)}")
    logging.info(f"Mode after: {oct(after)}")
    return after != before or True

def remove_permissions(path, user):
    before = _mode(path)
    u = user.strip().lower()
    if u and all(c in 'rwx' for c in u):
        clear = 0
        for shift in (6, 3, 0):
            bits = 0
            if 'r' in u: bits |= 4
            if 'w' in u: bits |= 2
            if 'x' in u: bits |= 1
            clear |= bits << shift
        after_mode = before & ~clear
    else:
        # No ACL support: the user-specific class on a POSIX file is the owner bits.
        # Removing all permissions for the named user therefore clears the owner bits.
        after_mode = before & ~0o700
    os.chmod(path, after_mode)
    after = _mode(path)
    logging.info(f"Removing permissions for user '{user}' on: {path}")
    logging.info(f"Mode before: {oct(before)}")
    logging.info(f"Mode after: {oct(after)}")

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    if not os.path.exists(args.path):
        logging.error(f"The specified path does not exist: {args.path}")
        print(f"Error: path does not exist: {args.path}")
        return 1
    if args.list_permissions:
        list_permissions(args.path)
        return 0
    if args.set_permissions:
        try:
            set_permissions(args.path, args.set_permissions[0], args.set_permissions[1])
        except ValueError as e:
            logging.error(str(e)); print(f"Error: {e}"); return 1
        return 0
    if args.remove_permissions:
        remove_permissions(args.path, args.remove_permissions)
        return 0
    logging.error("No valid operation specified. Use --help for usage details.")
    print("Error: no operation specified; give one of --list-permissions, --set-permissions, or --remove-permissions.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
