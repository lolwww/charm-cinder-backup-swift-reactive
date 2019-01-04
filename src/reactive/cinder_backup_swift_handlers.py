import charms_openstack.charm as charm
import charms.reactive as reactive


@reactive.when_any('install')
def install_cinder_backup():
    with charm.provide_charm_instance() as charm_class:
        charm_class.install()


@reactive.when('storage-backend.available')
@reactive.when_not('cinder.configured')
def backup_backend(principle):
    with charm.provide_charm_instance() as charm_class:
        config = charm_class.get_swift_backup_config()
        principle.configure_principal(config)
        charm_class.configure_ca()
        charm_class.restart_service()
    reactive.set_state('cinder.configured')


@reactive.hook('config-changed')
def update_config():
    reactive.remove_state('cinder.configured')
