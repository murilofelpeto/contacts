from contacts import (Contato, CreateContactError, DeleteError,
                    Email, Telefone, Agenda)


class TelefoneAtualizado(Telefone):
    """
    Eu esqueci de incluir este método na classe de Telefone, então
    estou criando esta classe para poder adicionar o método à classe Telefone
    sem que vocês precisem editar o código de vocês. Basta usar a nova classe
    que criei durantes os testes, como fiz.

    Portanto NÃO INCLUAM este método na classe Telefone de vocês.
    """

    def __eq__(self, other):
        if not isinstance(other, Telefone):
            raise TypeError('Não é possível comparar um Telefone com '
                            'objetos de outro tipo')
        n_self = self.telefone.replace('-', '')
        n_other = other.telefone.replace('-', '')
        return n_self == n_other


class TestEmail:
    def test_01_cria_email(self):
        e1 = Email('teste@exemplo.com')
        msg = 'o email criado não foi salvo na property `email`'
        assert e1.email == 'teste@exemplo.com', msg

    def test_02_cria_email_erro1(self):
        tipos_errados = [1, True, 3.0, None,
                         ('email', 'email@exemplo.com'),
                         {'email': 'nome@teste.com'}]
        for item in tipos_errados:
            try:
                Email(item)
            except TypeError:
                pass
            except Exception:
                raise AssertionError('Levantou um erro de tipo diferente do pedido')
            else:
                raise AssertionError('Não levantou erro para email inválido')

        try:
            Email('teste_erro@exemplo.com')
        except ValueError:
            pass
        except Exception:
            raise AssertionError('Levantou um erro de tipo diferente do pedido')
        else:
            raise AssertionError('Email com _ não deveria ser válido')

        try:
            Email('teste@exemplo@com')
        except ValueError:
            pass
        except Exception:
            raise AssertionError('Levantou um erro de tipo diferente do pedido')
        else:
            raise AssertionError('Email com 2 @ não deveria ser válido')

        try:
            Email('teste.exemplo.com')
        except ValueError:
            pass
        except Exception:
            raise AssertionError('Levantou um erro de tipo diferente do pedido')
        else:
            raise AssertionError('Email sem @ não deveria ser válido')

    def test_03_email_aluno(self):
        e1 = Email('teste@aluno.faculdadeimpacta.com.br')
        msg = 'o email criado deveria retornar True para a property eh_aluno_impacta'
        assert e1.eh_aluno_impacta, msg

    def test_04_email_aluno_erro(self):
        e1 = Email('teste@dominioincorreto.aluno.faculdadeimpacta.com.br')
        msg = 'o email criado deveria retornar False para a property eh_aluno_impacta'
        assert not e1.eh_aluno_impacta, msg

    def test_05_email_funcionario(self):
        e1 = Email('teste@aluno.faculdadeimpacta.com.br')
        e2 = Email('teste@coordenacao.faculdadeimpacta.com.br')
        e3 = Email('teste@faculdadeimpacta.com.br')
        msg = 'todos os emails criados deveriam retornar True para a property eh_impacta'
        assert all([e.eh_impacta for e in [e1, e2, e3]]), msg

    def test_06_email_funcionario_erro(self):
        e1 = Email('teste@aluno.faculdade.com.br')
        e2 = Email('teste@impacta.com.br')
        e3 = Email('teste@faculdadeimpacta.com')
        e4 = Email('teste@faculdadeimpacta.edu.br')
        msg = 'todos os emails criados deveriam retornar False para a property eh_impacta'
        assert not any([e.eh_impacta for e in [e1, e2, e3, e4]]), msg


