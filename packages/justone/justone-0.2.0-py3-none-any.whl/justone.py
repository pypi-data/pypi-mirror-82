"""Fast duplicate files finder.

Inspired by https://stackoverflow.com/a/36113168/300783

Cli Typical Usage: py justone.py FOLDER [FOLDER ...] -t


Sample:

```
import hashlib

# find duplicate files
dups_list = JustOne(hashlib.sha1).update('D:/data').update(Path('C:/Wegame')).duplicates()
# OR dups_list = JustOne()('D:/data')(Path('C:/Wegame')).dup()

# print them
for dups in dups_list:
    for d in dups:
        print(d)
    print('')
```


Classes:

    JustOne

Functions:

    update(arg, *args) -> JustOne
    duplicates(strict_level) -> Iterator[Sequence[Path]]

Short Functions Alias:

    dup = duplicates
    __call__ = update

Misc variables:

    __version__

"""

import argparse
import filecmp
import itertools
import stat
import sys
import time
import traceback
from collections import defaultdict
from enum import IntEnum
from io import BufferedReader
from os import DirEntry, PathLike, scandir
from pathlib import Path
from typing import AnyStr, Callable, DefaultDict, Dict, Final, Generator, Iterable, Iterator, List, Literal, Optional, Sequence, Set, TextIO, Tuple, Type, Union

try:
    import xxhash
    _hash_func_default: Callable = xxhash.xxh3_128 # xxhash.xxh3_128 is six times as fast as hashlib.sha1 .
except ModuleNotFoundError:
    import hashlib
    _hash_func_default: Callable = hashlib.sha1

try:
    from tqdm import tqdm as tqdm_real

    def tqdm(arg, desc=None):
        return tqdm_real(tuple(arg), desc=desc, ascii=False, leave=True)
except ModuleNotFoundError:

    def tqdm(arg, *_args, **_kwargs):
        return arg


__author__: Final[str] = 'owtotwo'
__copyright__: Final[str] = 'Copyright 2020 owtotwo'
__credits__: Final[Sequence[str]] = ['owtotwo']
__license__: Final[str] = 'LGPLv3'
__version__: Final[str] = '0.2.0'
__maintainer__: Final[str] = 'owtotwo'
__email__: Final[str] = 'owtotwo@163.com'
__status__: Final[str] = 'Experimental'

FileIndex: Type = int # the index of file_info
FileSize: Type = int # the number of bytes
HashValue: Type = bytes # the type of hash calculation result
SinglePath: Type = Union[str, Path] # file or directory
IterablePaths: Type = Iterable[SinglePath] # some files or directories


class StrictLevel(IntEnum):
    """ File comparison strict level """
    COMMON = 0
    SHALLOW = 1
    BYTE_BY_BYTE = 2


_DEBUG_MODE: Final[bool] = False

HASH_FUNCTION_DEFAULT: Final[Callable] = _hash_func_default
SMALL_HASH_CHUNK_SIZE_DEFAULT: Final[int] = 1024
FULL_HASH_CHUNK_SIZE_DEFAULT: Final[int] = 524288 # 512kb
STRICT_LEVEL_DEFAULT: Final[StrictLevel] = StrictLevel.COMMON


class UnreachableError(RuntimeError):
    """ like unreachable in rust, which means the code will not reach expectedly """


class JustOneError(Exception):
    """ Base Exception for this module """


class GetFileInfoError(JustOneError):
    """ Exception for JustOne._get_file_info """


class UpdateFileInfoError(JustOneError):
    """ Exception for JustOne._update_file_info """


class UpdateError(JustOneError):
    """ Exception for JustOne._update_* """


class GetSmallHashError(JustOneError):
    """ Exception for JustOne._get_small_hash """


class GetFullHashError(JustOneError):
    """ Exception for JustOne._get_full_hash """


class GetDuplicatesError(JustOneError):
    """ Exception for JustOne.duplicates """


