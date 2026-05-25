"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-25
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "epis",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(160), nullable=False),
        sa.Column("ca_numero", sa.String(40), nullable=False),
        sa.Column("validade_ca", sa.Date(), nullable=False),
        sa.Column("categoria", sa.Enum("protecao_auditiva", "visual", "respiratoria", "cabeca", "maos", "pes", "queda", name="epicategoria"), nullable=False),
        sa.Column("tamanhos_disponiveis", sa.Text(), nullable=True),
        sa.Column("estoque_atual", sa.Integer(), nullable=False),
        sa.Column("estoque_minimo", sa.Integer(), nullable=False),
        sa.Column("fornecedor", sa.String(160), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("ca_numero", name="uq_epis_ca_numero"),
    )
    op.create_index("ix_epis_ca_numero", "epis", ["ca_numero"])
    op.create_index("ix_epis_deleted_at", "epis", ["deleted_at"])

    op.create_table(
        "colaboradores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("matricula", sa.String(50), nullable=False),
        sa.Column("nome_completo", sa.String(180), nullable=False),
        sa.Column("cargo", sa.String(120), nullable=False),
        sa.Column("setor", sa.String(120), nullable=False),
        sa.Column("tamanho_capacete", sa.String(20), nullable=True),
        sa.Column("tamanho_luva", sa.String(20), nullable=True),
        sa.Column("tamanho_bota", sa.String(20), nullable=True),
        sa.Column("tamanho_camiseta", sa.String(20), nullable=True),
        sa.Column("cpf_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("cpf_salt", sa.String(32), nullable=False),
        sa.Column("consentimento_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consentimento_versao", sa.String(40), nullable=False),
        sa.Column("consentimento_canal", sa.Enum("web", "tablet", "papel_digitalizado", "integracao", name="consentimentocanal"), nullable=False),
        sa.Column("consentimento_revogado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("matricula", name="uq_colaboradores_matricula"),
    )
    op.create_index("ix_colaboradores_matricula", "colaboradores", ["matricula"])
    op.create_index("ix_colaboradores_deleted_at", "colaboradores", ["deleted_at"])

    op.create_table(
        "usuarios_sistema",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(80), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("matricula", sa.String(50), nullable=True),
        sa.Column("role", sa.String(40), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_usuarios_sistema_username", "usuarios_sistema", ["username"])
    op.create_index("ix_usuarios_sistema_deleted_at", "usuarios_sistema", ["deleted_at"])

    op.create_table(
        "retiradas_epi",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("colaborador_id", sa.Integer(), sa.ForeignKey("colaboradores.id"), nullable=False),
        sa.Column("epi_id", sa.Integer(), sa.ForeignKey("epis.id"), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("data_retirada", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_devolucao_prevista", sa.Date(), nullable=True),
        sa.Column("autorizado_por_matricula", sa.String(50), nullable=False),
        sa.Column("status", sa.Enum("ativo", "devolvido", "perdido", "danificado", name="retiradastatus"), nullable=False),
        sa.Column("assinatura_hash", sa.String(64), nullable=False),
        sa.Column("assinatura_arquivo_criptografado", sa.String(260), nullable=False),
        sa.Column("ca_numero_entrega", sa.String(40), nullable=False),
        sa.Column("ca_validade_entrega", sa.Date(), nullable=False),
        sa.Column("devolvido_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_retiradas_epi_colaborador_id", "retiradas_epi", ["colaborador_id"])
    op.create_index("ix_retiradas_epi_epi_id", "retiradas_epi", ["epi_id"])
    op.create_index("ix_retiradas_epi_data_retirada", "retiradas_epi", ["data_retirada"])
    op.create_index("ix_retiradas_epi_deleted_at", "retiradas_epi", ["deleted_at"])

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tabela_afetada", sa.String(80), nullable=False),
        sa.Column("registro_id", sa.String(80), nullable=False),
        sa.Column("operacao", sa.Enum("INSERT", "UPDATE", "DELETE", name="auditoperacao"), nullable=False),
        sa.Column("campo_alterado", sa.String(120), nullable=True),
        sa.Column("valor_anterior", sa.Text(), nullable=True),
        sa.Column("valor_novo", sa.Text(), nullable=True),
        sa.Column("usuario_sistema", sa.String(120), nullable=False),
        sa.Column("ip_origem", sa.String(80), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_audit_log_tabela_afetada", "audit_log", ["tabela_afetada"])
    op.create_index("ix_audit_log_registro_id", "audit_log", ["registro_id"])


def downgrade() -> None:
    op.drop_table("audit_log")
    op.drop_table("retiradas_epi")
    op.drop_table("usuarios_sistema")
    op.drop_table("colaboradores")
    op.drop_table("epis")
