# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")


def _nnabla_version():
    import nnabla
    return 'Version {}'.format(nnabla.__version__) + \
           ', ' + \
           'Build {}'.format(nnabla.__build_number__)


def version_command(args):
    print(_nnabla_version())


return_value = None


def main():
    global return_value
    import six.moves._thread as thread
    import threading
    thread.stack_size(128 * 1024 * 1024)
    sys.setrecursionlimit(0x3fffffff)
    main_thread = threading.Thread(target=cli_main)
    main_thread.start()
    main_thread.join()
    if not return_value:
        sys.exit(-1)


def cli_main():
    global return_value
    return_value = False

    import nnabla
    parser = argparse.ArgumentParser(description='Command line interface ' +
                                     'for NNabla({})'.format(_nnabla_version()))
    parser.add_argument(
        '-m', '--mpi', help='exec with mpi.', action='store_true')

    subparsers = parser.add_subparsers()

    from nnabla.utils.cli.train import add_train_command
    add_train_command(subparsers)

    from nnabla.utils.cli.forward import add_infer_command, add_forward_command
    add_infer_command(subparsers)
    add_forward_command(subparsers)

    from nnabla.utils.cli.encode_decode_param import add_decode_param_command, add_encode_param_command
    add_encode_param_command(subparsers)
    add_decode_param_command(subparsers)

    from nnabla.utils.cli.profile import add_profile_command
    add_profile_command(subparsers)

    from nnabla.utils.cli.conv_dataset import add_conv_dataset_command
    add_conv_dataset_command(subparsers)

    from nnabla.utils.cli.compare_with_cpu import add_compare_with_cpu_command
    add_compare_with_cpu_command(subparsers)

    from nnabla.utils.cli.create_image_classification_dataset import add_create_image_classification_dataset_command
    add_create_image_classification_dataset_command(subparsers)

    from nnabla.utils.cli.uploader import add_upload_command
    add_upload_command(subparsers)

    from nnabla.utils.cli.uploader import add_create_tar_command
    add_create_tar_command(subparsers)

    from nnabla.utils.cli.convert import add_convert_command
    add_convert_command(subparsers)

    from nnabla.utils.cli.plot import (
        add_plot_series_command, add_plot_timer_command)
    add_plot_series_command(subparsers)
    add_plot_timer_command(subparsers)

    # Version
    subparser = subparsers.add_parser(
        'version', help='Print version and build number.')
    subparser.set_defaults(func=version_command)

    print('NNabla command line interface (Version {}, Build {})'.format(
        nnabla.__version__, nnabla.__build_number__))

    args = parser.parse_args()

    if 'func' not in args:
        parser.print_help(sys.stderr)
        return

    if args.mpi:
        from nnabla.utils.communicator_util import create_communicator
        comm = create_communicator()
        try:
            return_value = args.func(args)
        except:
            import traceback
            print(traceback.format_exc())
            comm.abort()
    else:
        try:
            return_value = args.func(args)
        except:
            import traceback
            print(traceback.format_exc())
            return_value = False


if __name__ == '__main__':
    main()
