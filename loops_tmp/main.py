from loops import *

def main():            # в этой функции происходит инициализация и закрытие игры, а также управление состояниями (циклами) игры.
    game = Game_state()
    menu_loop(game, Game_state.FINISHED)
    game.quit()

if __name__ == "__main__":
    print("This module is for direct call!")
    main()



