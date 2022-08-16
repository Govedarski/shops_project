from resources.auth_resources import RegisterResource, LoginResource

routes = (
    (RegisterResource, "/register"),
    (LoginResource, "/login"),
)
