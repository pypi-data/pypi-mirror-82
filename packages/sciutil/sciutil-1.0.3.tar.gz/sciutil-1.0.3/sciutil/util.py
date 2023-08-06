###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from datetime import date
import os

from sciutil import Msg


class SciException(Exception):

    def __init__(self, message=''):
        Exception.__init__(self, message)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SciUtil:

    def __init__(self, fig_dir=None, data_dir=None, debug_on=True, plot_on=True, warn_color=bcolors.WARNING,
                 err_color=bcolors.FAIL, msg_color=bcolors.OKBLUE, sep="\t", user_date=None, save_fig=True,
                 add_date_postfix=True):
        self.debug_on = debug_on
        self.save_fig = save_fig
        self.plot_on = plot_on
        self.fig_dir = fig_dir
        self.data_dir = data_dir
        self.warn_color = warn_color
        self.err_color = err_color
        self.msg_color = msg_color
        self.sep = sep
        self.date = user_date
        self.add_date_postfix = add_date_postfix
        self.msg = Msg()
        # Make directory separator system dependent - here we set the windows to have a \ and / for linux and mac
        self.dir_sep = "\\" if os.name == 'nt' else '/'

    @staticmethod
    def print_msg(msg_lst: list, sep: str, color: str):
        msg = ""
        for i in msg_lst:
            msg += str(i) + sep

        print(color + "-" * 80 + bcolors.ENDC)
        print(color + msg.center(80, ' ') + bcolors.ENDC)
        print(color + '-' * 80 + bcolors.ENDC)

    def warn_p(self, msg_lst: list, sep=None, color=None):
        """
        Prints an error message. ToDo: Extend this to print to a log file as well.

        Parameters
        ----------
        self
        msg_lst
        sep
        color

        Returns
        -------

        """
        if color is None:
            color = self.warn_color
        if sep is None:
            sep = self.sep
        self.print_msg(msg_lst, sep, color)

    def err_p(self, msg_lst: list, sep=None, color=None):
        """
        Prints an error message. ToDo: Extend this to print to a log file as well.

        Parameters
        ----------
        self
        msg_lst
        sep
        color

        Returns
        -------

        """
        if color is None:
            color = self.err_color
        if sep is None:
            sep = self.sep

        self.print_msg(msg_lst, sep, color)

    def dp(self, msg_lst: list, sep=None, color=None):
        """
        Prints the message in a common debug format.
        Has a flag to stop printing too.
        Parameters
        ----------
        sep
        msg_lst
        color

        Returns
        -------

        """
        if self.debug_on:
            if sep is None:
                sep = self.sep
            if color is None:
                color = self.msg_color

            self.print_msg(msg_lst, sep, color)

    def get_date_str(self) -> str:
        """
        Helper funtion that returns the date - used typically when saving files.
        Returns
        -------

        """
        if self.add_date_postfix:
            if not self.date:
                self.date = date.today().strftime(("%Y%m%d"))
            return self.date
        else:
            return ''

    @staticmethod
    def save_df_json(data_df, outfile_path_str: str) -> None:
        """

        Parameters
        ----------
        data_df
        outfile_path_str

        Returns
        -------

        """

        data_df.to_json(outfile_path_str, orient='index')

    @staticmethod
    def save_df(data_df, outfile_path_str: str, keep_index_b=False, sep=',') -> None:
        """
        By default don't keep the index, it is just annoying.

        Parameters
        ----------
        data_df
        outfile_path_str
        keep_index_b
        sep

        Returns
        -------

        """

        data_df.to_csv(outfile_path_str, index=keep_index_b, sep=sep)

    @staticmethod
    def save_plt(fig, name: str, dpi=100) -> None:
        """
        Save a figure.
        Parameters
        ----------
        fig
        name
        dpi

        Returns
        -------

        """
        fig.savefig(name, format="png", bbox_inches='tight', pad_inches=0, dpi=dpi)

    def generate_label(self, label_lst: list, postfix='', sep='_') -> str:
        """

        Parameters
        ----------
        label_lst
        postfix
        sep

        Returns
        -------

        """
        date_time = self.get_date_str()
        label = ''
        for l in label_lst:
            if isinstance(l, str) and l[-1] != '/':
                label += str(l) + sep
            else:
                label += str(l)
        if label[-1] == sep:
            label += date_time
        else:
            label += sep + date_time
        return label + postfix

    def save_svg(self, plt, label_lst: list) -> None:
        """
        Saves a figure as SVG.

        Parameters
        ----------
        plt
        label_lst

        Returns
        -------

        """
        if self.save_fig:
            label = self.generate_label(label_lst)
            self.dp(["Saving plot", label])
            plt.savefig(label + ".svg")

    def check_dir_format(self, dir_str) -> str:
        """
        Check a directory string has a trailing slash.

        Parameters
        ----------
        dir_str

        Returns
        -------

        """
        return f'{dir_str}{self.dir_sep}' if not dir_str[-1] == self.dir_sep else dir_str

    def to_dir(self, dir_path: str, filename: str):
        """ Saves me having to import os. """
        return os.path.join(dir_path, filename)

    def dir_exists_err(self, dir_path: str, throw_err=True):
        """ Check if a dir exists otherwise throw an error """
        if os.path.exists(dir_path):
            msg = f'Path exists: {dir_path}'
            self.err_p([msg])
            if throw_err:
                raise SciException(msg)
            return True
        return False

    def dir_notexist_err(self, dir_path: str, throw_err=True):
        """ Check if a dir doesn't exists otherwise throw an error """
        if not os.path.exists(dir_path):
            msg = f'Path exists: {dir_path}'
            self.err_p([msg])
            if throw_err:
                raise SciException(msg)
            return True
        return False
