import charms_openstack.charm as charm
import charms.reactive as reactive

from charms.reactive.relations import (
    endpoint_from_flag,
)

charm.use_defaults(
    'charm.installed',
    'update-status')

# if config has been changed we need to re-evaluate flags
# config.changed is set and cleared (atexit) in layer-basic
flags.register_trigger(when='config.changed',
                       clear_flag='config.complete')
flags.register_trigger(when='upgraded', clear_flag='config.complete')
flags.register_trigger(
    when='endpoint.cinder-backup.changed',
    clear_flag='config.complete'
)


"""@reactive.when_any('install')
def install_cinder_backup():
    with charm.provide_charm_instance() as charm_instance:
        charm_instance.install()
        """


@reactive.when('endpoint.cinder-backup.joined')
@reactive.when_not('config.complete')
def configure_cinder_backup():
    # don't always have a relation context - obtain from the flag
    endp = endpoint_from_flag('endpoint.cinder-backup.joined')
    with charm.provide_charm_instance() as charm_instance:
        # publish config options for all remote units of a given rel
        name, config = charm_instance.get_swift_backup_config()
        endp.publish(name, config)
        charm_instance.configure_ca()
        charm_instance.restart_service()
        flags.set_flag('config.complete')
