# Puppet Rundeck

Feed Rundeck with Puppet nodes.

This project produces a yaml file which you can expose on an internal address. Using a URL Source in Project Nodes configuration, Rundeck then fetches up-to-date Puppet Nodes.


## Requirement
* Python 2.7 (tested). Other versions should work.

## Usage

This script should run on the Puppet Master and have read access to puppet directories.

```
./puppet_to_rundeck.py [OPTIONS]
```

### Options

Name | Description | Default
--- | --- | ---
`-o, --outfile` | Required: output yaml file |
`-i, --inputdir` | Required: in put directory containg puppet nodes yaml files | `/var/lib/puppet/yaml/node`
`-m, --maxage` | Required: max age of input node files (days) | 7
