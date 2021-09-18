"""
The tests need the env vars to be set with the credentials.
"""
import pytest
import contextlib
import os
import copy

from vitiplace_client.website_view import (
    VitiplaceView,
    VITIPLACE_CLIENT_EMAIL_VAR_NAME,
    VITIPLACE_CLIENT_PASSWORD_VAR_NAME,
)


@contextlib.contextmanager
def disable_credential_env_vars():
    previous_environ = copy.deepcopy(os.environ)
    del os.environ[VITIPLACE_CLIENT_EMAIL_VAR_NAME]
    del os.environ[VITIPLACE_CLIENT_PASSWORD_VAR_NAME]

    yield

    os.environ = previous_environ


class TestWebsiteView:
    @pytest.fixture
    def viti_logged_view(self) -> VitiplaceView:
        viti_view = VitiplaceView()
        viti_view.login()

        return viti_view

    def test_login(self) -> None:
        viti_view = VitiplaceView()
        assert viti_view.is_login is False

        viti_view.login()
        assert viti_view.is_login is True

        email = os.environ[VITIPLACE_CLIENT_EMAIL_VAR_NAME]
        password = os.environ[VITIPLACE_CLIENT_PASSWORD_VAR_NAME]

        with disable_credential_env_vars():
            viti_view.is_login = False

            with pytest.raises(KeyError):
                viti_view = VitiplaceView()

            with pytest.raises(KeyError):
                viti_view = VitiplaceView(email=email)

            with pytest.raises(KeyError):
                viti_view = VitiplaceView(password=password)

            viti_view = VitiplaceView(email=email, password=password)
            viti_view.login()
            assert viti_view.is_login is True

    def test_get_board_page(self, viti_logged_view: VitiplaceView) -> None:
        page = viti_logged_view.get_board_page()
        assert len(page) > 0

        page = viti_logged_view.get_history_page()
        assert len(page) > 0

    def test_get_visual_page(self, viti_logged_view: VitiplaceView) -> None:
        page = viti_logged_view.get_visual_page()
        assert len(page) > 0

    def test_get_wine_information(self, viti_logged_view: VitiplaceView) -> None:
        # FIXME: Make agnostic
        wine_id = 395529
        wine_info = viti_logged_view.get_wine_information(id=wine_id)
        assert "vin" in wine_info

    def test_get_page(self, viti_logged_view: VitiplaceView) -> None:
        # Public URL
        wine_page_url = "https://vin.vitiplace.com/sauternes/yquem-284.php"
        page = viti_logged_view.get_page(wine_page_url)
        assert len(page) > 0
