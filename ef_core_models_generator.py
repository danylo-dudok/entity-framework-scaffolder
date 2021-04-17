from typing import List, Final

BASH_AND_EXPRESSION: Final = ' && '
CREATE_PROJECT_COMMAND: Final = BASH_AND_EXPRESSION.join([
    'dotnet new console',
    'dotnet add package Microsoft.EntityFrameworkCore.SqlServer',
    'dotnet add package Microsoft.EntityFrameworkCore.Design',
])
SCAFFOLDING_COMMAND: Final = 'dotnet ef dbcontext scaffold \'{}\' Microsoft.EntityFrameworkCore.SqlServer -o Models'
CSPROJ_FILE_TEMPLATE: Final = '{}.csproj'
MAIN_EXEC_FILE_NAME: Final = 'Program.cs'
CONNECTION_STRING_ARGUMENT_NAME: Final = '--connection-string'


def run_bash(command: str) -> None:
    from subprocess import run
    run(command, shell=True, check=True, text=True)


def project_exists() -> bool:
    from pathlib import Path

    current_path = Path()
    file_names = [item.name for item in current_path.iterdir() if item.is_file()]
    dir_name = current_path.absolute().name
    csproj_name = CSPROJ_FILE_TEMPLATE.format(dir_name)

    needed_files = (csproj_name, MAIN_EXEC_FILE_NAME)
    project_has_needed_files = all(file in file_names for file in needed_files)

    return project_has_needed_files


def generate_models(connection_string: str) -> None:
    if not project_exists():
        run_bash(CREATE_PROJECT_COMMAND)

    command = SCAFFOLDING_COMMAND.format(connection_string)
    run_bash(command)


def replace_text_in_generated_files(connection_string: str, arguments: List[str]) -> None:
    exclude_arguments = (CONNECTION_STRING_ARGUMENT_NAME, connection_string)
    sentences_arguments = [
        arg for arg in arguments
        if arg not in exclude_arguments
    ]

    from replacer import replace_sentences
    replace_sentences(sentences_arguments)


def find_connection_string(bash_arguments: List[str]) -> str:
    connection_string_index = bash_arguments.index(CONNECTION_STRING_ARGUMENT_NAME) + 1
    connection_string = bash_arguments[connection_string_index]

    return connection_string


def main(bash_arguments: List[str]) -> None:
    connection_string = find_connection_string(bash_arguments)
    generate_models(connection_string)
    replace_text_in_generated_files(connection_string, bash_arguments)


if __name__ == '__main__':
    from sys import argv
    main(argv)
