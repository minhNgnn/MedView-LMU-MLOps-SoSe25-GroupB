import importlib
from unittest.mock import patch

import pytest


class TestEnvironmentVariables:
    @patch("backend.src.api.os.getenv")
    def test_missing_database_url_raises_error(self, mock_getenv):
        mock_getenv.return_value = None
        with pytest.raises(ValueError, match="DATABASE_URL environment variable is required"):
            importlib.reload(__import__("backend.src.api", fromlist=[""]))
