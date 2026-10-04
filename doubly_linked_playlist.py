class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.inicio = None
        self.final = None
        self.musica_atual = None
        self._size = 0

    def add(self, track):
        new_node = Node(track)
        if not self.inicio:
            self.inicio = new_node
            self.final = new_node
            self.musica_atual = new_node
        else:
            new_node.prev = self.final  
            self.final.next = new_node
            self.final = new_node
        self._size += 1

    def remove_at(self, pos: int):
        if pos < 1 or pos > self._size:
            raise IndexError("Posição inválida.")

        atual = self.inicio
        for _ in range(pos - 1):
            atual = atual.next

        if atual == self.musica_atual:
            self.musica_atual = atual.next if atual.next else atual.prev

        if atual.prev:
            atual.prev.next = atual.next
        else:
            self.inicio = atual.next

        if atual.next:
            atual.next.prev = atual.prev
        else:
            self.final = atual.prev

        self._size -= 1
        return atual.value

    def current(self):
        return self.musica_atual.value if self.musica_atual else None

    def play_next(self):
        if not self.musica_atual or not self.musica_atual.next:
            raise ValueError("Fim da playlist atingido.")
        self.musica_atual = self.musica_atual.next
        return self.musica_atual.value

    def play_prev(self):
        if not self.musica_atual or not self.musica_atual.prev:
            raise ValueError("Início da playlist atingido.")
        self.musica_atual = self.musica_atual.prev
        return self.musica_atual.value

    def reset_musica_atual(self):
        self.musica_atual = self.inicio

    def __len__(self):
        return self._size

    def __iter__(self):
        atual = self.inicio
        while atual:
            yield atual.value
            atual = atual.next
