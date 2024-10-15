import os
import sys
import traceback
from pathlib import Path


def error_msg(err):
    error_class = err.__class__.__name__
    if len(err.args) > 0:
        detail = err.args[0]
    else:
        detail = ''
    cl, exc, tb = sys.exc_info()
    cwd = Path(os.getcwd())
    error_details = []
    for s in traceback.extract_tb(tb):
        slack_path = Path(s[0])
        line_number = s[1]
        module_name = s[2]
        if slack_path.is_relative_to(cwd):
            path_detail = slack_path.relative_to(cwd)
        else:
            path_detail = slack_path.name
        info = f"File \"{path_detail}\", line {line_number} in {module_name}"
        error_details.append(info)
    details = '\n'.join(error_details)
    err_msg = f"\n[{error_class}] {detail}"
    return f"\n{details}{err_msg}\n"
