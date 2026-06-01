#Tabela de movimentaçãp

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class Tipo_de_movimentacao(str, enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo = Column(Enum(Tipo_de_movimentacao), nullable=False)
    quantidade = Column(Float, nullable=False)
    preco_unitario = Column(Float, nullable=False, default=0.0)
    observacao = Column(String, nullable=True)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())

    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=False)

    #Relacionamento
    produto = relationship("Produto", backref="movimentacoes")
    usuario = relationship("Usuario", backref="movimentacoes")

    @property
    def valor_total(self):
        return self.quantidade * self.preco_unitario