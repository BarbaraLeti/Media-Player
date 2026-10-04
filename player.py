import json
from collections import deque
from queue import PriorityQueue
from datetime import datetime
from mediap.models import Track
from mediap.doubly_linked_list import DoublyLinkedList

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

    def load_library(self, filepath: str):
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.library = {
                item["id"]: self.criar_track(item)
                 for item in data
            }

    def list_library(self, by="id"):
        tracks = list(self.library.values())
        if by in ["rating", "title", "artist"]:
            key_map = {"rating": lambda t: t.rating, "title": lambda t: t.titulo, "artist": lambda t: t.artista}
            tracks.sort(key=key_map[by])
        else:
            tracks.sort(key=lambda t: t.id)
        return tracks

    def new_playlist(self, name: str):
        self.playlist = DoublyLinkedList()
        self.playlist_name = name

    def add_to_playlist(self, track_id: int):
        if track_id in self.library:
            self.playlist.add(self.library[track_id])

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

        self.new_playlist("Smart Shuffle")
        count = 0
        while not pq.empty() and count < n:
            _, _, track = pq.get()
            self.playlist.add(track)
            count += 1

    def save_state(self, filepath: str):
        cursor_pos = 0
        if self.playlist.musica_atual:
            curr = self.playlist.inicio
            idx = 1
            while curr:
                if curr == self.playlist.musica_atual:
                    cursor_pos = idx
                    break
                curr = curr.next
                idx += 1

        state = {
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
            "cursor_pos": cursor_pos,
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
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, filepath: str):
        with open(filepath, 'r') as f:
            state = json.load(f)

        self.playlist_name = state["playlist_name"]
        self.playlist = DoublyLinkedList()
        for t_data in state["playlist"]:
            self.playlist.add(self.criar_track(t_data))

        pos = state["cursor_pos"]
        if pos > 0 and self.playlist.inicio:
            curr = self.playlist.inicio
            for _ in range(pos - 1):
                if curr.next:
                    curr = curr.next
            self.playlist.musica_atual = curr

        self.up_next = deque(
            self.criar_track(t) for t_data in state["up_next"]
        )

        self.history = deque(
            [
                {
                    "track": self.criar_track(h["track"]),
                    "timestamp": h["timestamp"]
                } for h in state["history"]
            ],
            maxlen=20
        )
