import charms.reactive as reactive
import charms_openstack.charm
import charm.openstack.cinder_backup_swift


charms_openstack.charm.defaults.use_defaults(
    'charm.installed',
    'update-status')


@reactive.when_any('backup-backend.joined', 'backup-backend.changed')
@reactive.when_not('backup-backend.available')
def configure_cinder_backup():
    with charm.provide_charm_instance() as charm_class:
        charm_class.set_relation_data()
        charm_class.configure_ca()
        charm_class.restart_service()
    reactive.set_state('backup-backend.available')


@reactive.hook('config-changed')
def update_config():
    reactive.remove_state('backup-backend.available')
    with charm.provide_charm_instance() as charm_class:
        charm_class.set_relation_data()
    reactive.set_state('backup-backend.available')
