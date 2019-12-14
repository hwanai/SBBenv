from gym.envs.registration import register
register(id='SBBenv-v0',
    entry_point='envs.SBBenv_dir:SBBenv'
)