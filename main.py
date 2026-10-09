from abc import ABC, abstractmethod
import re


class Cliente:
    """Representa um cliente do banco."""

    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome não pode ficar vazio.")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", valor
        ):
            raise ValueError("E-mail inválido. Exemplo: nome@email.com")
        self._email = valor.strip().lower()

    def __str__(self):
        return f"Cliente: {self.nome} | E-mail: {self.email}"

    def __repr__(self):
        return f"Cliente(nome={self.nome!r}, email={self.email!r})"

    def __eq__(self, outro):
        return isinstance(outro, Cliente) and self.email == outro.email


class Conta(ABC):
    """Classe abstrata que define o comportamento comum das contas."""

    _proximo_numero = 1001

    def __init__(self, titular: Cliente, saldo_inicial: float = 0.0):
        if not isinstance(titular, Cliente):
            raise TypeError("O titular deve ser um objeto Cliente.")
        self.numero = Conta._proximo_numero
        Conta._proximo_numero += 1
        self.titular = titular
        self.saldo = saldo_inicial

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise TypeError("O saldo deve ser numérico.")
        if valor < 0:
            raise ValueError("O saldo não pode ser negativo.")
        self._saldo = float(valor)

    def depositar(self, valor):
        self._validar_valor_positivo(valor)
        self.saldo = self.saldo + valor

    def sacar(self, valor):
        self._validar_valor_positivo(valor)
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo = self.saldo - valor

    @staticmethod
    def _validar_valor_positivo(valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise TypeError("O valor deve ser numérico.")
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

    @abstractmethod
    def calcular_rendimento(self):
        """Calcula o rendimento específico do tipo de conta."""
        raise NotImplementedError

    def __str__(self):
        return (
            f"{self.__class__.__name__} nº {self.numero} | "
            f"Titular: {self.titular.nome} | Saldo: R$ {self.saldo:.2f}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(titular={self.titular!r}, "
            f"saldo_inicial={self.saldo!r})"
        )

    def __eq__(self, outra):
        return isinstance(outra, Conta) and self.numero == outra.numero

    def __lt__(self, outra):
        if not isinstance(outra, Conta):
            return NotImplemented
        return self.saldo < outra.saldo


class ContaCorrente(Conta):
    """Conta corrente sem rendimento automático."""

    def __init__(self, titular: Cliente, saldo_inicial: float = 0.0,
                 tarifa_mensal: float = 12.0):
        super().__init__(titular, saldo_inicial)
        self.tarifa_mensal = tarifa_mensal

    @property
    def tarifa_mensal(self):
        return self._tarifa_mensal

    @tarifa_mensal.setter
    def tarifa_mensal(self, valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise TypeError("A tarifa deve ser numérica.")
        if valor < 0:
            raise ValueError("A tarifa não pode ser negativa.")
        self._tarifa_mensal = float(valor)

    def calcular_rendimento(self):
        return 0.0

    def cobrar_tarifa(self):
        if self.tarifa_mensal > self.saldo:
            raise ValueError("Saldo insuficiente para pagar a tarifa.")
        self.sacar(self.tarifa_mensal)

    def __str__(self):
        return f"{super().__str__()} | Tarifa mensal: R$ {self.tarifa_mensal:.2f}"

    def __repr__(self):
        return (
            f"ContaCorrente(titular={self.titular!r}, saldo_inicial={self.saldo!r}, "
            f"tarifa_mensal={self.tarifa_mensal!r})"
        )


class ContaPoupanca(Conta):
    """Conta poupança com taxa de rendimento."""

    def __init__(self, titular: Cliente, saldo_inicial: float = 0.0,
                 taxa_rendimento: float = 0.005):
        super().__init__(titular, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise TypeError("A taxa deve ser numérica.")
        if not 0 <= valor <= 1:
            raise ValueError("A taxa deve estar entre 0 e 1.")
        self._taxa_rendimento = float(valor)

    def calcular_rendimento(self):
        return self.saldo * self.taxa_rendimento

    def aplicar_rendimento(self):
        rendimento = self.calcular_rendimento()
        self.depositar(rendimento) if rendimento > 0 else None
        return rendimento

    def __str__(self):
        return (
            f"{super().__str__()} | Taxa: {self.taxa_rendimento:.2%} "
            f"| Rendimento previsto: R$ {self.calcular_rendimento():.2f}"
        )

    def __repr__(self):
        return (
            f"ContaPoupanca(titular={self.titular!r}, saldo_inicial={self.saldo!r}, "
            f"taxa_rendimento={self.taxa_rendimento!r})"
        )


def demonstrar_sistema():
    print("=== SISTEMA BANCÁRIO ORIENTADO A OBJETOS ===\n")

    # Criação de 10 clientes e 10 contas (mais de 10 instâncias no total).
    clientes = [
        Cliente("Ana Souza", "ana@email.com"),
        Cliente("Bruno Lima", "bruno@email.com"),
        Cliente("Carla Alves", "carla@email.com"),
        Cliente("Diego Santos", "diego@email.com"),
        Cliente("Eduarda Costa", "eduarda@email.com"),
        Cliente("Felipe Rocha", "felipe@email.com"),
        Cliente("Gabriela Melo", "gabriela@email.com"),
        Cliente("Heitor Nunes", "heitor@email.com"),
        Cliente("Isabela Reis", "isabela@email.com"),
        Cliente("João Martins", "joao@email.com"),
    ]

    contas = [
        ContaCorrente(clientes[0], 1200, 10),
        ContaPoupanca(clientes[1], 2000, 0.01),
        ContaCorrente(clientes[2], 850, 12),
        ContaPoupanca(clientes[3], 1500, 0.008),
        ContaCorrente(clientes[4], 500, 8),
        ContaPoupanca(clientes[5], 3200, 0.012),
        ContaCorrente(clientes[6], 950, 10),
        ContaPoupanca(clientes[7], 700, 0.01),
        ContaCorrente(clientes[8], 1800, 15),
        ContaPoupanca(clientes[9], 2500, 0.009),
    ]

    print("--- Contas cadastradas ---")
    for conta in contas:
        print(conta)

    print("\n--- Demonstração de polimorfismo ---")
    # A mesma chamada produz resultados diferentes conforme a classe concreta.
    for conta in contas:
        print(
            f"{conta.titular.nome}: "
            f"rendimento calculado = R$ {conta.calcular_rendimento():.2f}"
        )

    print("\n--- Operações bancárias ---")
    contas[0].depositar(100)
    contas[0].sacar(50)
    print(f"Saldo após depósito e saque: R$ {contas[0].saldo:.2f}")

    contas[1].aplicar_rendimento()
    print(f"Saldo da poupança após rendimento: R$ {contas[1].saldo:.2f}")

    print("\n--- Ordenação pelo saldo (__lt__) ---")
    for conta in sorted(contas)[:3]:
        print(conta)

    print("\n--- Representação técnica (__repr__) ---")
    print(repr(contas[0]))

    print("\n--- Testes de validação e exceções ---")
    testes_invalidos = [
        ("E-mail inválido", lambda: Cliente("Pessoa", "email-invalido")),
        ("Saldo negativo", lambda: ContaCorrente(clientes[0], -100)),
        ("Depósito negativo", lambda: contas[0].depositar(-10)),
        ("Saque acima do saldo", lambda: contas[0].sacar(999999)),
        ("Taxa inválida", lambda: ContaPoupanca(clientes[0], 100, 1.5)),
    ]

    for descricao, operacao in testes_invalidos:
        try:
            operacao()
        except (ValueError, TypeError) as erro:
            print(f"{descricao}: tratado corretamente — {erro}")

    print("\nDemonstração concluída.")


if __name__ == "__main__":
    demonstrar_sistema()
