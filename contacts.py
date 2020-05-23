# Linguagem de Programação II
# Atividade Contínua 05 - Classes e encapsulamento
#
# e-mails: gilda.costa@aluno.faculdadeimpacta.com.br

from typing import List, Tuple
import json


def dumper(obj):
    """
    Função auxiliar para ser usada no momento de serializar
    os objetos para json.
    - Não deve ser modificada -
    """
    try:
        return obj.to_json()
    except AttributeError:
        return obj.__dict__


class DeleteError(Exception):
    """
    Erro criado para indicar que não foi possível deletar o valor
    ou item pedido. Não é preciso implementar nada nesta classe
    - Não deve ser modificada -
    """
    pass


class CreateContactError(Exception):
    """
    Erro criado para indicar que não foi possível criar o contato.
    Não é preciso implementar nada nesta classe
    - Não deve ser modificada -
    """
    pass


class Telefone:
    """
    Classe para gerar objetos do tipo telefone, responsável por
    realizar a validação do valor recebido.
    - Não deve ser modificada -

    Regras consideradas para os números:
    - ter obrigatoriamente 8 ou 9 dígitos, fixo ou celular, respectivamente;
    - podem vir ou não precedidos de dois dígitos da área (11, 19, 21, etc.)
      levando o número de dígitos para 10 ou 11.
    - podem contér hífens para separar os números (apenas hífens, não espaços)
    Exemplos: '11-995-868-587', '11-4567-4879', '19123456789', '65498754'
    """

    def __init__(self, telefone: str):
        self.telefone = telefone

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, telefone: str) -> None:
        if self.valida_telefone(telefone):
            self._telefone = telefone
            self._numeros = telefone.replace('-', '')
            self._numero_de_digitos = len(self._numeros)

    @staticmethod
    def valida_telefone(telefone: str) -> bool:
        if not isinstance(telefone, str):
            raise TypeError('O telefone deve ser uma string')
        numeros = telefone.replace('-', '')
        if not numeros.isdigit():
            raise ValueError('O telefone pode conter apenas dígitos e hífens')
        if len(numeros) not in [8, 9, 10, 11]:
            raise ValueError('Número incorreto de dígitos para um telefone')
        return True

    @staticmethod
    def digitos(telefone: str) -> str:
        return telefone.replace('-', '')

    @property
    def eh_celular(self) -> bool:
        return len(self.digitos(self.telefone)) in [9, 11]

    @property
    def eh_fixo(self) -> bool:
        return len(self.digitos(self.telefone)) in [8, 10]

    @property
    def possui_ddd(self) -> bool:
        return len(self.digitos(self.telefone)) in [10, 11]

    @property
    def ddd(self) -> str:
        if self.possui_ddd:
            return self.digitos(self.telefone)[:1]
        return ''

    def to_json(self) -> str:
        return self.telefone

    def __repr__(self) -> str:
        return f'<Telefone: {self.telefone}>'


