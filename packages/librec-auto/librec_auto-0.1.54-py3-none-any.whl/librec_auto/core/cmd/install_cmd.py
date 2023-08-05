from librec_auto.core.cmd import Cmd
from librec_auto.core.util import Files
from librec_auto.core import ConfigCmd
import os
import sys
import librec_auto
from pathlib import Path

import progressbar
import urllib.request
import time


class InstallCmd(Cmd):
    def __str__(self):
        return f'InstallCmd()'

    def setup(self, args):
        pass

    def dry_run(self, config):
        # self._config = config
        print(f'librec-auto (DR): Running install command {self}')
        # for script_path, params in config.collect_scripts('post'):
        #     param_spec = utils.create_param_spec(params)
        #     print (f'    Post script: {script_path}')
        #     print (f'\tParameters: {param_spec}')

    def execute(self, config: ConfigCmd):
        install_path = Path(librec_auto.__file__).parent
        jar_path = install_path / "jar" / "auto.jar"
        #jar_path = os.path.dirname(librec_auto.__file__) + '\\jar\\auto.jar'
        urllib.request.urlretrieve(
            'http://that-recsys-lab.net/downloads/auto.jar',
            str(jar_path.absolute()), self.show_progress)

    # def execute(self, config: ConfigCmd):
    #     jar_path = os.path.dirname(librec_auto.__file__) + '\\jar\\auto.jar'
    #     import urllib.request
    #     urllib.request.urlretrieve(
    #         'https://www.dropbox.com/s/hyemqt99790t16q/auto.jar?dl=1',
    #         jar_path, self.show_progress)

    def show_progress(self, count, block_size, total_size):
        # global start_time
        if count == 0:
            self.start_time = time.time()
            return
        duration = time.time() - self.start_time
        progress_size = int(count * block_size)
        speed = int(
            progress_size /
            (1024 *
             (int(duration) + 1)))  # int(progress_size / (1024 * duration))
        percent = min(int(count * block_size * 100 / total_size),
                      100)  # int(count * block_size * 100 / total_size)
        sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                         (percent, progress_size /
                          (1024 * 1024), speed, duration))
        sys.stdout.flush()

    # def show_progress(self, block_num, block_size, total_size):
    #     # global pbar
    #     if self.pbar is None:
    #         self.pbar = progressbar.ProgressBar(maxval=total_size)
    #
    #     downloaded = block_num * block_size
    #     if downloaded < total_size:
    #         self.pbar.update(downloaded)
    #     else:
    #         self.pbar.finish()
    #         self.pbar = None


# class MyProgressBar():
#     def __init__(self):
#         self.pbar = None
#
#     def __call__(self, block_num, block_size, total_size):
#         if not self.pbar:
#             self.pbar=progressbar.ProgressBar(maxval=total_size)
#             self.pbar.start()
#
#         downloaded = block_num * block_size
#         if downloaded < total_size:
#             self.pbar.update(downloaded)
#         else:
#             self.pbar.finish()
