include nginx
include software
include python
include uwsgi
include redis
include upstart
include rq
include mongodb

exec { 'apt-get update':
    command => '/usr/bin/apt-get update',
}

group { 'www-data':
    ensure => present,
}
user { 'www-data':
    ensure => present,
    groups => ['www-data'],
    membership => minimum,
    shell => "/bin/bash",
    require => Group['www-data']
}

class upstart {
    package { 'upstart':
        ensure => installed,
        require => Exec['apt-get update'],
    }
}

class redis {
    package { 'redis-server':
        ensure  => present,
        require => Exec['apt-get update'],
    }
}

class nginx {
    package { 'nginx':
        ensure => present,
        before => File['/etc/nginx/sites-available/default'],
        require => Exec['apt-get update'],
    }
    file { '/etc/nginx/sites-available/default':
        ensure => file,
        owner => 'root',
        group => 'root',
        mode => '640',
        content => template('/www/puppet/templates/default_site.erb'),
    }
    file { '/var/log/nginx/error.log':
        ensure => file,
        owner => 'www-data',
        group => 'www-data',
        mode => '640',
    }
    service { 'nginx':
        ensure     => running,
        enable     => true,
        hasstatus  => true,
        hasrestart => true,
        subscribe  => File['/etc/nginx/sites-available/default'],
        require    => Class['uwsgi']
    }
}

class software {
  package { ['git', 'vim', ]:
      require => Exec['apt-get update'],
      ensure => installed,
  }
}

class python {
    include python::packages

    package { 'python':
        ensure => installed,
        require => Exec['apt-get update'],
    }
}

class python::packages {
    $apt = ['python-dev', 'build-essential', 'python-pip']
    $pip = ['flask', 'requests']

    package { $apt:
        require => Class['python'],
        ensure => installed,
    }
    package { $pip:
        require => Class['python'],
        ensure => installed,
        provider => pip,
    }
}

class mongodb {
    package { 'mongodb':
        ensure  => present,
        require => Exec['apt-get update'],
    }
    package { 'pymongo':
        require  => Class['python'],
        ensure   => installed,
        provider => pip,
    }
    service { 'mongodb':
        ensure     => running,
        enable     => true,
        hasstatus  => true,
        hasrestart => true,
        require => Package['mongodb'],
    }
}

class rq {
    $pip = ['redis', 'rq', 'rq-scheduler']
    package { $pip:
        require => [Class['python::packages'], Class['upstart']],
        ensure => installed,
        provider => pip,
    }
    file { '/etc/init/rq_scheduler.conf':
        ensure => present,
        owner => 'root',
        group => 'root',
        mode => '0644',
        source => '/www/puppet/files/etc/init/rq_scheduler.conf',
        require => Package['rq-scheduler'],
    }
    file { '/etc/init/rqworker.conf':
        ensure => present,
        owner => 'root',
        group => 'root',
        mode => '0644',
        source => '/www/puppet/files/etc/init/rqworker.conf',
        require => Package['rq'],
    }
    service { 'rq_scheduler':
        ensure => running,
        provider => upstart,
        enable => true,
        hasrestart => false,
        hasstatus => false,
        require => [Package['rq-scheduler'], File[ '/etc/init/rq_scheduler.conf']],
    }
    service { 'rqworker':
        ensure => running,
        provider => upstart,
        enable => true,
        hasrestart => false,
        hasstatus => false,
        require => [Package['rq'], File[ '/etc/init/rqworker.conf']],
    }
}

class uwsgi {
    package { 'uwsgi':
        ensure => installed,
        provider => pip,
        require => [Class['python::packages'], Class['rq'], Class['upstart']],
    }
    file { '/etc/init/uwsgi.conf':
        ensure => present,
        owner => 'root',
        group => 'root',
        mode => '0644',
        source => '/www/puppet/files/etc/init/uwsgi.conf',
        require => Package['uwsgi'],
    }
    file { '/var/log/uwsgi.log':
        ensure => present,
        owner => 'www-data',
        group => 'www-data',
        mode => '0755',
        require => User['www-data'],
    }
    service { 'uwsgi':
        ensure => running,
        provider => upstart,
        enable => true,
        hasrestart => false,
        hasstatus => false,
        require => [File['/etc/init/uwsgi.conf'], File['/var/log/uwsgi.log']],
    }
}
