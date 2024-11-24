from litestar import Litestar


def path_to_route_name(app: Litestar, path: str) -> str:
    app, handler, path, params = app.asgi_router.handle_routing(path, "OPTIONS")
    return next(iter(handler.paths))
