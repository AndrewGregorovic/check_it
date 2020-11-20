import os


def get_env_var(env_var):
    value = os.environ.get(env_var)

    if not value:
        raise ValueError(f"{env_var} is not set")

    return value


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "check"
    
    # 1MB for file size uploads
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_env_var("DB_URI")

    @property
    def AWS_ACCESS_KEY_ID(self):
        return get_env_var("AWS_ACCESS_KEY")

    @property
    def AWS_SECRET_ACCESS_KEY(self):
        return get_env_var("AWS_SECRET_ACCESS_KEY")

    @property
    def AWS_S3_BUCKET(self):
        return get_env_var("AWS_S3_BUCKET")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        return get_env_var("JWT_SECRET_KEY")


class TestingConfig(Config):
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_env_var("DB_TEST_URI")


class WorkflowConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
elif environment == "workflow":
    app_config = WorkflowConfig()
else:
    app_config = DevelopmentConfig()
