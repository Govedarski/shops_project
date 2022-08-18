from managers.auth_manager import AuthManager


def assert_count_equal(count, model):
    assert len(model.query.all()) == count


def generate_token(user):
    token = AuthManager.encode_token(user)
    return token
