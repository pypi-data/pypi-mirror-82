import os
from typing import TYPE_CHECKING

from .compile_result import CompileResult
from .file_result import FileResult
from .test_result import TestResult
from ..common import cat, get_modification_time, run, pipe
from ..common.modification_time import ModificationTime
from ..common.run_status import RunStatus
from ..formatters.truncate import truncate

if TYPE_CHECKING:
    from ..specs.spec import SpecFile


def get_file(file_spec: 'SpecFile', file_result: FileResult) -> bool:
    file_status, file_contents = cat(file_spec.file_name)
    if file_status is RunStatus.SUCCESS:
        file_result.last_modified, _ = get_modification_time(file_spec.file_name, os.getcwd(), ModificationTime.LATEST)

    if file_spec.options.hide_contents:
        file_contents = ''
    elif file_spec.options.truncate_contents:
        file_contents = truncate(file_contents, file_spec.options.truncate_contents)

    if file_status is not RunStatus.SUCCESS:
        file_result.file_missing = True
        file_result.other_files = os.listdir('.')
        file_result.optional = file_spec.options.optional
        return False
    else:
        file_result.compile_optional = file_spec.options.compile_optional
        file_result.contents = file_contents
        return True


def parse_command(command: str, *, file_name: str, supporting_dir: str) -> str:
    return command \
        .replace('$@', './' + file_name) \
        .replace('$SUPPORT', supporting_dir)


def compile_file(*, file_spec: 'SpecFile', results: FileResult, supporting_dir: str) -> bool:
    for command in file_spec.compile_commands:
        command = parse_command(command,
                                file_name=file_spec.file_name,
                                supporting_dir=supporting_dir)

        cmd, input_for_cmd = pipe(command)
        status, compile_output, _ = run(cmd, timeout=30, input_data=input_for_cmd)

        results.compile_results.append(CompileResult(command=command,
                                                     output=compile_output,
                                                     status=status))

        if status is not RunStatus.SUCCESS:
            return False

    return True


def test_file(*,
              file_spec: 'SpecFile',
              file_results: FileResult,
              supporting_dir: str,
              interact: bool):
    for command in file_spec.test_commands:
        if not command:
            continue

        command = parse_command(command,
                                file_name=file_spec.file_name,
                                supporting_dir=supporting_dir)

        test_cmd, input_for_test = pipe(command)

        again = True
        while again:
            status, full_result, again = run(test_cmd,
                                             input_data=input_for_test,
                                             timeout=file_spec.options.timeout,
                                             interact=interact)

            result = truncate(full_result, file_spec.options.truncate_output)
            was_truncated = (full_result != result)

            file_results.test_results.append(TestResult(
                command=command,
                output=result,
                status=status,
                error=status != RunStatus.SUCCESS,
                truncated=was_truncated,
                truncated_after=file_spec.options.truncate_output,
            ))


def process_file(*,
                 file_spec: 'SpecFile',
                 supporting_dir: str,
                 interact: bool,
                 skip_web_compile: bool) -> FileResult:
    file_result = FileResult(file_name=file_spec.file_name)

    should_continue = get_file(file_spec, file_result)

    if should_continue and not (skip_web_compile and file_spec.options.web_file):
        should_continue = compile_file(file_spec=file_spec,
                                       results=file_result,
                                       supporting_dir=supporting_dir)

    if should_continue and not file_spec.options.web_file:
        test_file(file_spec=file_spec,
                  file_results=file_result,
                  supporting_dir=supporting_dir,
                  interact=interact)

    return file_result
