import argparse
import os
import sys

def resolve_includes(bundle_name, bundle_path, content, bundles=False, path=set(), seen=set()):
    """
    resolve_incudes returns a full package list of include-resolved packages in
    the bundle definition file or pundle declaration under bundle_path. Sources
    for included bundles are other bundle definition files at
    bundle_path/bundles/* and bundle_path/packages.
    """
    if bundle_name in seen:
        return True
    seen.add(bundle_name)
    path.add(bundle_name)
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
        elif line.startswith("also-add("):
            continue
        elif line.startswith("include("):
            inc_bundle = line[line.find("(")+1:line.find(")")]
            if inc_bundle in path:
                return True
            success = resolve_includes(inc_bundle, bundle_path, content, bundles, path)
            if not success:
                return False
            if bundles:
                content.add(inc_bundle)
            continue
        elif not bundles:
            content.add(line)

    path.remove(bundle_name)
    return True

def main():
    parser = argparse.ArgumentParser(description='Process bundle packages following includes')
    parser.add_argument('bundle_name', help='name of bundle to process')
    parser.add_argument('bundle_path', help='path to clr-bundles directory')
    parser.add_argument('--bundles', default=False, action='store_true',
                        help='Report only included bundle names')
    args = parser.parse_args()
    success = True
    content = set()
    if args.bundles:
        os_core_set = set(["os-core"])
    else:
        os_core_set = set()
        success = resolve_includes("os-core", args.bundle_path, os_core_set)
    if not success:
        sys.exit(1)

    success = resolve_includes(args.bundle_name, args.bundle_path, content, bundles=args.bundles)
    if not success:
        sys.exit(1)

    print('\n'.join(sorted(os_core_set.union(content))))

if __name__ == "__main__":
    main()
