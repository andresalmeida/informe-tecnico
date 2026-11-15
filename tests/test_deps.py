"""A missing dependency gives an instruction, not a traceback."""
import subprocess
import sys
from pathlib import Path


def run_blocked(script, blocked):
    root = Path(__file__).resolve().parents[1]
    scripts = root / "skills" / "informe-tecnico" / "scripts"
    path = (Path(__file__).resolve().parent / script) if script == "self_test.py" else (scripts / script)
    code = ("import sys, runpy\n"
            f"sys.path.insert(0, {str(scripts)!r})\n"
            f"sys.modules[{blocked!r}] = None\n"
            f"sys.argv = [{script!r}]\n"
            f"runpy.run_path({str(path)!r}, run_name='__main__')\n")
    return subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)


def run_checks(example, root, checks, build):
    for script, blocked, pip_name in [('build_report.py', 'reportlab', 'reportlab'),
                                      ('check_report.py', 'pdfplumber', 'pdfplumber'),
                                      ('self_test.py', 'PIL', 'Pillow')]:
        result = run_blocked(script, blocked)
        assert result.returncode == 2, (script, result.returncode, result.stderr)
        assert 'Traceback' not in result.stderr, result.stderr
        assert pip_name in result.stderr and 'pip install' in result.stderr and script in result.stderr, result.stderr
        assert '~/.cache/informe-venv' in result.stderr, result.stderr
        checks.append({'case': 'dependencias-faltantes-' + script.replace('.py', ''), 'exit': result.returncode})
