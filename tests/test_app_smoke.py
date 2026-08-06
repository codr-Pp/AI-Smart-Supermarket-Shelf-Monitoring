from app import app


def test_core_routes_are_registered():
    routes = {rule.rule for rule in app.url_map.iter_rules()}

    assert "/" in routes
    assert "/upload" in routes
    assert "/latest" in routes
    assert "/export-report" in routes
    assert "/export-ml-report" in routes
