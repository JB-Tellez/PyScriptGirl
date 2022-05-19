from pyodide.http import pyfetch
import asyncio
import string

# TODO: Render the snake

pyscript = pyscript  # wierd, but gets rid of many linter warnings

url = "https://text-of-fortune.vercel.app/api/tof"
# url = "http://localhost:3000/api/tof"

game_data = None # fetch this data from back end

prompts = {
    "start": "Guess a letter to solve the word",
    "incorrect": "Wrong!!! Guess Again",
    "correct": "Noice! Keep it up",
    "victory": "Congratulations",
    "defeat": "You'll do better next time"
}


async def fetch_game_data(query_string=""):
    global game_data

    # ?id = 1 & guess = f & guesses = xy
    response = await pyfetch(url=url + query_string, method="GET")

    game_data = await response.json()

    id_ = game_data["id"]
    unsolved_word = game_data["working_word"]
    status = game_data["status"]
    guesses = game_data["guesses"]

    prompt = prompts[status]

    incorrect_guesses = ""
    for guess in guesses:
        if guess not in unsolved_word:
            incorrect_guesses += guess

    tries_left = 6 - len(incorrect_guesses)

    incorrect_guesses = incorrect_guesses or "***"

    render_game_info(id_, prompt, unsolved_word, incorrect_guesses, tries_left)

    render_buttons(guesses)


def render_game_info(id_, prompt, unsolved_word, incorrect_guesses, tries_left):
    pyscript.write("game-id", id_)
    pyscript.write("prompt", prompt)
    pyscript.write("unsolved-word", unsolved_word)
    pyscript.write("incorrect-guesses", incorrect_guesses)
    pyscript.write("tries-left", tries_left)


def render_buttons(guesses):
    """
    Go through alphabet and make button for any unused letters
    :param guesses:
    :return:
    """
    alphabet = string.ascii_lowercase

    button_markup = ""

    for char in alphabet:
        if char not in guesses:
            button_markup += f"<button class='px-2'>{char}</button>"

    pyscript.write("letter-buttons", button_markup)


async def clickHandler(event):
    id_ = game_data["id"]
    guess = event.target.textContent # a or b or z
    guesses = game_data["guesses"]

    query_params = f"?id={id_}&guess={guess}&guesses={guesses}"

    await fetch_game_data(query_params)


fetch_game_data()