# return string like '[aaa] -> [bbb] -> [ccc]'
def format_exception_chain(e: BaseException) -> str:
    # recursive function, get exception chain from __cause__
    def get_exception_chain(e: BaseException) -> List[BaseException]:
        return [e] if e.__cause__ is None else [e] + get_exception_chain(e.__cause__)

    # use Exception class name as string if no message in Exception object
    e2s = lambda e: str(e) or e.__class__.__name__
    return ''.join(f'[{e2s(exc)}]' if i == 0 else f' -> [{e2s(exc)}]' for i, exc in enumerate(reversed(get_exception_chain(e))))


class JustOne:
    """
    Note: JustOne object is picklable.
    """
    def __init__(self, hash_func: Callable = HASH_FUNCTION_DEFAULT, ignore_error: bool = False) -> None:
        """This sets a hash function for identifying the same file.

        Args:
            hash_func: A hashlib-compliant hash function. (e.g.: hashlib.sha1)
            ignore_error: Ignore the OSError such as PermissionError when dealing with files.

        Returns:
            None
        """
        # Member variables sample:
        #   file_info: [
        #     <Index, Path-Object, File-Size, Small-Hash, Full-Hash>
        #     [0, Path('D:/abc/efg.txt'), 16801, '900150983cd24fb0', 'd6963f7d28e17f72'],
        #     [1, Path(...), 14323, ..., ...],
        #     [2, ...],
        #     ...
        #   ]
        #   file_index: {
        #       <Path-Object: Index>
        #       Path('D:/abc/efg.txt'): 0,
        #       Path(...): 1,
        #       ...
        #   }
        self.hash_func: Callable = hash_func
        self.ignore_error: bool = ignore_error
        self.file_info: List[Tuple[FileIndex, Path, FileSize, Optional[HashValue], Optional[HashValue]]] = []
        self.file_index: Dict[Path, FileIndex] = {}
        self.size_dict: DefaultDict[FileSize, Set[FileIndex]] = defaultdict(set)
        self.small_hash_dict: DefaultDict[Tuple[FileSize, HashValue], Set[FileIndex]] = defaultdict(set)
        self.full_hash_dict: DefaultDict[HashValue, Set[FileIndex]] = defaultdict(set)

    @staticmethod
    def _scan_dir(folder: Union[AnyStr, PathLike], ignore_error: bool = False) -> Iterator[DirEntry]:
        """Traverse all files in the folder recursively.

        Args:
            folder: Folder path. (e.g.: 'D:/abc/' or Path('D:/abc/'))
            ignore_error:
                Ignore the OSError such as PermissionError when dealing with files.
                If OSError is raised, silently swallow it.

        Returns:
            DirEntry objects of all files in the folder with any depth.
        """
        def _scan_dir_raw(folder: Union[AnyStr, PathLike]) -> Iterator[DirEntry]:
            with scandir(folder) as it:
                for entry in it:
                    if entry.is_dir():
                        for e in JustOne._scan_dir(entry.path, ignore_error=ignore_error):
                            yield e
                    else:
                        yield entry

        if ignore_error:
            try:
                for e in _scan_dir_raw(folder):
                    yield e
            except OSError:
                return
        else:
            for e in _scan_dir_raw(folder):
                yield e

    @staticmethod
    def _get_hash(fp: Path,
                  first_chunk_only: bool = False,
                  first_chunk_size: int = SMALL_HASH_CHUNK_SIZE_DEFAULT,
                  hash_func: Callable = HASH_FUNCTION_DEFAULT) -> HashValue:
        """
        Calculate hash for file or just for first chunk of file(the fisrt 1024bytes).
        """
        def chunk_reader(freader: BufferedReader, chunk_size: int = 1024) -> Iterator[bytes]:
            """ Generator that reads a file in chunks of bytes """
            while True:
                chunk = freader.read(chunk_size)
                if not chunk:
                    return
                yield chunk

        hash_obj = hash_func()
        with fp.open(mode='rb') as f:
            if first_chunk_only:
                hash_obj.update(f.read(first_chunk_size))
            else:
                for chunk in chunk_reader(f, chunk_size=FULL_HASH_CHUNK_SIZE_DEFAULT):
                    hash_obj.update(chunk)
        return hash_obj.digest()

    def _get_file_info(self, index: FileIndex) -> Tuple[Path, FileSize, Optional[HashValue], Optional[HashValue]]:
        """
        Get file info from self.file_info .
        """
        try:
            _, file, file_size, small_hash, full_hash = self.file_info[index]
        except IndexError as e:
            raise GetFileInfoError from e
        return file, file_size, small_hash, full_hash

    def _add_file_info(self,
                       file: Path,
                       file_size: Optional[FileSize] = None,
                       small_hash: Optional[HashValue] = None,
                       full_hash: Optional[HashValue] = None) -> FileIndex:
        """
        Add file info to self.file_info .
        If file is existed, do nothing.
        """
        index = self.file_index.get(file, None)
        if index is None:
            file_size = file.stat().st_size if file_size is None else file_size
            index = len(self.file_info)
            self.file_index[file] = index
            self.file_info.append((index, file, file_size, small_hash, full_hash))
        return index

    def _update_file_info(self,
                          index: FileIndex,
                          file_size: Optional[FileSize] = None,
                          small_hash: Optional[HashValue] = None,
                          full_hash: Optional[HashValue] = None) -> FileIndex:
        """
        Update file info to self.file_info, only support file-size, small-hash and full-hash.
        """
        try:
            index, file, file_size_old, small_hash_old, full_hash_old = self.file_info[index]
            file_size = file_size_old if file_size is None else file_size
            small_hash = small_hash or small_hash_old
            full_hash = full_hash or full_hash_old
            self.file_info[index] = (index, file, file_size, small_hash, full_hash)
        except IndexError as e:
            raise UpdateFileInfoError from e
        return index

    def _get_small_hash(self, index: FileIndex) -> HashValue:
        """
        If small hash is existed, use it. Otherwise, calculate the small hash, update it and return.
        """
        try:
            index, file, file_size, small_hash, full_hash = self.file_info[index]
        except IndexError as e:
            raise GetSmallHashError from e
        if small_hash is None:
            small_hash = self._get_hash(file, first_chunk_only=True, hash_func=self.hash_func)
            self.file_info[index] = (index, file, file_size, small_hash, full_hash)
        return small_hash

    def _get_full_hash(self, index: FileIndex) -> HashValue:
        """
        If full hash is existed, use it. Otherwise, calculate the full hash, update it and return.
        """
        try:
            index, file, file_size, small_hash, full_hash = self.file_info[index]
        except IndexError as e:
            raise GetFullHashError from e
        if full_hash is None:
            full_hash = self._get_hash(file, first_chunk_only=False, hash_func=self.hash_func)
            self.file_info[index] = (index, file, file_size, small_hash, full_hash)
        return full_hash

    def _merge_size_dict(self, size_dict_temp: Dict[FileSize, Set[FileIndex]]) -> Iterator[Tuple[FileSize, FileIndex]]:
        """
        Merge the new size-dict to self.size_dict .
        Return
          the file(with file-size) whose duplicates are existed,
          AND
          the file(with file-size) which had no duplicates originally but has now.
        """
        for k, v in size_dict_temp.items():
            index_set = self.size_dict[k]
            is_single = len(index_set) == 1
            index_set |= v
            if len(index_set) > 1:
                for index in (index_set if is_single else v):
                    yield k, index

    def _merge_small_hash_dict(self, small_hash_dict_temp: Dict[Tuple[FileSize, HashValue], Set[FileIndex]]) -> Iterator[FileIndex]:
        """
        Merge the new small-hash-dict to self.small_hash_dict .
        Return
          the file(with file-size) whose duplicates are existed,
          AND
          the file(with file-size) which had no duplicates originally but has now.
        """
        for k, v in small_hash_dict_temp.items():
            index_set = self.small_hash_dict[k]
            is_single = len(index_set) == 1
            index_set |= v
            if len(index_set) > 1:
                for index in (index_set if is_single else v):
                    yield index

    def _merge_full_hash_dict(self, full_hash_dict_temp: DefaultDict[HashValue, Set[FileIndex]]) -> Iterator[FileIndex]:
        """
        Merge the new full-hash-dict to self.full_hash_dict .
        Return
          the file(with file-size) whose duplicates are existed,
          AND
          the file(with file-size) which had no duplicates originally but has now.
        """
        for k, v in full_hash_dict_temp.items():
            index_set = self.full_hash_dict[k]
            is_single = len(index_set) == 1
            index_set |= v
            if len(index_set) > 1:
                for index in (index_set if is_single else v):
                    yield index

    def _update_multiple_files_with_size(self, files_with_size: Iterable[Tuple[Path, FileSize]]) -> Set[FileIndex]:
        """
        Core function for update new files to JustOne object.

        Ignore the FileNotFoundError and PermissionError if self.ignore_error is True.
        """
        size_dict_temp: DefaultDict[FileSize, Set[FileIndex]] = defaultdict(set)
        small_hash_dict_temp: DefaultDict[Tuple[FileSize, HashValue], Set[FileIndex]] = defaultdict(set)
        full_hash_dict_temp: DefaultDict[HashValue, Set[FileIndex]] = defaultdict(set)
        duplicate_files_index: Set[FileIndex] = set()
        for file, file_size in tqdm(files_with_size, 'Fill size-dict'):
            try:
                file_index = self._add_file_info(file, file_size=file_size)
            # the file access might've changed till the exec point got here
            except FileNotFoundError as e:
                if self.ignore_error:
                    continue
                raise UpdateError from e
            size_dict_temp[file_size].add(file_index)
        for file_size, file_index in tqdm(self._merge_size_dict(size_dict_temp), 'Fill small-hash-dict'):
            try:
                small_hash = self._get_small_hash(file_index)
            # the file access might've changed till the exec point got here
            except (FileNotFoundError, PermissionError) as e:
                if self.ignore_error:
                    continue
                raise UpdateError from e
            except OSError as e:
                raise UpdateError from e
            small_hash_dict_temp[(file_size, small_hash)].add(file_index)
        # For all files with the hash on the first 1024 bytes, get their hash on the full
        # file - collisions will be duplicates
        for file_index in tqdm(self._merge_small_hash_dict(small_hash_dict_temp), 'Fill full-hash-dict'):
            try:
                full_hash = self._get_full_hash(file_index)
            # the file access might've changed till the exec point got here
            except (FileNotFoundError, PermissionError) as e:
                if self.ignore_error:
                    continue
                raise UpdateError from e
            except OSError as e: # TODO: replace with more specific Exceptions
                raise UpdateError from e
            full_hash_dict_temp[full_hash].add(file_index)
        for file_index in tqdm(self._merge_full_hash_dict(full_hash_dict_temp), 'Get duplicate-files'):
            duplicate_files_index.add(file_index)
        return duplicate_files_index

    def _update_multiple_files(self, files: IterablePaths) -> Set[FileIndex]:
        """
        Update multiple regular files to JustOne object.
        """
        files_with_size: List[Tuple[Path, FileSize]] = []
        for file in tqdm(files, 'Get size-of-file'):
            file = Path(file)
            try:
                file_stat = file.stat()
            except FileNotFoundError as e:
                if self.ignore_error:
                    continue
                raise UpdateError from e
            is_reg = stat.S_ISREG(file_stat.st_mode) # TODO: is symlink ...
            if not is_reg:
                if self.ignore_error:
                    continue
                raise UpdateError(f'Not a Regular File: {file}')
            file_size = file_stat.st_size
            files_with_size.append((file, file_size))
        return self._update_multiple_files_with_size(files_with_size)

    def _update_multiple_directories(self, dirs: IterablePaths) -> Set[FileIndex]:
        """
        Update multiple directories(all inner files recursively) to JustOne object.
        """
        files_with_size_iters: List[Generator] = []
        try:
            for d in dirs:
                files_with_size_iters.append(
                    (Path(entry.path), entry.stat().st_size) for entry in tqdm(JustOne._scan_dir(d, ignore_error=self.ignore_error), 'Dig all file'))
        except OSError as e: # TODO: replace with more specific Exceptions
            # not accessible (permissions, etc)
            raise UpdateError from e
        files_with_size: Iterator[Tuple[Path, FileSize]] = itertools.chain(*files_with_size_iters)
        return self._update_multiple_files_with_size(files_with_size)

    # No use for the time being.
    def _update_single_file(self, single_file: SinglePath) -> Set[FileIndex]:
        """
        Update one file to JustOne object.
        """
        return self._update_multiple_files((single_file, ))

    def update(self, arg: Union[SinglePath, IterablePaths], *args: Union[SinglePath, IterablePaths]) -> 'JustOne':
        """The main api for JustOne object to process files.

        Args:
            arg: File or folder path.
            args: Files' path if arg is file, or folders' path if arg is folder.

        Returns:
            Self JustOne object, for chain calling like `JustOne(hashlib.sha1).update('D:/data').update(Path('C:/Wegame')).duplicates()`.

        Raises:
            UpdateError: Raises an exception if something wrong.
        
        e.g.:
          1. update(file_1, file_2, file_3)    [Not Recommended]: file stat() calling which is too slow.
          2. update(iterable_files)            [Not Recommended]: ditto.
            - update([file_1, file_2])
            - update((f for f in Path.cwd().glob('*') if f.is_file()))  # Note: This is a slow method because of f.is_file().
          3. update(dir_1, dir_2, dir_3)       [Recommended]
          4. update(iterable_dirs)             [Recommended]
            - update([dir_1, dir_2])
            - update((f for f in Path.cwd().iterdir() if f.is_dir()))  # Note: This is a slow method because of f.is_dir().
        
        * Not support mix file and directory as arguments, such as update(file_1, dir_1) OR update(file_1, [dir_1, dir_2]).
        """
        args_iter = itertools.chain(*((a, ) if isinstance(a, (str, Path)) else a for a in (arg, *args)))
        args_iter, peek = itertools.tee(args_iter)
        first = next(peek, None)
        if first is None:
            # No Path element in arg and args
            return self
        if Path(first).is_dir():
            result: Set[FileIndex] = self._update_multiple_directories(args_iter)
        else:
            result: Set[FileIndex] = self._update_multiple_files(args_iter)
        # # @Deprecated: Return Sequence[Path]
        # return tuple(self._get_file_info(file_index)[0] for file_index in result)
        return self

    def _duplicates_common(self) -> Iterator[Sequence[Path]]:
        """
        Get duplicate files by hash value.
        """
        for _, v in self.full_hash_dict.items():
            dups = tuple(self._get_file_info(file_index)[0] for file_index in v)
            if len(dups) > 1:
                yield dups

    def _duplicates_strict(self, shallow=True) -> Iterator[Sequence[Path]]:
        """
        Check the files which have same hash by filecmp, shallow or deep comparison.
        """
        for _, v in self.full_hash_dict.items():
            if len(v) <= 1:
                continue
            diff_files: List[List[Path]] = [] # [[A_1, A_2], [B_1, B_2, B_3], [C_1]]
            files = tuple(self._get_file_info(file_index)[0] for file_index in v)
            for file in files:
                for same_files in diff_files:
                    first = same_files[0]
                    if filecmp.cmp(file, first, shallow=shallow):
                        same_files.append(file)
                        break
                diff_files.append([file])
            for same_files in diff_files:
                yield tuple(same_files)

    def duplicates(self, strict_level: Union[StrictLevel, Literal[0, 1, 2]] = STRICT_LEVEL_DEFAULT) -> Iterator[Sequence[Path]]:
        """Get duplicate files.

        Args:
            strict_level:
                A level in StrictLevel, or its corresponding integer. (e.g.: StrictLevel.SHALLOW or 1)

                [0][COMMON] compare by hash value of the whole file.
                [1][SHALLOW] compare by file stat first, then byte-by-byte checking if stats are different.
                [2][BYTE_BY_BYTE] compare by byte-by-byte checking directly.
            
        Returns:
            Iterator for duplicate files.
            e.g.: [
                [file_A_1, file_A_2],
                [file_B_1, file_B_2, file_B_3],
                ...
            ]

        Raises:
            GetDuplicatesError: Raises an exception if something wrong.
        """
        if strict_level == StrictLevel.COMMON:
            return self._duplicates_common()
        elif strict_level == StrictLevel.SHALLOW:
            return self._duplicates_strict(shallow=True)
        elif strict_level == StrictLevel.BYTE_BY_BYTE:
            return self._duplicates_strict(shallow=False)
        else:
            raise GetDuplicatesError from TypeError('the type of argument strict_level is not StrictLevel')

    # simple api
    __call__ = update

    # short api name
    dup = duplicates


