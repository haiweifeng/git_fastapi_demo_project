import os
# 项目根路径
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 日志文件路径
LOG_PATH: str = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
# -----------------------修改区-------------------------------------
DEBUG = True

RABMQ_HOST: str = "10.10.25.111" if DEBUG else '线上地址' # xxx.xx.xx.xxx
RABMQ_PORT:int = 5672
RABMQ_USERNAME: str = "feng" if DEBUG else '线上账号'
RABMQ_PASSWORD: str = "feng1991" if DEBUG else '线上密码'
RABMQ_VHOST: str = "/"
# redis配置
REDIS_URL: str = "127.0.0.1"
REDIS_PASS: str = "pwd" if DEBUG else "pwd"
REDIS_DB: int = 3
REDIS_PORT: int = 6379
# postgres 配置
MODEL_PATH: str = "models"

POSTGRES_HOST = '10.10.25.111' if DEBUG else "xxx.xx.xx.xxx"  # 线上地址
POSTGRES_USER = 'postgres' if DEBUG else "xxx"
POSTGRES_PWD = 'feng1991' if DEBUG else "xxxxxx"
POSTDB = 'feijiu_business_db' if DEBUG else "django_demo_db"
TORTOISE_CONFIG = {
                'connections': {
                    # Dict format for connection
                    'default': {
                        'engine': 'tortoise.backends.asyncpg',
                        'timezone':'Asia/Shanghai',
                        'credentials': {
                            'host': POSTGRES_HOST,
                            'port': '5432',
                            'user': POSTGRES_USER,
                            'password': POSTGRES_PWD,
                            'database': POSTDB,
                        },

                    },
                    # Using a DB_URL string
                    # 'default': f'postgres://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}:5432/{POSTDB}'
                },
                'apps': {
                    'models': {
                        "models": [MODEL_PATH],
                        'default_connection': 'default',
                    }
                },
                'use_tz': False,
                'timezone': 'Asia/Shanghai',
            }
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}:5432/{POSTDB}"

# ------------------以下不需要修改----------------------
TITLE: str = 'fastapi后端项目' if DEBUG else "线上项目"
DESCRIPTION: str = "Loding请点击页面..."
DOCS_URL = "/docs" if DEBUG else "/docs"
# 文档关联请求数据接口
OPENAPI_URL: str = "/openapi.json" if DEBUG else "/openapi.json"
# redoc 文档
REDOC_URL: str = "/redoc" if DEBUG else "/redoc"


NO_TOKEN_URL_LIST = ['/login', 'docs', 'favicon',
                     'openapi.json', 'static', 'redoc', '/logout',
                     ]

LOG_FILE = os.path.join(LOG_PATH, "loguru.log")
SELFKEY = '1234567890123456'  # 16位的加密秘钥
from loguru import logger
logger.add(LOG_FILE,
           format="{time:YYYY-MM-DD HH:mm:ss}|{level}|line:{line}|{message}",
           catch=True,
           # rotation='00:00',  # 每天0点生成一个 1 week
           level="INFO",
           rotation="10 MB",  # 日志大小
           # compression='zip', # 压缩为zip
           # retention='7 days',  # 保留7天
           backtrace=True,  # 追踪错误
           diagnose=True,  #
           enqueue=True,  # # 默认线程安全 指定异步和多进程安全
           encoding='utf-8')

