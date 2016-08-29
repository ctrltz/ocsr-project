import config


def show_settings():
    if config.debug:
        log('Job name: {}', config.name)
        log('Location of the database: {}', config.dbDir)
        log('Searching for files: {}', config.fPattern)
    log('Output directory: {}', config.outDir)
    if config.debug:
        blank()
        log('OSRA version: {}', config.osra_path)
        log('Action to perform: {}', config.action_full[config.action])
        log('Debug information: {}', config.tumbler[config.debug])
        # log('Restore initial state: {}', tumbler[restore])
        # log('Auto-corrections: {}', tumbler[auto])
        # log('Using files without hydrogen: {}', tumbler[noh])
        # log('Images to be manually corrected: {}', manual)
    blank()
    if not config.auto:
        log('Some help with spelling correction may be needed')


def log(out, *args):
    print out.format(*args)


def blank():
    print ''
