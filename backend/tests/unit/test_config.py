from app.core.config import Settings

def test_config_defaults():
    # pydantic_settings parses environment variables, but we can test defaults here
    settings = Settings(
        POSTGRES_SERVER="test-server",
        POSTGRES_USER="test-user",
        POSTGRES_PASSWORD="test-password",
        POSTGRES_DB="test-db",
        POSTGRES_PORT=1234
    )
    
    assert settings.POSTGRES_SERVER == "test-server"
    assert settings.POSTGRES_USER == "test-user"
    expected_uri = "postgresql://test-user:test-password@test-server:1234/test-db"
    assert settings.sqlalchemy_database_uri == expected_uri
