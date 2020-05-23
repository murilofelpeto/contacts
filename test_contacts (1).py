from contacts import (Agenda, Contato, CreateContactError, DeleteError,
                    Email, Telefone)


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
    """
    Testes para a classe Email
    """
    def test_01_cria_email(self):
        e1 = Email('teste@exemplo.com')
        msg = 'o email criado não foi salvo na property `email`'
        assert e1.email == 'teste@exemplo.com', msg

    def test_02_cria_email_erro(self):
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
    """
    Testes para a classe Contato
    """
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

    def test_15_buscar_contato(self):
        c1 = Contato('Rafael', '11999777888', 'rafael@exemplo.com')
        msg1 = 'O valor buscado existe no contato, deveria retornar True'
        msg2 = 'O valor buscado não existe no contato, deveria retornar False'
        assert c1.buscar('Rafa'), msg1
        assert c1.buscar('.com'), msg1
        assert c1.buscar('977'), msg1
        assert not c1.buscar('Pedro'), msg2
        assert not c1.buscar('rafael.ribeiro'), msg2
        assert not c1.buscar('456'), msg2

    def test_16_get_telefones(self):
        """
        Este teste não será disponibilizado, faça a verificação com base nas
        instruções do enunciado
        """
        pass

    def test_17_get_emails(self):
        """
        Este teste não será disponibilizado, faça a verificação com base nas
        instruções do enunciado
        """
        pass

    def test_18_lista_telefones(self):
        """
        Este teste não será disponibilizado, faça a verificação com base nas
        instruções do enunciado
        """
        pass

    def test_19_lista_emails(self):
        """
        Este teste não será disponibilizado, faça a verificação com base nas
        instruções do enunciado
        """
        pass


