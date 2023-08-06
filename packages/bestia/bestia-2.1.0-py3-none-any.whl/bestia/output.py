from sys import getsizeof, stdout
from os.path import join as PATH_JOIN
from os import sep as PATH_SEPARATOR
from os import popen, get_terminal_size
from time import sleep
from random import randint

from bestia.iterate import string_to_list, iterable_to_string, unique_random_items
from bestia.misc import command_output
from bestia.error import *

CHAR_SIZE = getsizeof('A')
ENCODING = 'utf-8'
RETRO_LAG = 0.00001 #  0.0005

ANSI_SGR_CODES = {
    
    # Select Graphic Rendition
    'reset': 0,
    'bold': 1,       # bolds  ONLY fg, NOT ul
    'faint': 2,      # faints ONLY fg, NOT ul           (AKA dark)
    'underline': 4,  # <<< SHOULD NOT affect padding
    'blink': 5,      # blinks ONLY fg, ul

    'reverse': 7,    # reverses fg + ul, bg
    'conceal': 8,    # conceals ONLY fg, ul, NOT bg

    'cross': 9,      # HARDLY supported...

    'black': 30,     # NOT gray...
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,

    # fx above this index are rarely supported...
    'frame': 51,
    'circle': 52,
    'overline': 53,

}

ANSI_CLR_VALUES = tuple( [ n for n in range(30, 50) ] )

ECHO_MODES = (
    'modern',
    'retro',
    'raw',
)

def validate_ansi(ansi_name, ansi_type=None):

    if not ansi_name:
        return

    if ansi_name not in ANSI_SGR_CODES:
        raise InvalidAnsiSequence(ansi_name)

    if not ansi_type:
        return ansi_name

    elif ansi_type == 'color':
        if ANSI_SGR_CODES[ansi_name] not in ANSI_CLR_VALUES:
            raise InvalidColor(ansi_name)

    elif ansi_type == 'fx':
        if ANSI_SGR_CODES[ansi_name] in ANSI_CLR_VALUES:
            raise InvalidFx(ansi_name)

    return ansi_name


def ansi_esc_seq(fx, offset=0):
    try:
        return '\033[{}m'.format(
            ANSI_SGR_CODES[fx] + offset
        )
    except KeyError:
        raise InvalidAnsiSequence(fx)


def dquoted(s):
    return '"{}"'.format(s)


def clear_screen():
    stdout.write('\033[H')
    stdout.write('\033[J')
    stdout.flush()


def obfuscate_random_chars(input_string, amount=0, obfuscator='_'):
    ''' returns input string with amount of random chars obfuscated '''
    amount = len(input_string) - 4 if not amount or amount >= len(input_string) else amount

    string_indecae = [
        i for i in range(
            len(str(input_string))
        )
    ]

    string_as_list = string_to_list(input_string)
    for random_index in unique_random_items(string_indecae, amount):
        string_as_list[random_index] = obfuscator

    return iterable_to_string(string_as_list)

def tty_rows():
    ''' returns dynamic rows of current terminal '''
    return get_terminal_size().lines

def tty_cols():
    ''' returns dynamic cols of current terminal '''
    return get_terminal_size().columns

