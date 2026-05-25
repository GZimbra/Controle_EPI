from datetime import date

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import Colaborador, EPI, UsuarioSistema
from app.models.enums import ConsentimentoCanal, EPICategoria
from app.schemas.colaborador import ColaboradorCreate, ConsentimentoInput, TamanhosColaborador
from app.schemas.epi import EPICreate
from app.services.colaborador_service import create_colaborador
from app.services.epi_service import create_epi


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if not db.query(UsuarioSistema).filter_by(username="admin").first():
            db.add(
                UsuarioSistema(
                    username="admin",
                    password_hash=get_password_hash("admin123-change"),
                    matricula="SESMT001",
                    role="admin",
                )
            )
            db.commit()
        if not db.query(EPI).filter_by(ca_numero="CA-12345").first():
            create_epi(
                db,
                EPICreate(
                    nome="Capacete classe B",
                    ca_numero="CA-12345",
                    validade_ca=date(2028, 12, 31),
                    categoria=EPICategoria.cabeca,
                    tamanhos_disponiveis=["M", "G"],
                    estoque_atual=50,
                    estoque_minimo=10,
                    fornecedor="Fornecedor Seguro LTDA",
                ),
            )
        if not db.query(Colaborador).filter_by(matricula="COL001").first():
            create_colaborador(
                db,
                ColaboradorCreate(
                    matricula="COL001",
                    nome_completo="Colaborador Exemplo",
                    cargo="Técnico de Manutenção",
                    setor="Operações",
                    cpf="11144477735",
                    tamanhos=TamanhosColaborador(capacete="M", luva="G", bota="42", camiseta="G"),
                    consentimento=ConsentimentoInput(versao="2026-05-25", canal=ConsentimentoCanal.web),
                ),
            )
    print("Seed concluído. Usuário: admin / senha: admin123-change")


if __name__ == "__main__":
    main()
