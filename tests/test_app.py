from simple_web_app.app import hello

def test_hello():
    assert "Hello from" in hello()
