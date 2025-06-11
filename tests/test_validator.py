import pytest
from utils.validator import Validator
# NOME
def test_nome_valido():
    assert Validator.validate_nome("Ramon Miguel") is True

def test_nome_invalido():
    assert Validator.validate_nome("Raamon1234") is False
# CPF
def test_cpf_valido():
    assert Validator.validate_cpf("123.123.123-05") is False
# IDADE
def test_idade_maior_invalido():
    assert Validator.validate_idade("06/04/2006") is False

def test_idade_menor_invalido():
    assert Validator.validate_idade("2008") is False

def test_idade_maior_valido():
    assert Validator.validate_idade("2006") is True
# EMAIL
def test_email_valido():
    assert Validator.validate_email("ramonmiguel717@gmail.com") is True

def test_email_invalido():
    assert Validator.validate_email("ramon@") is False