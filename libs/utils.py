import config


def show_settings():
    log('Job name: {}', config.name)
    log('Location of the database: {}', config.dbDir)
    log('Output directory: {}', config.resDir)
    if config.debug:
        blank()
        log('OSRA version: {}', config.osra_path)
        # log('Debug information: {}', config.tumbler[config.debug])
        # log('Restore initial state: {}', tumbler[restore])
        # log('Auto-corrections: {}', tumbler[auto])
        # log('Using files without hydrogen: {}', tumbler[noh])
        # log('Images to be manually corrected: {}', manual)

    if not config.auto:
        log('Some help with spelling correction may be needed')


def log(out, *args):
    print out.format(*args)


def blank():
    print ''
