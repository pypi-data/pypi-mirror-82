## BOMIST Utilities

## Getting started

Requirements: Python 3.

```
$ pip3 install bomist_utils
$ bomist_utils --help
```

On Windows you might have to re-launch your terminal in order for the `bomist_utils` command to be recognized.

## Dumping legacy workspaces (v1 to v2)

```
$ bomist_utils --dump1 --ws <wspath>
```

`wspath` is the path of the workspace you want to dump. A `.ws` file must exist in it.

A `legacy.bomist_dump` file will be created on the directory the command is ran from. This file can then be imported by BOMIST v2.

### Limitations

This utility can only export/dump and keep data connections between:

```
parts, documents, labels, storage, categories
```

---

For more info: [bomist.com](https://bomist.com)
