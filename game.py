import subprocess
import time
from dash import Dash, Output, Input, ALL, ctx
import dash_mantine_components as dmc

app = Dash(__name__)

app.layout = dmc.MantineProvider(

    dmc.Container([
        
        dmc.Anchor(
            "Click on Link to get instructions on playing each games",
            href="https://pypi.org/project/freegames/",
        ),

        dmc.Title(
            "FreeGames Launcher",
            order=1,
            mb="lg"
        ),

        dmc.Button(
            "Show All Games",
            id="run-btn",
            size="md",
            radius="md",
            mb="lg"
        ),

        dmc.Stack(
            id="result",
            gap="sm"
        ),

        dmc.Alert(
            id="game-output",
            title="Status",
            children="No game launched yet",
            color="blue",
            mt="xl"
        )



    ], size="sm", py="xl")

)


# Load games and generate buttons
@app.callback(
    Output("result", "children"),
    Input("run-btn", "n_clicks"),
    prevent_initial_call=True
)
def show_games(n):


    result = subprocess.run(
        ["python", "-m", "freegames", "list"],
        capture_output=True,
        text=True
    )

    games = result.stdout.strip().splitlines()

    return [

        dmc.Button(
            game,

            id={
                "type": "game-btn",
                "name": game
            },

            variant="light",
            radius="md",
            fullWidth=True,
            n_clicks=0

        )

        for game in games
    ]


# Launch selected game
@app.callback(
    Output("game-output", "children"),
    Input({"type": "game-btn", "name": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def launch_game(n_clicks):
    if not any(n_clicks):
        return "No game selected"

    clicked = ctx.triggered_id

    if not clicked:
        return "No game selected"

    game_name = clicked["name"]
    subprocess.Popen(
        ["python", "-m", f"freegames.{game_name}"],
        start_new_session=True
    )

    return f"Launching {game_name} 🎮 and Showing Score At the Terminal"


if __name__ == "__main__":
    app.run(debug=True)