class Email:
    """ (3,5 pontos)
    Classe para representar um Email, responsável por realizar a validação
    do email recebido. As instruções e regras de validação estão descritas
    nos métodos da classe.
    """

    def __init__(self, email: str):
        """
        Construtor de Email - deve usar a property para atribuir o email,
        isto é, deve ser usado o atributo público `self.email`, da mesma
        forma que foi feito no construtor de Telefone.
        """
        self.email = email

    @property
    def email(self) -> str:
        """
        Retorna o endereço de email (o atributo protegido -> apenas um _ )
        """
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        """
        Verifica se o email recebido é válido, usando o método estático
        valida_email() e em caso afirmativo, define o atributo protegido
        para email (apenas um _).
        DICA: Se o email for válido, defina também mais outros dois atributos
              protegidos para guardar o usuario e o dominio do email
        """
        if(self.valida_email(email)):
            emailSplited = email.split("@")
            usuario = emailSplited[0]
            dominio = emailSplited[1]
            self._email = email
            self._usuario = usuario
            self._dominio = dominio

    @staticmethod
    def valida_email(email: str) -> bool:
        """
        Recebe um email e retorna True caso seja válido, levanta um erro
        caso contrário.

        Este método estático é responsável por conter as regras de validação
        de um endereço de email, qualquer objeto da classe pode acessá-lo
        (chamá-lo), mas notem que ele não recebe o self como primeiro
        parâmetro, portanto ele não tem conhecimento sobre o objeto (não
        sabe quais informações o objeto guarda).

        Regras de validação:
        - Deve ser uma string, senão levanta um TypeError
        - Deve conter exatamente 1 símbolo @, senão levanta um ValueError
        - Deve conter apenas letras, números e pontos, senão levanta um
          ValueError.

        DICAS:
        - As mensagens de erro não importam;
        - A validação de caracteres pode ser feita como preferirem,
          uma forma de descobrir se os caracteres são alfanuméricos
          (apenas letras e números) é usar o método de strings isalnum():
              Ex: 'abc123'.isalnum() -> True
                  '#@123'.isalnum() -> False
          Vocês podem quebrar (split) a string no '.' e verificar se cada
          string da lista resultante retorna True para isalnum(), ou
          usar um replace para trocar os pontos por uma string vazia e
          em seguida verificar se isalnum() é True.
          Qualquer outra forma de validação que use apenas módulos da
          biblioteca padrao do python pode ser usada. (Se foi necessário
          fazer um pip install do módulo, então ele não está na biblioteca
          padrão e não será considerado para a nota - eu não irei instalar
          o módulo e isso irá gerar um erro de sintaxe, resultando em nota
          zero. Caso alguém esteja na dúvida, o módulo de regex faz parte
          e pode ser usado se assim desejarem)
        """
        if not isinstance(email, str):
            raise TypeError('O email deve ser uma string')
        
        countAt = email.count("@")
        if(countAt != 1):
            raise ValueError("Email inválido")
        
        emailSplited = email.split("@")
        usuario = emailSplited[0]
        dominio = emailSplited[1]
        usuarioValido = usuario.replace(".", "").isalnum()
        dominioValido = dominio.replace(".", "").isalnum()
        if(usuarioValido and dominioValido):
            return True
        raise ValueError("Email inválido")

    @property
    def eh_aluno_impacta(self) -> bool:
        """
        Retorna True se o dominio completo do email (parte depois do @)
        for igual à 'aluno.faculdadeimpacta.com.br', False caso contrário
        """
        emailSplited = self._email.split("@")
        dominio = emailSplited[1]
        if(dominio == "aluno.faculdadeimpacta.com.br"):
            return True
        return False

    @property
    def eh_impacta(self) -> bool:
        """
        Retorna True se a string 'faculdadeimpacta.com.br' estiver
        contida no dominio do email (parte depois do @), False caso contrário
        """
        emailSplited = self._email.split("@")
        dominio = emailSplited[1]
        if("faculdadeimpacta.com.br" in dominio):
            return True
        return False

    def __eq__(self, other):
        """
        Reescrevendo o método de comparação de igualdade para os objetos de
        email. Este é um método especial do python que será chamado quando
        fizermos a comparação `email1 == email2`. email1 será o self e email2
        será o other. Caso tenhamos uma lista de emails e fizermos a
        verificação de pertencimento `email1 in [e1, e2, e3, e4, ...]`
        o python irá automaticamente percorrer a lista chamando para cada
        elemento dessa lista o método __eq__ de email1 passando os elementos
        da lista como other, isto é:
            email1.__eq__(e1), email1.__eq__(e2), email1.__eq__(e3), ...
        e no primeiro resultado True, ele retorna True. Se chegar ao final da
        lista e não tiver nenhum True, então retorna False.
        """
        if not isinstance(other, Email):
            raise TypeError('Não é possível comparar um email com '
                            'objetos de outro tipo')
        return self.email == other.email

    def to_json(self) -> str:
        """
        Retorna o endereço de email para ser a representação serializada
        de email no arquivo json.
        """
        return self.email

    def __repr__(self) -> str:
        """
        Retorna uma string representando o objeto do tipo email
        Siga o padrão usado para a representação de Telefone
        """
        return f'<Email: {self.email}>'


