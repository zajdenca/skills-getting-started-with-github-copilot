from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_store

# Preserve a clean activities baseline so tests can reset global state.
original_activities = deepcopy(activities_store)

@pytest.fixture(autouse=True)
def reset_activities():
    activities_store.clear()
    activities_store.update(deepcopy(original_activities))

@pytest.fixture
def client():
    return TestClient(app)