class TestContato:
    def test_07_cria_contato(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        assert c1.nome == 'Rafael', 'O nome foi criado incorretamente'
        assert isinstance(c1.get_telefones()['principal'], Telefone), (
            'Objeto adicionado ao dicionário de telefones não é do tipo Telefone')
        assert c1.get_telefones()['principal'] == TelefoneAtualizado('11999777888'), (
            'o telefone não foi salvo com o valor correto no dicionário')
        assert isinstance(c1.get_emails()['principal'], Email), (
            'Objeto adicionado ao dicionário de emails não é do tipo Email')
        assert c1.get_emails()['principal'] == Email('rafael@exemplo.com'), (
            'o email não foi salvo com o valor correto no dicionário')

    def test_08_cria_contato_erro(self):
        try:
            Contato('', '11999777888', 'rafael@exemplo.com')
        except CreateContactError:
            pass
        except Exception:
            raise AssertionError('Levantou um erro do tipo incorreto')
        else:
            raise AssertionError('Não deveria criar um contato com nome vazio')

        tipos_errados = [1, True, 3.0, None, ('nome', 'Rafael'), {'nome': 'Rafael'}]
        for item in tipos_errados:
            try:
                Contato(item, '11999777888', 'rafael@exemplo.com')
            except TypeError:
                pass
            except Exception:
                raise AssertionError('Levantou um erro do tipo incorreto')
            else:
                raise AssertionError('Não deveria criar um contato sem nome')

    def test_09_adiciona_telefone(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        c1.adiciona_telefone('11987654321', 'trabalho')
        telefones = c1.get_telefones()
        assert telefones['principal'] == TelefoneAtualizado('11999777888'), (
            'o telefone não foi salvo com o valor correto no dicionário')
        assert telefones['trabalho'] == TelefoneAtualizado('11987654321'), (
            'o telefone não foi salvo com o valor ou a chave correta no dicionário')
        c1.adiciona_telefone('1144556677', 'casa')
        c1.adiciona_telefone('11-999-555-111')
        assert telefones['casa'] == TelefoneAtualizado('1144556677'), (
            'o telefone não foi salvo com o valor ou a chave correta no dicionário')
        assert telefones['principal'] == TelefoneAtualizado('11999555111'), (
            'o telefone principal não foi atualizado no dicionário')

    def test_10_apaga_telefone(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        c1.adiciona_telefone('11987654321', 'trabalho')
        telefones = c1.get_telefones()
        assert telefones['principal'] == TelefoneAtualizado('11999777888'), (
            'o telefone não foi salvo com o valor correto no dicionário')
        assert telefones['trabalho'] == TelefoneAtualizado('11987654321'), (
            'o telefone não foi salvo com o valor ou a chave correta no dicionário')
        c1.apaga_telefone('trabalho')
        telefones = c1.get_telefones()
        assert 'trabalho' not in telefones, 'o telefone de trabalho não foi apagado do dicionário'
        assert 'principal' in telefones, (
            'o telefone principal não deveria ter sido apagado do dicionário')

    def test_11_apaga_telefone_principal(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        try:
            c1.apaga_telefone('principal')
        except DeleteError:
            pass
        except Exception:
            raise AssertionError('Levantou o tipo de erro incorreto')
        else:
            raise AssertionError('Não levantou erro ao tentar apagar o telefone principal')

    def test_12_adiciona_email(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        c1.adiciona_email('rafael@empresa.com', 'trabalho')
        emails = c1.get_emails()
        assert emails['principal'] == Email('rafael@exemplo.com'), (
            'o email não foi salvo com o valor correto no dicionário')
        assert emails['trabalho'] == Email('rafael@empresa.com'), (
            'o email não foi salvo com o valor ou a chave correta no dicionário')
        c1.adiciona_email('naruto27@rasenshuriken.com', 'jogos')
        c1.adiciona_email('rafael@novoemail.com')
        assert emails['jogos'] == Email('naruto27@rasenshuriken.com'), (
            'o email não foi salvo com o valor ou a chave correta no dicionário')
        assert emails['principal'] == Email('rafael@novoemail.com'), (
            'o email principal não foi atualizado no dicionário')

    def test_13_apaga_email(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        c1.adiciona_email('rafael@empresa.com', 'trabalho')
        emails = c1.get_emails()
        assert emails['principal'] == Email('rafael@exemplo.com'), (
            'o email não foi salvo com o valor correto no dicionário')
        assert emails['trabalho'] == Email('rafael@empresa.com'), (
            'o email não foi salvo com o valor ou a chave correta no dicionário')
        c1.apaga_email('trabalho')
        emails = c1.get_emails()
        assert 'trabalho' not in emails, 'o email de trabalho não foi apagado do dicionário'
        assert 'principal' in emails, (
            'o email principal não deveria ter sido apagado do dicionário')

    def test_14_apaga_email_principal(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        try:
            c1.apaga_email('principal')
        except DeleteError:
            pass
        except Exception:
            raise AssertionError('Levantou o tipo de erro incorreto')
        else:
            raise AssertionError('Não levantou erro ao tentar apagar o email principal')

    def test_15_exporta_contato(self):
        agenda = Agenda("Murilo", "11222333444", "murilo@teste.com.br")
        agenda.novo_contato('Rafael', '11999777888', 'rafael@exemplo.com')
        agenda.novo_contato('Roberto', '61555666777', 'roberto@exemplo.com')
        agenda.exportar_contatos("contatos-teste")