class Row(object):

    '''a string with width == terminal size (unless otherwise specified). Instantiate a Row object with as many str|FString items as you like and it will keep its width constant by cropping/aligning items without a fixed_size'''

    def __init__(self, *items, width=False):
        self.__output = ''
        self.__fixed_width = width
        self.__fstrings = []
        for item in items:
            self.append(item)

    def __len__(self):
        return self.__fixed_width if self.__fixed_width else tty_cols()

    def assign_spaces(self):
        spaces_left = self.width

        # remove fixed_fs sizes
        for fs in self.fixed_fstrings():
            spaces_left -= len(fs)

        # gather adaptive_fs
        adaptive_fs_count = len(
            [ fs for fs in self.adaptive_fstrings() ]
        )
        if not adaptive_fs_count:
            return

        # if spaces_left < 1:
            ### CROP if removed more spaces than available?
            # return

        ### ALIGN

        # calculate individual size for each adaptive_fs + any spaces left
        adaptive_fs_size, spaces_left = divmod(
            spaces_left, adaptive_fs_count
        )

        # resize adaptive_fs
        for i, _ in enumerate(self.__fstrings):
            if not self.__fstrings[i].fixed_size:
                self.__fstrings[i].size = adaptive_fs_size

        # deal spaces_left to adaptive_fs 1 by 1
        while spaces_left:

            for i, _ in enumerate(self.__fstrings):

                if self.__fstrings[i].fixed_size:
                    continue

                self.__fstrings[i].size += 1

                spaces_left -= 1
                if not spaces_left:
                    break

    @property
    def width(self):
        return len(self)

    @property
    def output(self):
        self.__output = ''
        self.assign_spaces()
        for fs in self.__fstrings:
            self.__output = self.__output + str(fs)
        return self.__output

    def fixed_fstrings(self):
        for fs in self.__fstrings:
            if fs.fixed_size:
                yield fs

    def adaptive_fstrings(self):
        for fs in self.__fstrings:
            if not fs.fixed_size:
                yield fs

    def append(self, s):
        self.__fstrings.append(
            FString(s) if type(s) != FString else s
        )

    def echo(self, mode='modern'):
        echo(self, mode=mode)

    def __str__(self):
        return self.output


class echo(object):

    def __init__(self, init_string='', *fx, mode='modern'):

        self.__output = str(init_string)

        self.__fx = [ validate_ansi(f, ansi_type=None) for f in fx if f ]

        if mode not in ECHO_MODES:
            raise InvalidMode(mode)
        self.__mode = mode

        self()


    def __call__(self):

        try:
            exception = None
            for f in self.__fx:
                for char in ansi_esc_seq(f):
                    _lag_chr(char)

            for char in self.__output:
                # only output chars get lagged...
                _lag_chr(
                    char,
                    lag =  RETRO_LAG if self.__mode == 'retro' else 0,
                    random_lag = 100 if self.__mode == 'retro' else 1,
                )

        except Exception as x:
            exception = x

        finally:
            if self.__fx:
                for char in ansi_esc_seq('reset'):
                    _lag_chr(char)

            if exception:
                raise exception

            if self.__mode != 'raw':
                _lag_chr('\n')


def _lag_chr(char=' ', lag=0, random_lag=1):
    random_multiplier = randint(1, random_lag)
    sleep(lag *random_multiplier)
    stdout.write(char)
    stdout.flush()


