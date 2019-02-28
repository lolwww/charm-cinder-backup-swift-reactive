Cinder Backup to external Swift
-------------------------------

Overview
========

Support for backing up volumes to external swift.
Cinder-backup service configuration is propagated to the cinder charm.

In order to use it external swift URL is needed along with authentication details.


To use:

    juju deploy cinder
    juju deploy cinder-backup-swift
    juju add-relation cinder-backup-swift cinder


