import os

# https://fastapi.tiangolo.com/advanced/settings/
env = os.environ.get('WORKING_ENV', 'qa')
if env == 'dev':
    from .config_dev import *

    config = ConfigDev

elif env == 'qa':
    from .config_qa import *

    config = ConfigQA

elif env == 'prod':
    from .config_prod import *

    config = ConfigProd
