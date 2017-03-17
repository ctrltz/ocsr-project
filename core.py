from os import path
import argparse
from libs import config, process, utils


def main():
    # Setting up argument parser
    parser = argparse.ArgumentParser(description='This script allows to use OSRA for processing big datasets and '
                                                 'evaluate quality of the result.')
    io = parser.add_argument_group("I/O Options")
    io.add_argument('db_path',
                    help="Directory where the database is located")
    # io.add_argument('-f', choices=['png', 'jpg'],
    #                 help="File format to process (default: png)")
    io.add_argument('-w',
                    help="Output directory (default: 'out' near the database folder)")
    advanced = parser.add_argument_group("Advanced Options")
    # advanced.add_argument('-d', action='store_true',
    #                       help="Debug mode (detailed output)")
    advanced.add_argument('-j', '--jar',
                           help="Path to the jar file to be used")
    advanced.add_argument('-p', '--path',
                          help="OSRA executable (default = 'osra')")
    advanced.add_argument('-t', '--threaded', action='store_true',
                          help="Use multithreading")
    # advanced.add_argument('-r', action='store_true',
    #                    help="Restore initial version of 'spelling.txt' file after experiments")
    # advanced.add_argument('-s', action='store_true',
    #                       help='Turn on auto-corrections')
    args = parser.parse_args()

    # Initializing all parameters
    config.dbDir = path.abspath(args.db_path)
    config.name = path.basename(config.dbDir)
    if args.jar is not None:
        config.jar_path = path.abspath(args.jar)
    # config.spelling = path.join(getcwd(), 'spelling.txt')
    config.resDir = path.normpath(path.join(config.dbDir, config.RESULTS_RELATIVE_PATH))
    if args.w is None:
        config.resDir = path.normpath(path.join(config.resDir, config.name))
    else:
        config.resDir = args.w
    config.report_file = path.normpath(path.join(config.resDir, config.REPORT_FILE))
    config.tmpDir = path.normpath(path.join(config.resDir, 'tmp'))
    config.inDir = path.normpath(path.join(config.resDir, 'in'))
    config.outDir = path.normpath(path.join(config.resDir, 'out'))

    open(config.report_file, "w").close()

    # config.debug = args.d
    config.version = 'osra'  # + args.v
    # config.restore = args.r
    # config.auto = args.s

    config.fPattern = '*.png'
    # if args.f is None:
    #     config.fPattern = config.pattern[config.action]
    # else:
    #     config.fPattern = '*.' + args.f

    # Logging the settings & starting the process
    utils.show_settings()
    process.launch()


if __name__ == '__main__':
    main()
