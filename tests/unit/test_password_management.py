"""
Unit tests for password management functionality.
"""

import os
from pathlib import Path
from unittest.mock import mock_open, patch

from src.htcli.utils.password import (
    clear_password_cache,
    get_cached_password,
    get_secure_password,
    prompt_for_password,
    set_cached_password,
    store_password,
)


class TestPasswordManagement:
    """Test password management functionality."""

    def test_get_secure_password_from_cache(self):
        """Test getting password from cache."""
        from src.htcli.utils.password import _password_cache

        _password_cache["test-key"] = "cached_password"

        result = get_secure_password("test-key")
        assert result == "cached_password"

        _password_cache.clear()

    def test_get_secure_password_from_env(self):
        """Test getting password from environment variable."""
        with patch.dict(os.environ, {"HTCLI_PASSWORD_TEST_KEY": "env_password"}):
            result = get_secure_password("test_key")
            assert result == "env_password"

    def test_get_secure_password_prompt(self):
        """Test getting password from user prompt."""
        with patch("src.htcli.utils.password.Prompt.ask") as mock_prompt:
            mock_prompt.return_value = "prompted_password"

            result = get_secure_password("test-key")
            assert result == "prompted_password"

    def test_prompt_for_password_success(self):
        """Test successful password prompting."""
        with patch("src.htcli.utils.password.Prompt.ask") as mock_prompt:
            mock_prompt.side_effect = ["test_password", "test_password"]

            result = prompt_for_password("Enter password", confirm=True)
            assert result == "test_password"

    def test_store_password_success(self):
        """Test successful password storage."""
        with patch("src.htcli.utils.password.Path.home") as mock_home:
            mock_home.return_value = Path("/tmp")

            with patch("src.htcli.utils.password.load_stored_passwords") as mock_load:
                mock_load.return_value = {"existing": "password"}

                with patch("builtins.open", mock_open()) as mock_file:
                    with patch(
                        "src.htcli.utils.password.encrypt_passwords"
                    ) as mock_encrypt:
                        mock_encrypt.return_value = b"encrypted_data"

                        result = store_password("test-key", "test_password")
                        assert result is True

    def test_clear_password_cache(self):
        """Test clearing password cache."""
        from src.htcli.utils.password import _password_cache

        _password_cache["test-key"] = "test_password"

        clear_password_cache()
        assert len(_password_cache) == 0

    def test_get_cached_password(self):
        """Test getting cached password."""
        from src.htcli.utils.password import _password_cache

        _password_cache["test-key"] = "cached_password"

        result = get_cached_password("test-key")
        assert result == "cached_password"

        _password_cache.clear()

    def test_set_cached_password(self):
        """Test setting cached password."""
        set_cached_password("test-key", "test_password")

        from src.htcli.utils.password import _password_cache

        assert _password_cache["test-key"] == "test_password"

        _password_cache.clear()
