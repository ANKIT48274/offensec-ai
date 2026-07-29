"""Tests for application services."""

import pytest


class TestUserService:
    @pytest.mark.asyncio
    async def test_register_creates_user(self):
        pass

    @pytest.mark.asyncio
    async def test_register_duplicate_email_raises_error(self):
        pass

    @pytest.mark.asyncio
    async def test_authenticate_valid_credentials(self):
        pass

    @pytest.mark.asyncio
    async def test_authenticate_invalid_password(self):
        pass


class TestProjectService:
    @pytest.mark.asyncio
    async def test_create_project(self):
        pass

    @pytest.mark.asyncio
    async def test_get_project_by_id(self):
        pass

    @pytest.mark.asyncio
    async def test_list_projects_by_owner(self):
        pass

    @pytest.mark.asyncio
    async def test_delete_project_validates_owner(self):
        pass
