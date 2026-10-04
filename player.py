import json
from collections import deque
from queue import PriorityQueue
from datetime import datetime
from mediap.models import Track
from mediap.doubly_linked_list import DoublyLinkedList


def pegar_rating(t):
    return t.rating

def pegar_titulo(t):
    return t.titulo

def pegar_artista(t):
    return t.artista

def pegar_id(t):
    return t.id

class MediaPlayer:
    def __init__(self):
        self.library = {}
        self.playlist = DoublyLinkedList()
        self.playlist_name = ""
        self.up_next = deque()
        self.history = deque(maxlen=20)

    def criar_track(self,dados):
        return Track (
            id = int(dados["id"]),
            titulo = str(dados["titulo"]),
            artista = str(dados["artista"]),
            duracao = int(dados["duracao"]),
            rating= int(dados["rating"]),
            data_adicao=str(dados["data_adicao"])
        )

    def carregar_biblioteca(self, arquivo: str):
        with open(arquivo, 'r') as f:
            dados = json.load(f)
            self.library = {
                item["id"]: self.criar_track(item)
                 for item in dados
            }

    def listar_biblioteca(self, por="id"):
        tracks = list(self.library.values())

        if por == "rating":
            tracks.sort(key=pegar_rating)

        elif por == "title":
            tracks.sort(key=pegar_titulo)

        elif por == "artist":
            tracks.sort(key=pegar_artista)

        else:
            tracks.sort(key=pegar_id)

        return tracks

    def nova_playlist(self, name: str):
        self.playlist = DoublyLinkedList()
        self.playlist_name = name

    def adicionar_musica(self, musica_id: int):
        if musica_id in self.library:
            self.playlist.add(self.library[musica_id])

    def _record_history(self, track: Track):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.appendleft({"track": track, "timestamp": timestamp})

    def play(self):
        curr = self.playlist.current()
        if curr:
            self._record_history(curr)
            return curr
        return None

    def next(self):
        if self.up_next:
            track = self.up_next.popleft()
            self._record_history(track)
            return track
        
        track = self.playlist.play_next()
        self._record_history(track)
        return track

    def prev(self):
        track = self.playlist.play_prev()
        self._record_history(track)
        return track

    def smart_shuffle(self, n: int):
        pq = PriorityQueue()
        hist_list = [item["track"].id for item in self.history]

        for track in self.library.values():
            pos = hist_list.index(track.id) if track.id in hist_list else None
            penalty = (5 - pos) if pos is not None and pos < 5 else 0
            priority = -10 * track.rating + penalty
            pq.put((priority, track.id, track))

        self.nova_playlist("Smart Shuffle")
        count = 0
        while not pq.empty() and count < n:
            _, _, track = pq.get()
            self.playlist.add(track)
            count += 1

    def salvar_estado(self, arquivo: str):
        atual_pos = 0
        if self.playlist.musica_atual:
            atual = self.playlist.inicio
            indice = 1
            while atual:
                if atual == self.playlist.musica_atual:
                    atual_pos = indice
                    break
                atual = atual.next
                indice += 1

        estado = {
            "playlist_name": self.playlist_name,
            "playlist": [
                {
                    "id": t.id,
                    "titulo": t.titulo,
                    "artista": t.artista,
                    "duracao": t.duracao,
                    "rating": t.rating,
                    "data_adicao": t.data_adicao
                } for t in self.playlist
            ],
            "atual_pos": atual_pos,
            "up_next": [
                {
                    "id": t.id,
                    "titulo": t.titulo,
                    "artista": t.artista,
                    "duracao": t.duracao,
                    "rating": t.rating,
                    "data_adicao": t.data_adicao
                } for t in self.up_next
            ],
            "history": [
                {
                    "track": {
                        "id": item["track"].id,
                        "titulo": item["track"].titulo,
                        "artista": item["track"].artista,
                        "duracao": item["track"].duracao,
                        "rating": item["track"].rating,
                        "data_adicao": item["track"].data_adicao
                    },
                    "timestamp": item["timestamp"]
                } for item in self.history
            ]
        }
        with open(arquivo, 'w') as f:
            json.dump(estado, f, indent=2)

    def carregar_estado(self, arquivo: str):
        with open(arquivo, 'r') as f:
            estado = json.load(f)

        self.playlist_name = estado["playlist_name"]
        self.playlist = DoublyLinkedList()
        for dado in estado["playlist"]:
            self.playlist.add(self.criar_track(dado))

        pos = estado["atual_pos"]
        if pos > 0 and self.playlist.inicio:
            atual = self.playlist.inicio
            for _ in range(pos - 1):
                if atual.next:
                    atual = atual.next
            self.playlist.musica_atual = atual

        self.up_next = deque(
            self.criar_track(t) for dado in estado["up_next"]
        )

        self.history = deque(
            [
                {
                    "track": self.criar_track(h["track"]),
                    "timestamp": h["timestamp"]
                } for h in estado["history"]
            ],
            maxlen=20
        )
