project('orchestration', meson_version: '>=1.12.0')

source_root = meson.project_source_root()
build_root = meson.project_build_root()
linter = find_program('orchestration-linter', required: true)
installer = find_program('rulebook-install', required: true)
sync = find_program('build-sync', required: true)
git = find_program('git', required: true)

burn_input = get_option('burn_input')
lint_mode_args = []
if burn_input != ''
  lint_mode_args = ['--public-pack', '--burn-input', burn_input]
endif
domain = get_option('domain')
release_tag = get_option('release_tag')
release_commit = ''
if release_tag != ''
  release_commit = run_command(git, '-C', source_root, 'rev-parse', 'HEAD', check: true).stdout().strip()
  tagged_commit = run_command(git, '-C', source_root, 'rev-list', '-n', '1', release_tag, check: true).stdout().strip()
  dirty = run_command(git, '-C', source_root, 'status', '--porcelain', check: true).stdout().strip()
  if tagged_commit != release_commit or dirty != ''
    error('release_tag must name HEAD over a clean tree')
  endif
endif

subdir('adr')
subdir('docs/spec')
subdir('docs')

linter_paths = [
  '.linter/environments.toml',
  '.linter/imports/tools.toml',
  '.linter/lists.toml',
  '.linter/owners.toml',
  '.linter/policies.toml',
  '.linter/policy-assembly-publications.toml',
  '.linter/policy-interchange.toml',
  '.linter/policy-legacy-implementation.toml',
  '.linter/policy-legacy-record-references-repository.toml',
  '.linter/policy-legacy-record-references.toml',
  '.linter/policy-legacy-section-references-repository.toml',
  '.linter/policy-legacy-section-references.toml',
  '.linter/policy-legacy-tag-references.toml',
  '.linter/policy-legacy-todos.toml',
  '.linter/policy-legacy-unprefixed-record-references.toml',
  '.linter/policy-owner-names.toml',
  '.linter/policy-public-pack-values.toml',
  '.linter/policy-references-divisions.toml',
  '.linter/policy-references-path-linking.toml',
  '.linter/policy-references-prefix-numbers.toml',
  '.linter/policy-references-scenarios.toml',
  '.linter/policy-spdx.toml',
  '.linter/shape.toml',
]
root_paths = ['.gitignore', 'CHANGELOG.md', 'CLAUDE.md', 'LICENSE-CODE', 'LICENSE-DOCS', 'ORCHESTRATION.md', 'README.md', 'maps/generic-map.toml', 'public-set.toml']
example_subject_paths = []
example_relative_subjects = []
foreach path : example_names_paths
  if path != 'docs/examples/meson.build' and path != 'docs/examples/meson.options'
    example_subject_paths += path
  endif
endforeach
foreach name : example_names
  if name != 'examples/meson.build' and name != 'examples/meson.options'
    example_relative_subjects += name.replace('examples/', '')
  endif
endforeach
prose_paths = adr_names_paths + spec_names_paths + docs_top_names_paths + coreos_names_paths + reference_names_paths + proposal_names_paths + ['CHANGELOG.md', 'CLAUDE.md', 'ORCHESTRATION.md', 'README.md']
foreach path : example_subject_paths
  if path.endswith('.md')
    prose_paths += path
  endif
endforeach
declared_paths = linter_paths + root_paths + adr_names_paths + spec_names_paths + docs_top_names_paths + coreos_names_paths + reference_names_paths + proposal_names_paths + example_subject_paths + ['docs/spec.md']

# Build definitions are Meson's graph, not linter subjects.
# maps/list.in and maps/empty.in are configuration templates and are excluded from the subject census.
excluded_pattern = '(^|/)meson[.](build|options)$|^maps/(list|empty)[.]in$'
declared_list = configure_file(input: 'maps/list.in', output: 'declared-paths.txt', configuration: {'PATHS': '\n'.join(declared_paths)})
excluded_list = configure_file(input: 'maps/empty.in', output: 'excluded-paths.txt', copy: true)
example_list = configure_file(input: 'maps/list.in', output: 'example-paths.txt', configuration: {'PATHS': '\n'.join(example_relative_subjects)})
example_excluded = configure_file(input: 'maps/empty.in', output: 'example-excluded.txt', copy: true)

check_inputs = []
fmt_inputs = []
project_inputs = []
assembly_inputs = []
export_inputs = []
fmt_args = []
foreach path : declared_paths
  if path != '.gitignore'
    check_inputs += files(path)
  endif
endforeach
foreach path : prose_paths
  fmt_inputs += files(path)
  fmt_args += source_root / path