def print_duplicates(dirpath: Path,
                     *dirpaths: Path,
                     output: TextIO = sys.stdout,
                     strict_level: Union[StrictLevel, Literal[0, 1, 2]] = STRICT_LEVEL_DEFAULT,
                     ignore_error: bool = False,
                     time_it: bool = False) -> int:
    """Print duplicate files.

    Sample:
        # Output the duplicate files in folders `dir1` and `dir2` to file `dupFiles.txt`.
        with open('dupFiles.txt', 'wt', encoding='utf-8') as f:
            print_duplicates('./dir1/', './dir2/', output=f, strict_level=1, ignore_error=True, time_it=True)
    
    Return:
        0 if success, other integers if fail.
    """
    justone = JustOne(ignore_error=ignore_error)
    start_time: float = time.time()
    try:
        duplicates_list = justone((dirpath, *dirpaths)).dup(strict_level) # equal to justone.update(...).duplicates()
    except JustOneError as e:
        print(f'Error: {format_exception_chain(e)}')
        if _DEBUG_MODE:
            traceback.print_exc(chain=True)
        return 1
    end_time: float = time.time()
    is_stdout: bool = output == sys.stdout
    for i, duplicates in enumerate(duplicates_list):
        if i != 0:
            print(f'', file=output) # divider
        if is_stdout:
            print(f'[{i+1}] Duplicate found:', file=output)
        for fp in duplicates:
            try:
                print(f'{" - " if is_stdout else ""}{fp}', file=output)
            except UnicodeEncodeError:
                print(f'{" - " if is_stdout else ""}{bytes(fp)}  [File Name Unicode Encode Error]', file=output)
    if time_it:
        print(f'\nTime Waste: {end_time-start_time:.2f}s')
    return 0


