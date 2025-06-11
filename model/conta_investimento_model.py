from dataclasses import dataclass

@dataclass
class ContaInvestimento:
    id_conta: int
    perfil_risco: str  # Exemplo: 'CONSERVADOR', 'MODERADO', 'AGRESSIVO'
    valor_minimo: float
    taxa_rendimento_base: float
