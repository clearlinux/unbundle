# unbundle

unbundle parses bundle and pundle definition files to recursively resolve
a complete list of all packages in a bundle.

```
usage: unbundle [-h] bundle_name bundle_path

Process bundle packages following includes

positional arguments:
  bundle_name  name of bundle to process
  bundle_path  path to clr-bundles directory

optional arguments:
  -h, --help   show this help message and exit
```

unbundle prints a sorted list of all included packages.
