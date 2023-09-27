# Interpretador [rinha](https://github.com/aripiprazole/rinha-de-compiler) em Python

## FAQ (Perguntas & Respostas)

### O que é rinha?

É a linguagem criada para [rinha de compiler](https://github.com/aripiprazole/rinha-de-compiler)

### Mas isso não é um compilador!

A rinha também aceita interpretadores. Meu objetivo inicial neste projeto era fazer um interpretador com compilador JIT em [RPython](https://rpython.readthedocs.io/).

### Por que Python?

A dificuldade de usar RPython foi bem maior do que esperado, já que não tinha nenhuma experiência com este framework. Como descobri a rinha há poucos dias do prazo final, tive que abrir mão de implementar o JIT. Como ainda haviam problemas com RPython, a versão final está usando o interpretador python comum.

### O que é RPython?

É um subconjunto da linguagem Python que permite inferencia estática de tipos.
É também  o framework usado para desenvolver interpretadores como o pypy.

### O que é pypy?

É um interpretador JIT para Python, escrito em Python (ou mais especificamente, RPython).
Isso faz com que o pypy seja tecnicamente uma versão [self-hosted](https://pt.wikipedia.org/wiki/Auto-hospedagem) do Python

### Qual o status do projeto?

O desenvolvimento da versão compilada continua no branch `rpython`. 

## Utilização

### Para gerar a imagem docker

```sh
docker build .
```
ou

```sh
make image
```

### Para rodar num container docker

```sh
make container
```

### Para rodar os testes no python do host

```sh
make test
```

### Para compilar o interpretador no host

```sh
make rinha
```

### Para usar o compilador gerado

```sh
./rinha <arquivo.rinha>
```

Todos os comandos no host exigem um ambiente com Python 2.7
