from datetime import date, timedelta

import pytest
from fastapi import HTTPException

from app.models.enums import EPICategoria
from app.models.epi import EPI
from app.services.epi_service import ensure_ca_vigente, ensure_stock


def test_ca_validation_blocks_expired():
    epi = EPI(nome="Respirador", ca_numero="CA1", validade_ca=date.today() - timedelta(days=1), categoria=EPICategoria.respiratoria, estoque_atual=1, estoque_minimo=0)
    with pytest.raises(HTTPException):
        ensure_ca_vigente(epi)


def test_stock_validation_blocks_insufficient():
    epi = EPI(nome="Luva", ca_numero="CA2", validade_ca=date.today() + timedelta(days=30), categoria=EPICategoria.maos, estoque_atual=1, estoque_minimo=0)
    with pytest.raises(HTTPException):
        ensure_stock(epi, 2)
