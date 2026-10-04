from mediap.player import MediaPlayer

def fmt_time(segundos_totais: int) -> str:
    m = segundos_totais // 60
    s = segundos_totais % 60
    return f"{m:02d}:{s:02d}"

def run():
    player = MediaPlayer()
    while True:
        try:
            cmd = input("mediap> ").strip().split()
            if not cmd:
                continue

            action = cmd[0]

            if action == "library":
                if cmd[1] == "load":
                    player.load_library(cmd[2])
                    print(f"Biblioteca carregada: {len(player.library)} faixas.")
                elif cmd[1] == "list":
                    by = cmd[2].replace("--by=", "") if len(cmd) > 2 else "id"
                    for t in player.list_library(by):
                        print(f"{t.id}. {t.titulo} - {t.artista} ({fmt_time(t.duracao)}) [{t.rating}★]")

            elif action == "playlist":
                sub = cmd[1]
                if sub == "new":
                    player.new_playlist(cmd[2])
                    print(f'Playlist "{cmd[2]}" criada.')
                elif sub == "add":
                    player.add_to_playlist(int(cmd[2]))
                elif sub == "remove":
                    player.playlist.remove_at(int(cmd[2]))
                elif sub == "show":
                    for i, track in enumerate(player.playlist, 1):
                        cursor_mark = "> " if player.playlist.musica_atual and player.playlist.musica_atual.value.id == track.id else "  "
                        print(f"{cursor_mark}{i}. {track.titulo} {track.artista} ({fmt_time(track.duracao)})")
            elif action in ["play", "next", "prev"]:
                func = getattr(player, action)
                track = func()
                print(f'>>> Tocando: "{track.titulo}" {track.artista} ({fmt_time(track.duracao)})')

            elif action == "enqueue":
                t = player.library[int(cmd[1])]
                player.up_next.append(t)

            elif action == "queue" and cmd[1] == "show":
                for i, t in enumerate(player.up_next, 1):
                    print(f"{i}. {t.titulo} - {t.artista}")

            elif action == "history":
                for i, item in enumerate(player.history, 1):
                    t = item["track"]
                    print(f"{i}. {t.titulo} {t.artista} [{item['timestamp']}]")

            elif action == "smart-shuffle":
                player.smart_shuffle(int(cmd[1]))

            elif action == "save":
                player.save_state(cmd[1])

            elif action == "load":
                player.load_state(cmd[1])

            elif action == "help":
                print("Comandos: library load/list, playlist new/add/remove/show, play, next, prev, enqueue, queue show, history, smart-shuffle, save, load, quit")

            elif action == "quit":
                break

        except Exception as e:
            print(f"Erro: {e}")
