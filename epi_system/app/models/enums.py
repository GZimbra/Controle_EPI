import enum


class EPICategoria(str, enum.Enum):
    protecao_auditiva = "protecao_auditiva"
    visual = "visual"
    respiratoria = "respiratoria"
    cabeca = "cabeca"
    maos = "maos"
    pes = "pes"
    queda = "queda"


class RetiradaStatus(str, enum.Enum):
    ativo = "ativo"
    devolvido = "devolvido"
    perdido = "perdido"
    danificado = "danificado"


class AuditOperacao(str, enum.Enum):
    insert = "INSERT"
    update = "UPDATE"
    delete = "DELETE"


class ConsentimentoCanal(str, enum.Enum):
    web = "web"
    tablet = "tablet"
    papel_digitalizado = "papel_digitalizado"
    integracao = "integracao"
