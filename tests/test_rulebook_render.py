"""Exercise production rendering without embedding instance values in fixtures."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

installer, source, instance = sys.argv[1:]
source = Path(source).resolve()


def render_case(root, map_path, description):
    document = tomllib.loads(map_path.read_text())
    targets = [t for t in document['targets'] if t.get('kind') == 'render' and t.get('base') == 'ORCHESTRATION.md']
    assert len(targets) == 1, 'rulebook-render-target: expected one orchestration render'
    target = targets[0]
    assert target.get('max_bytes') == 9500, 'rulebook-bound: instance must retain the hook limit'
    with tempfile.TemporaryDirectory(prefix='rulebook-render-') as directory:
        temporary = Path(directory)
        mapping = temporary / 'render.toml'
        # Isolate the declared render from unrelated installation copy targets.
        def write_map(bound, destination):
            mapping.write_text('root = ' + json.dumps('/' + destination) + '\n\n[[targets]]\n'
                               + 'kind = "render"\nbase = "ORCHESTRATION.md"\n'
                               + 'overlay = ' + json.dumps(target['overlay']) + '\n'
                               + 'destination = "ORCHESTRATION.md"\nmode = "0644"\n'
                               + f'max_bytes = {bound}\n')
        def run():
            return subprocess.run([installer, '--map', str(mapping), '--shape-root', str(source), '--destdir', str(temporary / 'stage')], cwd=root, capture_output=True, text=True)
        write_map(9500, 'accepted')
        result = run()
        # Do not echo output containing private overlay text on refusal.
        assert result.returncode == 0, f'{description}: production-render-refused (exit {result.returncode})'
        payload = (temporary / 'stage/accepted/ORCHESTRATION.md').read_bytes()
        payload.decode('utf-8')
        assert 0 < len(payload) <= 9500, 'rulebook-bound: rendered byte count exceeds hook limit'
        print(f'{description}: rendered_bytes={len(payload)} maximum=9500 headroom={9500-len(payload)}', flush=True)
        write_map(len(payload) - 1, 'refused')
        result = run()
        assert result.returncode != 0 and 'rendered_size' in result.stdout + result.stderr, 'rulebook-bound: missing named rendered_size refusal'
        assert not (temporary / 'stage/refused/ORCHESTRATION.md').exists(), 'rulebook-bound: refused render was published'


render_case(source, source / 'docs/examples/rulebooks/tools-map.toml', 'fictional-instance')
if instance:
    root = Path(instance).resolve()
    render_case(root, root / 'rulebooks/tools-map.toml', 'external-instance')
else:
    print('external-instance: NOT SELECTED; fictional render is not instance acceptance')
