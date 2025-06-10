import argparse
import os
import sys


def resolve_includes(bundle_name, bundle_path,
                     content, bundles=False, seen=None, search=''):
    """
    resolve_incudes returns a full package list of include-resolved packages in
    the bundle definition file or pundle declaration under bundle_path. Sources
    for included bundles are other bundle definition files at
    bundle_path/bundles/* and bundle_path/packages.
    """
    if not seen:
        seen = set()
    if bundle_name in seen:
        return True
    seen.add(bundle_name)
    bundle_def = os.path.join(bundle_path, "bundles", bundle_name)
    try:
        with open(bundle_def, "r", encoding="latin-1") as bundlef:
            lines = bundlef.readlines()
    except FileNotFoundError:
        print(f"ERROR: could not find {bundle_name} bundle")
        return False

    if bundles:
        content.add(bundle_name)

    for line in lines:
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("also-add("):
            continue
        if line.startswith("include("):
            inc_bundle = line[line.find("(")+1:line.find(")")]
            success = resolve_includes(inc_bundle, bundle_path,
                                       content, bundles, seen, search)
            if not success:
                return False
            if search == inc_bundle:
                print(f"{bundle_name} includes {search}")
            if bundles:
                content.add(inc_bundle)
            continue
        if not bundles:
            content.add(line)

    return True


def main():
    parser = argparse.ArgumentParser(description='Process bundle packages following includes')
    parser.add_argument('bundle_name', help='name of bundle to process')
    parser.add_argument('bundle_path', help='path to clr-bundles directory')
    parser.add_argument('--bundles', default=False, action='store_true',
                        help='Report only included bundle names')
    parser.add_argument('--search', default='',
                        help='Display bundles processed that include this bundle')
    args = parser.parse_args()
    success = True
    content = set()
    if args.bundles:
        os_core_set = set(["os-core"])
    else:
        os_core_set = set()
        success = resolve_includes("os-core", args.bundle_path, os_core_set, search=args.search)
    if not success:
        sys.exit(1)

    success = resolve_includes(args.bundle_name, args.bundle_path, content,
                               bundles=args.bundles, search=args.search)
    if not success:
        sys.exit(1)

    if not args.search:
        print('\n'.join(sorted(os_core_set.union(content))))


if __name__ == "__main__":
    main()