endforeach
foreach path : linter_paths
  project_inputs += files(path)
  export_inputs += files(path)
endforeach
foreach path : adr_names_paths + spec_names_paths + docs_top_names_paths + coreos_names_paths + reference_names_paths + proposal_names_paths + ['CLAUDE.md', 'ORCHESTRATION.md', 'README.md']
  export_inputs += files(path)
endforeach
foreach path : spec_names_paths + ['docs/spec.md']
  assembly_inputs += files(path)
endforeach

check_stamp = custom_target('linter-check', input: check_inputs, output: ['linter-check.stamp', 'linter-check.json'], command: [linter, 'check'] + lint_mode_args + ['--root', source_root, '--write-report', '@OUTPUT1@', '--write-stamp', '@OUTPUT0@'], build_by_default: true)
fmt_stamp = custom_target('linter-fmt', input: fmt_inputs, output: ['linter-fmt.stamp', 'linter-fmt.json'], command: [linter, 'fmt', '--check', '--write-report', '@OUTPUT1@', '--write-stamp', '@OUTPUT0@'] + fmt_args, build_by_default: true)
project_stamp = custom_target('linter-project', input: project_inputs, output: ['linter-project.stamp', 'linter-project.json'], command: [linter, 'project'] + lint_mode_args + ['--root', source_root, '--write-report', '@OUTPUT1@', '--write-stamp', '@OUTPUT0@'], build_by_default: true)
assembly_stamp = custom_target('spec-assembly', input: assembly_inputs, output: ['spec-assembly.stamp', 'spec-assembly.json'], command: [linter, 'assemble'] + lint_mode_args + ['--root', source_root, '--write-report', '@OUTPUT1@', '--write-stamp', '@OUTPUT0@'], build_by_default: true)
census_stamp = custom_target('census', input: [declared_list, excluded_list], output: ['census.stamp', 'census.json'], command: [linter, 'census'] + lint_mode_args + ['--root', source_root, '--declared', declared_list, '--excluded', excluded_list, '--pattern', excluded_pattern, '--write-report', '@OUTPUT1@', '--write-stamp', '@OUTPUT0@'], build_always_stale: true, build_by_default: true)
labels_export = custom_target('labels-export', input: export_inputs, output: 'labels.toml', command: [linter, 'export'] + lint_mode_args + ['--root', source_root, '--owner', 'ORCHESTRATION', '--out', '@OUTPUT0@'], build_by_default: true)

run_target('spec-assemble', command: [linter, 'assemble'] + lint_mode_args + ['--root', source_root, '--write'])
run_target('linter-project-write', command: [linter, 'project'] + lint_mode_args + ['--root', source_root, '--write'])
run_target('linter-fmt-write', command: [linter, 'fmt'] + fmt_args)

test('linter-check', sync, args: ['--probe', check_stamp[0]], depends: check_stamp, suite: 'lint', timeout: 120)
test('linter-fmt', sync, args: ['--probe', fmt_stamp[0]], depends: fmt_stamp, suite: 'lint', timeout: 120)
test('linter-project', sync, args: ['--probe', project_stamp[0]], depends: project_stamp, suite: 'lint', timeout: 120)
test('spec-assembly', sync, args: ['--probe', assembly_stamp[0]], depends: assembly_stamp, suite: 'lint', timeout: 120)

example_root = source_root / 'docs/examples'
test('example-census', linter, args: ['census', '--root', example_root, '--declared', example_list, '--excluded', example_excluded, '--pattern', '^meson[.](build|options)$', '--required', example_root / 'instance-contract.toml'], suite: 'template', timeout: 120)
test('example-check', linter, args: ['check', '--root', example_root], suite: 'template', timeout: 120)
foreach map_name : ['routine-map', 'tools-map', 'install-map']
  stage_root = build_root / 'stage-' + map_name
  map_args = ['--map', example_root / 'rulebooks' / (map_name + '.toml'), '--shape-root', source_root]
  test(map_name + '-first', installer, args: map_args, env: {'DESTDIR': stage_root}, workdir: source_root, suite: 'template', timeout: 120, is_parallel: false, priority: 10)
  test(map_name + '-again', installer, args: map_args, env: {'DESTDIR': stage_root}, workdir: source_root, suite: 'template', timeout: 120, is_parallel: false, priority: 0)
endforeach

install_args = ['--map', source_root / 'maps/generic-map.toml', '--build-root', build_root]
if release_tag != ''
  install_args += ['--release-tag', release_tag, '--release-commit', release_commit]
endif
meson.add_install_script(installer, install_args)
