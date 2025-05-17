from django.db import models

# Modelo de usuário simples, sem autenticação
class Usuario(models.Model):
    # Tipos possíveis de usuário: aluno ou instrutor
    TIPOS = (
        ('aluno', 'Aluno'),
        ('instrutor', 'Instrutor'),
    )

    # Nome do usuário (exibido em listagens e referências)
    nome = models.CharField(max_length=150)

    # Email do usuário (único, pode servir como identificador)
    email = models.EmailField(unique=True)

    # Tipo do usuário, com escolha entre aluno e instrutor
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS)

    def __str__(self):
        # Representação em texto do usuário
        return self.nome


# Modelo de categoria de cursos (ex: Programação, Design)
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Modelo de curso, que pertence a uma categoria e é criado por um instrutor
class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()

    # Instrutor responsável pelo curso (relacionado a um usuário do tipo "instrutor")
    instrutor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'instrutor'}
    )

    # Categoria do curso
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo


# Aula que pertence a um curso, com título e link para o vídeo
class Aula(models.Model):
    titulo = models.CharField(max_length=200)
    video_url = models.URLField()

    # Curso ao qual a aula pertence
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='aulas')

    def __str__(self):
        return self.titulo


# Inscrição de um aluno em um curso
class Inscricao(models.Model):
    # Usuário que fez a inscrição (somente alunos podem se inscrever)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'aluno'}
    )

    # Curso em que o usuário se inscreveu
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    # Data de inscrição, definida automaticamente no momento da criação
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome} - {self.curso.titulo}"


# Progresso de um aluno em relação a uma aula
class Progresso(models.Model):
    # Status possíveis de progresso
    STATUS = (
        ('não concluído', 'Não Concluído'),
        ('em andamento', 'Em Andamento'),
        ('concluído', 'Concluído'),
    )

    # Aluno que está assistindo a aula
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    # Aula assistida
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)

    # Status de progresso do aluno em relação à aula
    status = models.CharField(max_length=15, choices=STATUS, default='não concluído')

    class Meta:
        # Garante que não existam registros duplicados para o mesmo usuário e aula
        unique_together = ('usuario', 'aula')

    def __str__(self):
        return f"{self.usuario.nome} - {self.aula.titulo}: {self.status}"