class Contato:
    """ (4,0 pontos)
    Classe para representar um contato

    Possui os atributos PROTEGIDOS nome, telefones e emails

    Deve receber na criação três strings, uma para cada parâmetro,
    conforme dado no construtor.

    nome:
        se não for uma string, levanta um TypeError, e se
        for uma string vazia, levanta um CreateContactError

    telefones:
        um dicionário iniciado com um par chave-valor,
        chave -> 'principal'; valor -> uma instância de Telefone

    emails:
        um dicionário iniciado com um par chave-valor,
        chave -> 'principal'; valor -> uma instância de Email

    (Deve ser instânciado um objeto de Telefone/Email com o valor recebido
    na string para telefone/email e esse objeto adicionado ao dicionário)
    Ex: {'principal': <instância de Telefone aqui>}
    """

    def __init__(self, nome: str, telefone: str, email: str):
        if(not isinstance(nome, str)):
            raise TypeError("Nome precisa ser uma string")
        if(not nome):
            raise CreateContactError("Nome vazio")

        self._nome = nome
        self._telefones = {'principal' : Telefone(telefone)}
        self._emails = {'principal' : Email(email)}


    @property
    def nome(self) -> str:
        """
        Retorna o valor do atributo protegido nome
        """
        return self._nome

    @nome.setter
    def nome(self, nome: str) -> None:
        """
        Verifica as condições definidas para validação do nome e
        atribui o valor à variável protegida _nome se estiverem OK
        """
        if(not isinstance(nome, str)):
            raise TypeError("Nome precisa ser uma string")
        if(not nome):
            raise CreateContactError("Nome vazio")
        self._nome = nome

    def adiciona_telefone(self, telefone: str, tipo='principal') -> None:
        """
        Atualiza o dicionário com um novo número de telefone, adicionado na chave
        dada em `tipo`. (Notem que o uso de crase ` indica que é a variável e não
        uma string). Da mesma forma que na criação, o telefone deve ser uma instância
        de Telefone.
        Se o tipo não for passado, deve ser por padrão tipo 'principal'.
        """
        self._telefones[tipo] = Telefone(telefone)

    def adiciona_email(self, email: str, tipo='principal') -> None:
        """
        Atualiza o dicionário com um novo endereço de email, adicionado na chave
        dada em `tipo`. (Notem que o uso de crase ` indica que é a variável e não
        uma string). Da mesma forma que na criação, o email deve ser uma instância
        de Email.
        Se o tipo não for passado, por padrão o tipo 'principal' é atualizado.
        """
        self._emails[tipo] = Email(email)

    def apaga_telefone(self, tipo):
        """
        Exclui o telefone dado em `tipo` do dicionário de emails, mas não deve permitir a
        exclusão do tipo 'principal', levantando um DeleteError nesse caso
        """
        if(tipo == "principal"):
            raise DeleteError("Não pode deletar o telefone principal")
        self._telefones.pop(tipo)

    def apaga_email(self, tipo):
        """
        Exclui o email dado em `tipo` do dicionário de emails, mas não deve permitir a
        exclusão do tipo 'principal', levantando um DeleteError nesse caso
        """
        if(tipo == "principal"):
            raise DeleteError("Não pode deletar o email principal")
        self._emails.pop(tipo)

    def get_telefones(self):
        """
        Retorna o dicionário de telefones
        """
        return self._telefones

    def get_emails(self):
        """
        Retorna o dicionário de emails
        """
        return self._emails

    def lista_telefones(self) -> List[Tuple[str, Telefone]]:
        """
        Retorna o dicionário de telefones convertido para uma lista de tuplas,
        cada tupla com um par de valores (chave, valor) referentes às entradas
        do dicionário.
        Ex: [('principal', objeto_telefone01), ('casa', objeto_telefone02)]

        DICA: usem o método items() de dicionários e convertam o resultado
        para uma lista com list().
        """
        listaTelefones = [(k, v) for k, v in self._telefones.items()]
        return listaTelefones

    def lista_emails(self) -> List[Tuple[str, Email]]:
        """
        Retorna o dicionário de emails convertido para uma lista de tuplas,
        cada tupla com um par de valores (chave, valor) referentes às entradas
        do dicionário.
        Ex: [('principal', objeto_email01), ('casa', objeto_email02)]

        DICA: usem o método items() de dicionários e convertam o resultado
        para uma lista com list().
        """
        listaEmails = [(k, v) for k, v in self._emails.items()]
        return listaEmails

    def buscar(self, valor_busca: str):
        """
        Função para determinar se o contato atual (o self) corresponde ao
        valor buscado, retorna True em caso afirmativo e False caso contrário

        Regras para correspondências:
        - o valor buscado está contido no nome do contato
        - o valor buscado está contido em um dos telefones do contato
        - o valor buscado está contido em um dos emails do contato
        Se qualquer uma das condições acima forem verdadeiras, retornar True.
        Caso contrário, retornar False.
        Ex: Uma busca por Ana deve retornar os contatos que tenham Ana em
            qualquer lugar: 'Ana Julia', 'Mariana', 'marcos@bananas.com.br'
            E uma busca por '345' deve retornar todos os contatos que tenham
            '345' em qualquer lugar: '11999888345', 'João do 345',
            'joao345@exemplo.com'
        """
        achouNome = valor_busca in self._nome
        achouTelefone = False
        achouEmail = False
        for value in self._telefones.values():
            if(valor_busca in value.telefone):
                achouTelefone = True

        for value in self._emails.values():
            if(valor_busca in value.email):
                achouEmail = True

        if(achouNome or achouEmail or achouTelefone):
            return True
        return False

    def create_dump(self):
        """
        Retorna um dicionário com os dados do contato:
        Pares chave-valor:
        'nome': nome do contato,
        'telefones': dicionário de telefones do contato
        'emails': dicionário de emails do contato.
        """
        contatos = dict()
        contatos["nome"] = self._nome
        contatos["telefones"] = self._telefones
        contatos["emails"] = self._emails
        return contatos

    def __repr__(self):
        """
        Representação de um contato, use o padrão:
        '<Contato: nome-do-contato-aqui>'
        """
        return f'<Contato: {self._nome}>'