def parse_args():
    def get_folder_path(path_string) -> Path:
        p = Path(path_string)
        if not p.is_dir():
            raise argparse.ArgumentTypeError(f'`{path_string}` is not a valid path for an existed folder.')
        return p

    def get_output_file(path_string) -> Path:
        p = Path(path_string)
        if p.is_dir():
            raise argparse.ArgumentTypeError(f'`{path_string}` is a path for an existed folder.')
        return p

    parser = argparse.ArgumentParser(description='Fast duplicate files finder', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('directory', metavar='FOLDER', type=get_folder_path, nargs='+', help='文件夹路径')
    parser.add_argument('-s',
                        '--strict',
                        action='count',
                        default=0,
                        help=(f'[0][default] Based on hash comparison.\n'
                              f'[1][-s] Shallow comparison based on file stat, and byte comparison when inconsistent, to prevent hash collision.\n'
                              f'[2][-ss] Strictly compare byte by byte to prevent file stat and hash collision.'))
    parser.add_argument('-i',
                        '--ignore-error',
                        action='store_const',
                        const=True,
                        default=False,
                        help='Ignore exceptions such as PermissionError or FileNotExisted.')
    parser.add_argument('-t', '--time', action='store_const', const=True, default=False, help='Show total time consumption.')
    parser.add_argument('-o', '--output', metavar='OUTPUT', type=get_output_file, default=None, help='Output result to file.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}', help='Show the current version of this command line tool.')

    args: argparse.Namespace = parser.parse_args()
    if args.strict not in (0, 1, 2):
        raise argparse.ArgumentTypeError(f'{args.strict} is not a valid value for file comparison strict level. (need -s or -ss)')
    return args


def main() -> int:
    try:
        args: argparse.Namespace = parse_args()
    except argparse.ArgumentTypeError as e:
        print(f'Cli arguments Error: {format_exception_chain(e)}')
        return 1
    dirs: Final[Sequence[Path]] = args.directory
    if args.output is not None:
        output: Path = args.output
        with output.open('wt') as f:
            return print_duplicates(*dirs, output=f, strict_level=args.strict, ignore_error=args.ignore_error, time_it=args.time)
    else:
        return print_duplicates(*dirs, output=sys.stdout, strict_level=args.strict, ignore_error=args.ignore_error, time_it=args.time)


if __name__ == '__main__':
    sys.exit(main())
