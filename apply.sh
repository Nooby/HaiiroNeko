#!/bin/sh

dir=$(dirname $0)

puppet apply $dir/puppet/manifests/base.pp --modulepath=$dir/puppet/modules
