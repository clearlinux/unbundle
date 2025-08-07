## DISCONTINUATION OF PROJECT. 

This project will no longer be maintained by Intel. 

Intel will not provide or guarantee development of or support for this project, including but not limited to, maintenance, bug fixes, new releases or updates. Patches to this project are no longer accepted by Intel. If you have an ongoing need to use this project, are interested in independently developing it, or would like to maintain patches for the community, please create your own fork of the project.

Contact: webadmin@linux.intel.com  
# unbundle

unbundle parses bundle and pundle definition files to recursively resolve
a complete list of all packages in a bundle.

```
usage: unbundle [-h] [--bundles] bundle_name bundle_path

Process bundle packages following includes

positional arguments:
  bundle_name  name of bundle to process
  bundle_path  path to clr-bundles directory

optional arguments:
  -h, --help   show this help message and exit
  --bundles    Report only included bundle names
```

unbundle prints a sorted list of all included packages.
