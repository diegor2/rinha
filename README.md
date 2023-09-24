# Interpretador [rinha](https://github.com/aripiprazole/rinha-de-compiler) em [RPython](https://rpython.readthedocs.io/)

## FAQ (Perguntas & Respostas)

### O que é rinha?

É a linguagem criada para [rinha de compiler](https://github.com/aripiprazole/rinha-de-compiler)

### Mas isso não é um compilador!

A rinha também aceita interpretadores. O objetivo inicial era fazer um interpretador com compilador JIT.

### O que é RPython?

É um subconjunto da linguagem Python que permite inferencia estática de tipos.
É também  o framework usado para desenvolver interpretadores como o pypy.

### O que é pypy?

É um interpretador JIT para Python, escrito em Python (ou mais especificamente, RPython).
Isso faz com que o pypy seja tecnicamente uma versão [self-hosted](https://pt.wikipedia.org/wiki/Auto-hospedagem) do Python

### Por que RPython?

Permite que o interpretador seja escrito em python e compilado para código nativo.
RPython também permite criar interpretadores com JIT.
Devido ao prazo, a implemetação atual do interpretador rinha não inclui JIT.

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

### Para rodar os testes unitarios no docker

```sh
make docker-test
```

### Para rodar os testes no cpython ou pypy 2.7 sem compilar e sem container

```sh
make test
```

### Para rodar o interpretador no cpython ou pypy 2.7 sem compilar
```sh
./treta <arquivo.rinha>
```

### Para compilar o interpretador sem container

```sh
make rinha
```

### Para usar o compilador gerado

```sh
./rinha <arquivo.rinha>
```
