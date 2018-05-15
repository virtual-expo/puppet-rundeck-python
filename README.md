# Puppet Rundeck

Feed Rundeck with Puppet nodes.

This Python script reads into the Puppet Master filesystem and produces a yaml file containing up-to-date nodes information. The nodes description is based on Puppet facts and reads from the yaml node reports written by puppet. The output file respects [Rundeck resource yaml format](http://rundeck.org/docs/man5/resource-yaml.html). Facts (custom or not) can be added at will, and are then available in Rundeck Node Filter.

The final yaml file should be exposed to an internal address, used as a URL Source in Rundeck Project Nodes configuration.


## Requirement
* Python 3

## Usage
This script should run on the Puppet Master and have read access to puppet directories.

```bash
cp conf/conf_example.yaml conf/conf.yaml
./puppet_to_rundeck.py [OPTIONS]
```

### Options

Name | Description | Default
--- | --- | ---
`-o, --outfile` | **Required:** output yaml file |
`-i, --inputdir` | **Required:** input directory containg puppet nodes yaml files | `/var/lib/puppet/yaml/node`
`-m, --maxage` | **Required:** max age of input node files (days) | 7


### Configuration

The file `conf/conf.yaml` should be copied from `conf/conf_example.yaml` and adapted. Sections:

* `tmp_file`: the temporary file where the script will write before replacing the output file with its new version
* `yamlstruct`: the yaml block describing each node. It should be formatted in this way:
```yaml
yamlstruct:
  node_name: yournodename
  keys:
    key1: value1
    key2: value2
    key3: value3
```
where `yournodename` is the title of your yaml block. The `node_name` entry is mandatory.
`keyN` is an optionnal entry, like a fact you want to access via Rundeck Node Filter.
* `tags_list`: is a list of tags, which are used in Rundeck for node filtering. The tag list is a subset of {key1, key2,...,keyN}.

If you need to add a few nodes **not** managed by Puppet, you can describe them in the file `conf/other_nodes.yaml`, following the example file `conf/other_nodes_example.yaml`.


### Example

Assuming your configuration file `conf/conf.yaml` is the following:
```yaml
---
tmp_file: /tmp/tmpfile.yaml
tags_list:
  - lsbdistcodename
  - customfact

yamlstruct:
  node_name: parameters.hostname
  keys:
    hostname: name
    osFamily: parameters.osfamily
    osVersion: parameters.os.release.full
    osName: parameters.os.lsb.distdescription
    osArch: parameters.architecture
    lsbdistcodename: parameters.lsbdistcodename
    customfact: parameters.mycustomfact
```

and the script reads from puppet node directory (`/var/lib/puppet/yaml/node` by default) the file `mynode.yaml` which contains:
```yaml
name: mynode
parameters:
  hostname: example_node
  osfamily: Debian
  os:
    release:
      full: '9.4'
    lsb:
      distdescription: Debian GNU/Linux 9.4 (stretch)
  architecture: amd64
  lsbdistcodename: stretch
  mycustomfact: mycustomvalue
[...]
```

the output block describing this node will read:
```yaml
example_node:
  hostname: mynode
  osFamily: Debian
  osVersion: '9.4'
  osName: Debian GNU/Linux 9.4 (stretch)
  osArch: amd64
  lsbdistcodename: stretch
  customfact: mycustomvalue
  tags: stretch, mycustomvalue
```

Each of the fields of the output block can be queried by Rundeck Node Filter.
