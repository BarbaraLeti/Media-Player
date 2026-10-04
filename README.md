# Mini Projeto 1 - Media Player

Projeto desenvolvido para a disciplina de Estrutura de Dados.

## Como executar

No terminal, dentro da pasta do projeto, execute:

py -m mediap

O programa será iniciado no terminal e exibirá o prompt:

mediap>

## Para executar o pytest:

py -m pytest

## Comandos disponíveis

library load library.json - carrega a biblioteca de músicas;

library list - lista as músicas da biblioteca;

library list --by=rating - lista por avaliação;

library list --by=artist - lista por artista;

library list --by=title - lista por título;

playlist new nome - cria uma nova playlist;

playlist add track_id - adiciona uma música à playlist;

playlist remove posição - remove uma música da playlist com base na posição digitada;

playlist show - mostra a playlist;

play - reproduz a música atual;

next - avança para a próxima música;

prev - volta para a música anterior;

enqueue track_id - adiciona uma música à fila Up Next;

queue show - mostra a fila Up Next;

history - mostra o histórico de reprodução;

smart-shuffle <n> - cria uma playlist com as músicas selecionadas pelo Smart Shuffle;

save <arquivo> - salva o estado atual;

load <arquivo> - carrega um estado salvo;

help - mostra os comandos disponíveis;

quit - encerra o programa.

## Exemplo de sessão

mediap> library load library.json

Biblioteca carregada: 10 faixas.

mediap> playlist new Musiquinhas

Playlist "Musiquinhas" criada.

mediap> playlist add 1

mediap> playlist add 3

mediap> playlist show

> 1. Música 1 - Artista 1
  2. Música 3 - Artista 3

mediap> play

>>> Tocando: "Música 1" - Artista 1 (xx:xx)

mediap> enqueue 5

mediap> next

>>> Tocando: "Música 5" - Artista 5 (xx:xx)

mediap> history

1. Música 5 - Artista 5
2. Música 1 - Artista 1

mediap> quit

## Smart Shuffle

Foi utilizada a fórmula de prioridade proposta no enunciado:

chave(f) = -10 * rating(f) + penaltyrec(f)

A PriorityQueue retorna primeiro os menores valores de prioridade.

Primeiro eu crio a PriorityQueue:

pq = PriorityQueue()

Ela vai decidir qual música vem primeiro.

Eu coloco as músicas na fila usando:

pq.put()

E depois retiro o item com menor prioridade usando:

pq.get()
