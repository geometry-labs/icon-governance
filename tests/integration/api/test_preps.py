from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from icon_governance.config import settings


def test_api_get_preps(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/preps")
    assert response.status_code == 200


def test_api_get_prep(db: Session, client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/preps/hx0b047c751658f7ce1b2595da34d57a0e7dad357d"
    )
    assert response.status_code == 200


def test_api_get_prep_error(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/preps/hx0b047c751658f7ce1b2595da34d57a0")
    assert response.status_code == 204