class Agenda:
    """ (3,5 pontos)
    No mometo de criação, a agenda recebe um titular (nome), um número de
    telefone e um email do titular, criando um atributo público
    meu_contato que irá guardar uma instância de contato criada com os
    dados do titular.
    O construtor deve ainda criar um atributo público contatos, que deverá
    ser inicializado como uma lista vazia.
    """

    def __init__(self, titular: str, meu_numero: str, meu_email: str):
        self.meu_contato = Contato(titular, meu_numero, meu_email)
        self.contatos = list()

    def novo_contato(self, nome: str, telefone: str, email: str) -> None:
        """
        Insere um novo contato na agenda, adicionando-o à lista de contatos.
        """
        contato = Contato(nome, telefone, email)
        self.contatos.append(contato)

    def busca_contatos(self, valor_busca) -> List[Contato]:
        """
        Retorna uma lista com todos os contatos que correspondam ao valor
        buscado. Se nenhum contato for encontrado, retorna uma lista vazia

        DICA: Itere sobre a lista de contatos e use o método de
        correspondência (buscar) de cada contato para ver se ele deve ou não
        ser adicionado à lista
        """
        contatosEncontrados = list()
        for contato in self.contatos:
            if(contato.buscar(valor_busca)):
                contatosEncontrados.append(contato)
        return contatosEncontrados

    def ligar(self, valor_busca, tipo='principal') -> None:
        """
        Busca a lista de contato que correspondam ao valor buscado e liga
        para o primeiro contato da lista que possuir o telefone do tipo dado
        retornando uma string com a mensagem:
        'Ligando para <nome_contato>: <telefone>'
        Se nenhum contato da lista possuir o tipo dado, retorna a mensagem:
        'Nenhum contato possui o tipo de telefone dado!'

        DICA: Percorram a lista retornada pelo método de buscar contatos
        e para cada contato dessa lista, percorram a lista de telefones
        do contato verificando se o primeiro valor da tupla é igual ao tipo
        dado. Se sim, o telefone a ser chamado é o segundo valor da tupla.
        """
        mensagem = "Ligando para "
        contatos = self.busca_contatos(valor_busca)
        for contato in contatos:            
            telefones = contato.get_telefones()
            emails = contato.get_emails()

            if(valor_busca in contato._nome):
                mensagem = mensagem + contato._nome + ": " + telefones.get(tipo).__repr__()
                return mensagem

            if(tipo in telefones):
                if(valor_busca in telefones.get(tipo)._telefone):
                    mensagem = mensagem + contato._nome + ": " + telefones.get(tipo).__repr__()
                    return mensagem

                if(valor_busca in email._email for email in emails.values()):
                    mensagem = mensagem + contato._nome + ": " + telefones.get(tipo).__repr__()
                    return mensagem

            if(tipo in emails):
                if(valor_busca in emails.get(tipo)._email):
                    mensagem = mensagem + contato._nome + ": " + telefones.get(tipo).__repr__()
                    return mensagem
                
                if(valor_busca in telefone._telefone for telefone in telefones.values()):
                    mensagem = mensagem + contato._nome + ": " + telefones.get(tipo).__repr__()
                    return mensagem


        return "Nenhum contato possui o tipo de telefone dado!"
            

    def apagar_contato(self, email_busca) -> str:
        """
        Busca um contato por email e exclui o contato da agenda.
        retornando a mensagem:
        '<representação do contato> excluído com sucesso!'
        Ex: '<Contato: João do 345> excluído com sucesso!'

        Se nenhum contato for encontrado, retorna a mensagem:
        'Nenhum contato corresponde ao email dado.'
        """
        for contato in self.contatos:
            emails = contato.get_emails()
            for email in emails.values():
                if(email_busca == email.email):
                    self.contatos.remove(contato)
                    return contato.__repr__() + " excluído com sucesso!"
        
        return "Nenhum contato corresponde ao email dado."

    def exportar_contatos(self, nome_arquivo: str) -> None:
        """
        Exporta um arquivo json com a agenda de contatos.
        Verificar se o nome do arquivo termina em '.json'.
        Em caso afirmativo, deve ser usadado como dado para criação
        do arquivo. Caso o nome do arquivo não termine em '.json',
        a extensão deve ser adicionada ao nome para criação do arquivo
        em disco, garantindo que será sempre escrito um arquivo json.

        DICAS:
            - Crie uma nova lista vazia e percorra a lista de contatos
              adicionando à nova lista o dicionário retornado pelo método
              create_dump para cada contato da lista de contatos.
            - Usem o gerenciador de contexto --> with
            - Os objetos de Telefone e Email não são serializáveis,
              por isso criei o método to_json() e a função dumper.
              Então passe a função dumper por parâmetro nomeado para o
              parâmetro `default` do método dump() de json.
            - Para deixar o arquivo json mais legível por humanos, passe
              como parâmetro nomeado `indent` um valor inteiro positivo.
              Valores comuns são 2 ou 4.
        """
        if(not nome_arquivo.endswith(".json")):
            nome_arquivo = nome_arquivo + ".json"

        contatos = list()
        for contato in self.contatos:
            contatos.append(contato.create_dump())
        json_data = json.dumps(contatos, default=lambda objeto: objeto.to_json(), indent=2)
        file = open(nome_arquivo, "w")
        file.write(json_data)
        file.close()


        

    def carregar_contatos(self, nome_arquivo: str) -> None:
        """
        Método bônus - não será considerado para a correção
        Ler um arquivo json exportado pelo método anterior e
        carregar os contatos na agenda.
        """
        pass
