import sys
from os.path import join
from sys import platform
from typing import List, Final
from pathlib import Path

UNIX_PLATFORMS: Final = ('linux', 'linux2', 'darwin')
RECURSIVE_ARGUMENT_NAME: Final = '--recursive'
PATH_ARGUMENT_NAME: Final = '--path'
SENTENCES_ARGUMENT_NAME: Final = '--sentences'


def file_name_doesnt_start_with_dot_in_unix(name: str) -> bool:
    return not name.startswith('.') or platform not in UNIX_PLATFORMS


def replace_content(file: Path, replace_list: List):
    content = file.read_text()

    for to_replace, value in replace_list:
        content = content.replace(to_replace, value)

    file.write_text(content)


def replace_in_file(path: str or Path, replace_list: List, is_recursive: bool) -> None:
    path = Path(path)

    for item in path.iterdir():
        name = item.name
        if item.is_file() and file_name_doesnt_start_with_dot_in_unix(name):
            replace_content(item, replace_list)
        elif item.is_dir() and is_recursive:
            dir_path = join(path, name)
            replace_in_file(dir_path, replace_list, is_recursive)


def replace_sentences(bash_arguments: List[str]) -> None:
    arguments = [*bash_arguments]
    is_recursive = RECURSIVE_ARGUMENT_NAME in arguments
    if is_recursive:
        arguments.remove(RECURSIVE_ARGUMENT_NAME)

    begin_path_index = arguments.index(PATH_ARGUMENT_NAME) + 1
    begin_sentences_index = arguments.index(SENTENCES_ARGUMENT_NAME) + 1

    path = arguments[begin_path_index]
    if not path:
        raise Exception('Invalid path.')

    sentences = (arguments[begin_sentences_index:]
                 if begin_path_index < begin_sentences_index
                 else arguments[begin_sentences_index:begin_path_index])
    if not sentences:
        raise Exception('No sentences to replace.')
    if len(sentences) % 2 != 0:
        raise Exception('Amount of sentences should be even.')

    sentences_iterator = iter(sentences)
    grouped_sentences = [*zip(sentences_iterator, sentences_iterator)]

    replace_in_file(path, grouped_sentences, is_recursive)


if __name__ == '__main__':
    replace_sentences(sys.argv)
