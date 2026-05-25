import base64
from datetime import UTC, date, datetime, timedelta

from app.models.colaborador import Colaborador
from app.models.enums import ConsentimentoCanal, EPICategoria
from app.models.epi import EPI
from app.schemas.retirada import RetiradaCreate
from app.services.retirada_service import criar_retirada


def test_withdrawal_decrements_stock(db, tmp_path, monkeypatch):
    monkeypatch.setenv("SIGNATURE_STORAGE_DIR", str(tmp_path))
    c = Colaborador(
        matricula="M2",
        nome_completo="Pessoa Teste",
        cargo="Tec",
        setor="Ops",
        cpf_hash="c" * 64,
        cpf_salt="d" * 32,
        consentimento_timestamp=datetime.now(UTC),
        consentimento_versao="v1",
        consentimento_canal=ConsentimentoCanal.web,
    )
    e = EPI(
        nome="Capacete",
        ca_numero="CA-OK",
        validade_ca=date.today() + timedelta(days=365),
        categoria=EPICategoria.cabeca,
        estoque_atual=10,
        estoque_minimo=2,
    )
    db.add_all([c, e])
    db.commit()
    retirada = criar_retirada(
        db,
        RetiradaCreate(
            colaborador_id=c.id,
            epi_id=e.id,
            quantidade=3,
            autorizado_por_matricula="SESMT",
            assinatura_base64=base64.b64encode(b"fake-png-signature-payload").decode(),
        ),
    )
    assert retirada.id
    assert e.estoque_atual == 7
