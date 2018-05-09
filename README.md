# Puppet Rundeck

Feed Rundeck with Puppet nodes.

This Python script reads into the Puppet Master filesystem and produces a yaml file containing up-to-date nodes information. The nodes definition can be customized to add or remove as many facts as wanted, which can then be queried by Rundeck Node Filter.

The final yaml file should be exposed to an internal address, used as a URL Source in Rundeck Project Nodes configuration.


## Requirement
* Python 3

## Usage

### Configuration

The file `conf/conf.yaml` should be filled with several sections:

* `tmp_file`: the temporary file where the script will write before replacing the output file with its new version
* `yamlstruct`: the yaml block describing each node. It should be formatted in this way:
```yaml
yamlstruct:
  node_name: name
  keys:
    key1: value1
    key2: value2
    key3: value3
```
    

This script should run on the Puppet Master and have read access to puppet directories.

```
./puppet_to_rundeck.py [OPTIONS]
```

### Options

Name | Description | Default
--- | --- | ---
`-o, --outfile` | **Required:** output yaml file |
`-i, --inputdir` | **Required:** input directory containg puppet nodes yaml files | `/var/lib/puppet/yaml/node`
`-m, --maxage` | **Required:** max age of input node files (days) | 7