class TestAgenda:
    """
    Testes para a classe Agenda
    """
    def test_20_cria_agenda(self):
        a1 = Agenda('Rafael', '11999887766', 'rafael@email.com')
        assert hasattr(a1, 'meu_contato'), 'Não criou o atributo público corretamente'
        assert isinstance(a1.meu_contato, Contato), (
            'meu_contato deve guardar uma instância de Contato')
        assert hasattr(a1, 'contatos'), 'Não criou o atributo público corretamente'
        assert a1.contatos == [], (
            'atributo contatos deve ser inicializado como uma lista vazia')

    def test_21_adiciona_contato(self):
        a1 = Agenda('Rafael', '11999887766', 'rafael@email.com')
        a1.novo_contato('Ana', '11999888563', 'ana@email.com')
        a1.novo_contato('Pedro', '1955552222', 'pedro@email.com')
        assert len(a1.contatos) == 2, 'A agenda deveria ter 2 contatos'
        assert a1.contatos[0].nome == 'Ana', 'O primeiro contato não está correto'
        assert a1.contatos[1].nome == 'Pedro', 'O segundo contato não está correto'
        a1.novo_contato('Silvia', '21145145145', 'silvia@email.com')
        assert len(a1.contatos) == 3, 'A agenda deveria ter 3 contatos'
        assert a1.contatos[2].nome == 'Silvia', 'O terceiro contato não está correto'

    def test_22_busca_contatos(self):
        a1 = Agenda('Rafael', '11999887766', 'rafael@email.com')
        a1.novo_contato('Ana', '11999888563', 'ana@email.com')
        a1.novo_contato('Pedro', '1955552222', 'pedro@email.com')
        a1.novo_contato('Mariana', '21145145145', 'mariana@email.com')
        a1.novo_contato('João', '1152525252', 'joao@email.com')
        lista01 = a1.busca_contatos('ana')
        lista02 = a1.busca_contatos('9888')
        lista03 = a1.busca_contatos('52')
        lista04 = a1.busca_contatos('email.com')
        assert len(lista01) == 2, 'A busca deveria retornar 2 contatos'
        assert len(lista02) == 1, 'A busca deveria retornar 1 contato'
        assert len(lista03) == 2, 'A busca deveria retornar 2 contatos'
        assert len(lista04) == 4, 'A busca deveria retornar 4 contatos'
        assert lista01[0].nome == 'Ana', 'O contato da lista está incorreto'
        assert lista01[1].nome == 'Mariana', 'O contato da lista está incorreto'
        assert lista02[0].nome == 'Ana', 'O contato da lista está incorreto'
        assert lista03[0].nome == 'Pedro', 'O contato da lista está incorreto'
        assert lista03[1].nome == 'João', 'O contato da lista está incorreto'
        assert lista04[1].nome == 'Pedro', 'O contato da lista está incorreto'
        assert lista04[2].nome == 'Mariana', 'O contato da lista está incorreto'
        assert lista04[3].nome == 'João', 'O contato da lista está incorreto'

    def test_23_ligar_contato(self):
        a1 = Agenda('Rafael', '11999887766', 'rafael@email.com')
        a1.novo_contato('Ana', '11999888563', 'ana@email.com')
        a1.novo_contato('Pedro', '1955552222', 'pedro@email.com')
        a1.novo_contato('Mariana', '21145145145', 'mariana@email.com')
        a1.novo_contato('João', '1152525252', 'joao@email.com')
        a1.contatos[2].adiciona_telefone('45124512', 'casa')
        ligar01 = a1.ligar('ana')
        ligar02 = a1.ligar('9888', 'casa')
        ligar03 = a1.ligar('52')
        ligar04 = a1.ligar('email.com', 'casa')
        resp = [
            'Ligando para Ana: <Telefone: 11999888563>',
            'Nenhum contato possui o tipo de telefone dado!',
            'Ligando para Pedro: <Telefone: 1955552222>',
            'Ligando para Mariana: <Telefone: 45124512>'
        ]
        msg = 'Método ligar não retornou a mensagem correta'
        assert ligar01 == resp[0], msg
        assert ligar02 == resp[1], msg
        assert ligar03 == resp[2], msg
        assert ligar04 == resp[3], msg

    def test_24_exclui_contato(self):
        a1 = Agenda('Rafael', '11999887766', 'rafael@email.com')
        a1.novo_contato('Ana', '11999888563', 'ana@email.com')
        a1.novo_contato('Pedro', '1955552222', 'pedro@email.com')
        a1.novo_contato('Mariana', '21145145145', 'mariana@email.com')
        a1.novo_contato('João', '1152525252', 'joao@email.com')
        a1.contatos[2].adiciona_telefone('45124512', 'casa')
        exclui01 = a1.apagar_contato('rafael@email.com')
        exclui02 = a1.apagar_contato('pedro@email.com')
        exclui03 = a1.apagar_contato('mariana@email.com')
        exclui04 = a1.apagar_contato('joao@email.com')
        resp = [
            'Nenhum contato corresponde ao email dado.',
            '<Contato: Pedro> excluído com sucesso!',
            '<Contato: Mariana> excluído com sucesso!',
            '<Contato: João> excluído com sucesso!'
        ]
        msg = 'Método apagar_contato não retornou a mensagem correta'
        assert exclui01 == resp[0], msg
        assert exclui02 == resp[1], msg
        assert exclui03 == resp[2], msg
        assert exclui04 == resp[3], msg
        assert not len(a1.contatos) > 1, 'Pelo menos um dos contatos não foi removido da lista'
        assert not len(a1.contatos) == 0, 'Apagou mais contatos do que os emails passados'
        assert a1.contatos[0].nome == 'Ana', 'Apagou contatos que não foram pedidos'

    def test_25_exporta_contatos(self):
        """
        Este teste não será disponibilizado, faça a verificação com base nas
        instruções do enunciado e no arquivo de exemplo disponibilizado no
        enunciado da AC5 no Classroom
        """
        a1 = Agenda('Rafael', '11999887766', 'rafael@email.com')
        a1.novo_contato('Ana', '11999888563', 'ana@email.com')
        a1.novo_contato('Pedro', '1955552222', 'pedro@email.com')
        a1.novo_contato('Mariana', '21145145145', 'mariana@email.com')
        a1.novo_contato('João', '1152525252', 'joao@email.com')
        a1.contatos[2].adiciona_telefone('45124512', 'casa')
        a1.exportar_contatos("contatos-teste-1")
        pass
