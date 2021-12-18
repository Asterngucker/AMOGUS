from loops import *

def main():            # в этой функции происходит инициализация и закрытие игры, а также управление состояниями (циклами) игры.
    game = Game_state()
    while game.state != Game_state.FINISHED:
        assert game.state in [Game_state.MENU, Game_state.SANDBOX, Game_state.SAVES, Game_state.SETTINGS], "emergency situation. Leave the building immediately."
        if   game.state == Game_state.MENU:
            menu_loop(game)
        elif game.state == Game_state.SANDBOX:
            sandbox_loop(game)
        elif game.state == Game_state.SAVES:
            saves_loop(game)
        elif game.state == Game_state.HELP:
            help_loop(game)
        elif game.state == Game_state.SETTINGS:
            settings_loop(game)
    
    game.quit()

if __name__ == "__main__":
    print("This module is for direct call!")
    main()



