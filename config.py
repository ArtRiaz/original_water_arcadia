from environs import Env

from dataclasses import dataclass

@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_DATABASE')
        ),
        misc=Miscellaneous()
    )


config = load_config()

POSTGRES_URL = f"postgres://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
PAYMENT_TOKEN = "1877036958:TEST:b48618a00463aa581864ca139be5e7a591e1fc15"
