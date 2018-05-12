import subprocess as sp


def run_command(cmd, retcode=0):
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    code = p.wait()
    stdout, _ = p.communicate()
    stdout = stdout.replace(b"\x1b[?1034h", b"")
    if code != retcode:
        print(stdout)
        raise RuntimeError("command returned unexpected code: {}".format(code))
    return stdout
