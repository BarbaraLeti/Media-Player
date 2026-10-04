import pytest
import os
from mediap.models import Track
from mediap.doubly_linked_list import DoublyLinkedList
from mediap.player import MediaPlayer

def test_doubly_linked_list_cursor():
    dll = DoublyLinkedList()
    t1 = Track(1, "Música 1", "Artista 1", 200, 5, "2026-01-01")
    t2 = Track(2, "Música 2", "Artista 2", 180, 4, "2026-01-01")
    
    dll.add(t1)
    dll.add(t2)
    
    assert dll.current().id == 1
    assert dll.play_next().id == 2
    
    with pytest.raises(ValueError):
        dll.play_next()
        
    assert dll.play_prev().id == 1

def test_up_next_precedence():
    player = MediaPlayer()
    t1 = Track(1, "Playlist 1", "Artista", 200, 5, "2026-01-01")
    t2 = Track(2, "Playlist 2", "Artista", 200, 5, "2026-01-01")
    t_queue = Track(3, "Fila 1", "Artista", 200, 5, "2026-01-01")
    
    player.library = {1: t1, 2: t2, 3: t_queue}
    player.new_playlist("Teste")
    player.add_to_playlist(1)
    player.add_to_playlist(2)
    
    player.up_next.append(t_queue)
    
    next_track = player.next()
    assert next_track.id == 3
    assert len(player.up_next) == 0

def test_history_limit():
    player = MediaPlayer()
    for i in range(25):
        t = Track(i, f"Track {i}", "Artista", 100, 5, "2026-01-01")
        player._record_history(t)
    
    assert len(player.history) == 20
    assert player.history[-1]["track"].id == 5

def test_save_load_state(tmp_path):
    player = MediaPlayer()
    t1 = Track(1, "Track 1", "Artista 1", 100, 5, "2026-01-01")
    player.library = {1: t1}
    player.new_playlist("Minha")
    player.add_to_playlist(1)
    
    file_path = tmp_path / "test_state.json"
    player.save_state(str(file_path))
    
    new_player = MediaPlayer()
    new_player.load_state(str(file_path))
    
    assert new_player.playlist_name == "Minha"
    assert len(new_player.playlist) == 1
    assert new_player.playlist.current().titulo == "Track 1"

def test_remove_at():
    dll = DoublyLinkedList()

    t1 = Track(1, "Música 1", "Artista", 200, 5, "2026-01-01")
    t2 = Track(2, "Música 2", "Artista", 180, 4, "2026-01-01")

    dll.add(t1)
    dll.add(t2)

    dll.remove_at(1)

    assert len(dll) == 1
    assert dll.current().id == 2

def test_smart_shuffle():
    player = MediaPlayer()

    player.library = {
        1: Track(1, "Track 1", "Artista", 100, 5, "2026-01-01"),
        2: Track(2, "Track 2", "Artista", 100, 4, "2026-01-01"),
        3: Track(3, "Track 3", "Artista", 100, 3, "2026-01-01")
    }

    player.smart_shuffle(2)

    assert len(player.playlist) == 2
    assert player.playlist.current().id == 1
