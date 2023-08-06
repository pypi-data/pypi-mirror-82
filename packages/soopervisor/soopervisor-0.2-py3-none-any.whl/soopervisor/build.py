from pathlib import Path

from soopervisor.script.ScriptConfig import ScriptConfig
from soopervisor.executors.LocalExecutor import LocalExecutor
from soopervisor.executors.DockerExecutor import DockerExecutor


def check_project(config):
    """
    Verify project has the right structure before running the script
    """
    if not Path(config.paths.environment).exists():
        raise FileNotFoundError(
            'An environment file was expected at: {}'.format(
                config.paths.environment))

    if not Path(config.paths.project,
                'pipeline.yaml').exists() and not config.args:
        raise FileNotFoundError('A "pipeline.yaml" is required to declare '
                                'run the pipeline')


def build_project(project_root, clean_products_path, dry_run):
    """
    Build a project using settings from a soopervisor.yaml file
    """
    config = ScriptConfig.from_path(project_root)

    print(f'Env prefix {config.environment_prefix}')
    print(config.paths)

    print(f'Output will be stored at: {config.storage.path}')

    check_project(config)

    if clean_products_path:
        print('Cleaning product root folder...')
        config.clean_products()

    if config.executor == 'local':
        executor = LocalExecutor(script_config=config)
    elif config.executor == 'docker':
        executor = DockerExecutor(script_config=config)
    else:
        raise ValueError('Unknown executor "{}"'.format(config.executor))

    print('Running script with executor: {}'.format(repr(executor)))

    if dry_run:
        print('Dry run, skipping execution...')
        print(f'Script:\n{config.to_script()}')
    else:
        executor.execute()
        print('Successful build!')