class FString(object):

    def __init__(self, init_string='', size=0, pad=' ', align='l', fg='', bg='', fx=[]):

        self.fixed_size = True if size else False

        self.__input_string = ''
        self.append(init_string)

        self.__output_size = self.__input_size
        self.size = size

        self.__pad = ' '
        self.pad = pad

        # l, r, c, cl, lc, cr, rc
        self.__align = 'l'
        self.align = align

        # black, red, green, yellow, blue, magenta, cyan, white
        self.__fg_color = ''
        self.fg_color = fg

        self.__bg_color = ''
        self.bg_color = bg

        # bold, dark, underline, blink, reverse, concealed
        self.__fx = []
        self.fx = fx


    def filter_utf_chars(self, string):
        '''
            filters out chars that can cause misalignments
            because made of more than a byte... makes sense?
        '''
        return bytearray(
            ord(c.encode(ENCODING)) for c in replace_special_chars(
                string
            ) if len(c.encode(ENCODING)) == 1
        ).decode(ENCODING)

    def append(self, string):
        self.__input_string = '{}{}'.format(
            self.__input_string,
            # self.filter_utf_chars(string),
            string,
        )
        self.set_input_size()

    def set_input_size(self):
        # calculate input_string length without color bytes
        ignore_these = [
            b'\xe2\x80\x8e', # left-to-right-mark
            b'\xe2\x80\x8b', # zero-width-space
        ]
        color_start_byte = b'\x1b'
        color_end_byte = b'm'
        self.__input_size = 0
        add = True
        for char in self.__input_string:
        # when encoding input_string into byte_string: byte_string will not necessarily have the same amount of bytes as characters in the input_string ( some characters will be made of several bytes ), therefore, the input_string should not be encoded but EACH INDIVIDUAL CHAR should
            byte = char.encode(ENCODING)
            if byte == color_start_byte and add:
                add = False
                continue
            elif byte == color_end_byte and not add:
                add = True
                continue
            if add and byte not in ignore_these:
                self.__input_size += 1

    def __str__(self):
        return self.output

    def __iter__(self):
        for c in self.output:
            yield c

    def __len__(self):
        return self.__output_size if self.__output_size > 0 else 0

    def __add__(self, other):
        return self.output + str(other)

    def echo(self, mode='modern'):
        echo(self, mode=mode)

    @property
    def size(self):
        return len(self)

    @size.setter
    def size(self, s=None):
        self.__output_size = int(s) if s else self.__input_size # desired len of output


    @property
    def pad(self):
        return self.__pad

    @pad.setter
    def pad(self, p):
        self.__pad = str(p)[0] if p else ' '

    @property
    def align(self):
        return self.__align

    @align.setter
    def align(self, a):
        if a not in ('l', 'r', 'c', 'lc', 'cl', 'rc', 'cr'):
            raise InvalidAlignment(a)
        self.__align = a

    @property
    def fg_color(self):
        return self.__fg_color

    @property
    def bg_color(self):
        return self.__bg_color

    @property
    def fx(self):
        return self.__fx

    @fg_color.setter
    def fg_color(self, c):
        if validate_ansi(c, ansi_type='color'):
            self.__fg_color = c

    @bg_color.setter
    def bg_color(self, c):
        if validate_ansi(c, ansi_type='color'):
            self.__bg_color = c

    @fx.setter
    def fx(self, fx):
        if type(fx) != list:
            raise TypeError('fx argument must be list')
        self.__fx = []
        for f in fx:
            if validate_ansi(f, ansi_type='fx'):
                self.__fx.append(f)


    @property
    def __big_pad(self):
        exact_half, excess = divmod(
            self.__output_size - self.__input_size, 2
        )
        return self.pad * (exact_half + excess)

    @property
    def __sml_pad(self):
        exact_half, excess = divmod(
            self.__output_size - self.__input_size, 2
        )
        return self.pad * exact_half


    def __paint_pad(self, p):
        ''' pads get bg_color as well BUT NOT if reverse option is specified '''

        if 'reverse' in self.__fx:
            # s = ansi_esc_seq('reverse') + s
            return p

        if self.__fg_color:
            p = ansi_esc_seq(self.__fg_color) + p

        if self.__bg_color:
            p = ansi_esc_seq(self.__bg_color, 10) + p

        return p + ansi_esc_seq('reset')


    @property
    def output(self):

        self.__output = self.__input_string.replace('\t', ' ') # can't afford to have tabs in output as they are never displayed the same

        if self.__input_size > self.__output_size:
            self.__crop_output()

        if self.__fg_color or self.__bg_color or self.__fx:
            self.__paint_output()

        if self.__output_size > self.__input_size:
            self.__align_output()

        return self.__output


    def __crop_output(self):
        delta_len = self.__input_size - self.__output_size
        self.__output = self.__output[:0 - delta_len]


    def __paint_output(self):

        for f in self.__fx:
            self.__output = ansi_esc_seq(f) + self.__output

        if self.__fg_color:
            self.__output = ansi_esc_seq(self.__fg_color) + self.__output

        if self.__bg_color:
            # background color range is +10 respect to foreground color
            self.__output = ansi_esc_seq(self.__bg_color, offset=10) + self.__output

        self.__output = self.__output + ansi_esc_seq('reset')


    def __align_output(self):

        if self.__align == 'l':
            self.__output = self.__output + self.__paint_pad(self.__sml_pad + self.__big_pad)

        elif self.__align == 'r':
            self.__output = self.__paint_pad(self.__sml_pad + self.__big_pad) + self.__output

        elif self.__align in ('c', 'cl', 'lc'):
            self.__output = self.__paint_pad(self.__sml_pad) + self.__output + self.__paint_pad(self.__big_pad)

        elif self.__align in ('cr', 'rc'):
            self.__output = self.__paint_pad(self.__big_pad) + self.__output + self.__paint_pad(self.__sml_pad)


def expand_seconds(input_seconds, output=dict):
    ''' expands input_seconds into a dict with as less keys as needed:
            seconds, minutes, hours, days, weeks

        can also return string
    '''
    time = {}
    time['minutes'], time['seconds'] = divmod(input_seconds, 60)
    time['hours'], time['minutes'] = divmod(time['minutes'], 60)
    time['days'], time['hours'] = divmod(time['hours'], 24)
    time['weeks'], time['days'] = divmod(time['days'], 7)

    if output == str:
        seconds = ' {} seconds'.format(round(time['seconds'], 2))
        minutes = ' {} minutes'.format(int(time['minutes'])) if time['minutes'] else ''
        hours = ' {} hours'.format(int(time['hours'])) if time['hours'] else ''
        days = ' {} days'.format(int(time['days'])) if time['days'] else ''
        weeks = ' {} weeks'.format(int(time['weeks'])) if time['weeks'] else ''
        return '{}{}{}{}{}'.format(weeks, days, hours, minutes, seconds).strip()

    return time


def remove_path(input_path, depth=-1):
    ''' removes directories from file path
        supports various levels of dir removal
    '''
    try:
        if depth > 0:
            depth = 0 - depth
        elif depth == 0:
            depth = -1
        levels = []
        while depth <= -1:
            levels.append(input_path.split(PATH_SEPARATOR)[depth])
            depth += 1
        return PATH_JOIN(*levels)
    except IndexError:
        return remove_path(input_path, depth=depth+1)


def replace_special_chars(t):
    ''' https://www.i18nqa.com/debug/utf8-debug.html
        some of the chars here im not sure are correct,
        check dumbo dublat romana translation
    '''
    special_chars = {
        # 'Äƒ': 'Ã',
        # 'Äƒ': 'ă',
        'Ã¢': 'â',
        'Ã¡': 'á', 'ã¡': 'á',
        'Ã ': 'à',
        'Ã¤': 'ä',
        'Å£': 'ã',
        # 'ÅŸ': 'ß',
        'ÃŸ': 'ß',
        'Ã©': 'é', 'ã©': 'é',
        'Ã¨': 'è',
        'Ã' : 'É', 'Ã‰': 'É',
        'Ã­': 'í',
        'Ã': 'Í',
        # 'Ã®': 'î',
        'Ã³': 'ó',
        'Ã“': 'Ó',
        'Ã¶': 'ö',
        'Ãº': 'ú',
        'Ã¹': 'ù',
        'Ã¼': 'ü',
        'Ã±': 'ñ',
        'Ã‘': 'Ñ',
        'Â´': '\'',
        '´': '\'',
        'â€ž': '“',
        'â€œ': '”',
        'â€¦': '…',
        b'\xe2\x80\x8e'.decode(ENCODING) : '', # left-to-right-mark
        b'\xe2\x80\x8b'.decode(ENCODING) : '',	# zero-width-space
        '&amp' : '&',
        '&;': '&',
        '【': '[',
        '】': ']',
        'â€“': '-',
        '⑥': '6',
    }

    for o, i in special_chars.items():
        t = str(t).replace(o, i)
    return t


class ProgressBar(object):

    def __init__(self, goal, width=0, pad='=', color=''):

        self.goal = float(goal)
        self.score = 0.0

        self.spaces = int(
            width if width else tty_cols() - 3
        )

        self.scores_by_space = [
            # 100.1, 100.1, 100.1
        ]
        self.calculate_space_scores()

        self.pad = str(pad)[0]
        self.color = color

    @property
    def done(self):
        return self.score >= self.goal


    def eval_score(self, value):

        self.score += float(value)

        overcome_scores = []
        for i, space_score in enumerate(self.scores_by_space):
            if self.score < space_score:
                break
            overcome_scores.append(i)
            echo(
                self.pad,
                self.color,
                mode='raw'
            )

        for d in range(len(overcome_scores)):
            del self.scores_by_space[0]


    def calculate_space_scores(self):
        ''' sets threshold needed to fill each space '''
        score_x_space = self.goal / self.spaces
        for s in range(self.spaces):
            self.scores_by_space.append(
                score_x_space * (s + 1)
            )
        # assert self.scores_by_space[-1] == self.goal


    def update(self, value=0.0):

        if self.done:
            return

        if self.score == 0:
            echo('[', 'faint', self.color, mode='raw')
            echo('.' * self.spaces, 'faint', self.color, mode='raw')
            echo(']', 'faint', self.color, mode='raw')
            stdout.write('\b' * (self.spaces +1 ))

        self.eval_score(value)

        if self.done:
            echo(']', 'faint', self.color)
