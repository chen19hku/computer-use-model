"""
Automated IMDb ID retrieval using CUA agent and computer-use model.
Reads movie titles from video_list.csv, uses CUA agent to search IMDb, and saves results.
"""
import asyncio
import csv
import os
import re

import cua
import local_computer
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def get_imdb_id(agent, title, max_steps=15):
    instructions = f"Open Chrome web browser, go to imdb.com, search for {title}, and find its imdb movie id."
    agent.start_task()
    user_input = instructions
    pattern = r"tt\d{7,8}"  # IMDb IDs look like 'tt1234567'
    imdb_id = None
    step = 0
    while step < max_steps and not imdb_id:
        await agent.continue_task(user_input)
        user_input = ""  # Only send instructions on first step
        # Log agent actions and messages for debugging
        if agent.reasoning_summary:
            print(f"Reasoning: {agent.reasoning_summary}")
        for action, action_args in agent.actions:
            print(f"Action: {action} {action_args}")
        for msg in agent.messages:
            print(f"Agent message: {msg}")
            match = re.search(pattern, msg)
            if match:
                imdb_id = match.group(0)
                break
        step += 1
    return imdb_id

async def main():
    # Setup agent (similar to main.py)
    client = openai.AsyncAzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2025-03-01-preview",
    )
    model = "computer-use-preview"
    computer = local_computer.LocalComputer()
    computer = cua.Scaler(computer, (1024, 768))
    agent = cua.Agent(client, model, computer)

    # Read input CSV
    input_path = "video_list.csv"
    output_path = "imdb_cua_results.csv"
    results = []
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vidlink = row.get('vidlink', '')
            title = row.get('title', '')
            print(f"Processing: {title}")
            imdb_id = await get_imdb_id(agent, title)
            print(f"IMDb ID for '{title}': {imdb_id}")
            results.append({'vidlink': vidlink, 'title': title, 'imdb_id': imdb_id or ''})

    # Write output CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['vidlink', 'title', 'imdb_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(main())

# Prompt for GitHub Copilot Agent
# Round 1: write a new program imdb_cua.py based imdb.py but instead of using selenium and human input leverage main.py program's computer use to go to imdb.com and search for movie title and retrieve the imdb id.
# Round 2: It seems that CUA is not activated: Processing: #Realityhigh (2017) IMDb ID for '#Realityhigh (2017)': None Processing: <span>5 a Day (2010) IMDb ID for '</span>5 a Day (2010)': None Processing: (500) Days of Summer (2009) IMDb ID for '(500) Days of Summer (2009)': None Processing: Zootopia (2016) IMDb ID for 'Zootopia (2016)': None Processing: Hush (2016) IMDb ID for 'Hush (2016)': None

# 200 requests, 4k tokens per request, 35 tokens per response, 0.8 Million input tokens, 7k output tokens, US$2.5 cost
"""
Processing: #Realityhigh (2017)
Action: screenshot {}
Reasoning: Opening browser, navigating to IMDb
Action: click {'button': 'left', 'x': 189, 'y': 563}
Reasoning: Searching IMDB for #Realityhigh movie
Action: click {'button': 'left', 'x': 375, 'y': 70}
Action: type {'text': '#Realityhigh (2017)'}
Action: keypress {'keys': ['ENTER']}
Reasoning: Selecting #Realityhigh movie page
Action: click {'button': 'left', 'x': 344, 'y': 98}
Reasoning: Opening #Realityhigh page for details
Action: click {'button': 'left', 'x': 214, 'y': 251}
Action: wait {}
Reasoning: Retrieving IMDb ID for Realityhigh
Agent message: The IMDb ID for "#Realityhigh" (2017) is tt6119504.
IMDb ID for '#Realityhigh (2017)': tt6119504
Processing: $5 a Day (2010)
Action: screenshot {}
Reasoning: Searching IMDb for "$5 a Day"
Action: click {'button': 'left', 'x': 985, 'y': 69}
Reasoning: Clicking search bar for "$5 a Day"
Action: click {'button': 'left', 'x': 312, 'y': 66}
Action: type {'text': '$5 a Day (2010)'}
Action: click {'button': 'left', 'x': 653, 'y': 69}
Reasoning: Refining search for "$5 a Day"
Action: click {'button': 'left', 'x': 300, 'y': 67}
Reasoning: Refining search for $5 a Day
Action: click {'button': 'left', 'x': 310, 'y': 67}
Action: type {'text': '$5 a Day'}
Action: keypress {'keys': ['ENTER']}
Reasoning: Reviewing search results for relevance
Action: click {'button': 'left', 'x': 321, 'y': 537}
Reasoning: Scrolling for more search results
Action: click {'button': 'left', 'x': 257, 'y': 499}
Action: wait {}
Reasoning: Selecting closest match, gathering information
Action: click {'button': 'left', 'x': 201, 'y': 253}
Action: wait {}
Reasoning: Confirming film details with user
Agent message: I found a movie titled "$5 a Day" on IMDb that was released in 2008. Its IMDb movie ID is "tt1024773." Since the year is different from what you initially mentioned, could you confirm if this is the film you were looking for, or would you like me to refine the search?
IMDb ID for '$5 a Day (2010)': tt1024773
Processing: (500) Days of Summer (2009)
Action: screenshot {}
Reasoning: Accessing IMDb, searching for movie
Action: click {'button': 'left', 'x': 635, 'y': 70}
Action: type {'text': '(500) Days of Summer (2009)'}
Action: click {'button': 'left', 'x': 657, 'y': 69}
Action: wait {}
Reasoning: Selecting result for movie ID
Action: click {'button': 'left', 'x': 225, 'y': 279}
Action: wait {}
Reasoning: Identifying IMDb ID for movie
Agent message: The IMDb movie ID for "(500) Days of Summer" (2009) is "tt1022603."
IMDb ID for '(500) Days of Summer (2009)': tt1022603
Processing: Zootopia (2016)
Action: screenshot {}
Reasoning: Using search bar for Zootopia
Action: click {'button': 'left', 'x': 467, 'y': 67}
Action: type {'text': 'Zootopia'}
Action: keypress {'keys': ['ENTER']}
Action: wait {}
Reasoning: Selecting Zootropolis for IMDb ID
Action: click {'button': 'left', 'x': 219, 'y': 253}
Action: wait {}
Reasoning: Checking URL for IMDb ID
Action: click {'button': 'left', 'x': 172, 'y': 37}
Reasoning: Sharing IMDb ID for Zootropolis
Agent message: I found the IMDb ID for the movie "Zootopia (2016)." It's "tt2948356."
IMDb ID for 'Zootopia (2016)': tt2948356
Processing: Hush (2016)
Action: screenshot {}
Reasoning: Searching IMDB for "Hush (2016)"
Action: click {'button': 'left', 'x': 451, 'y': 66}
Reasoning: Retrying to activate search field
Action: click {'button': 'left', 'x': 446, 'y': 67}
Action: type {'text': 'Hush (2016)'}
Action: wait {}
Reasoning: Selecting relevant "Hush" movie entry
Action: click {'button': 'left', 'x': 297, 'y': 99}
Reasoning: Re-searching for "Hush (2016)"
Action: type {'text': 'Hush (2016)'}
Reasoning: Displaying "Hush" movie details, confirming needs
Agent message: The IMDb movie ID for "Hush" (2016) is 'tt5022702'. Would you need any more specifics from the website about this movie?
IMDb ID for 'Hush (2016)': tt5022702
Processing: Do-Over (2016)
Action: screenshot {}
Reasoning: Navigating to IMDb for movie search
Action: click {'button': 'left', 'x': 219, 'y': 39}
Action: type {'text': 'imdb.com'}
Action: keypress {'keys': ['ENTER']}
Action: wait {}
Reasoning: Using search bar for "Do-Over"
Action: click {'button': 'left', 'x': 326, 'y': 68}
Action: type {'text': 'Do-Over (2016)'}
Action: wait {}
Reasoning: Selecting correct film for IMDb
Action: click {'button': 'left', 'x': 357, 'y': 149}
Action: wait {}
Reasoning: Retrieving IMDb ID for Do Over
Agent message: The IMDb movie ID for "Do Over (2016)" is "tt3856414."
IMDb ID for 'Do-Over (2016)': tt3856414
Processing: 1 Mile to You (2017)
Action: screenshot {}
Reasoning: Searching IMDb for "1 Mile to You"
Action: click {'button': 'left', 'x': 314, 'y': 67}
Action: type {'text': '1 Mile to You'}
Action: keypress {'keys': ['ENTER']}
Reasoning: Clicking on "1 Mile to You" result
Action: click {'button': 'left', 'x': 313, 'y': 93}
Reasoning: Selecting "1 Mile to You" details
Action: click {'button': 'left', 'x': 213, 'y': 252}
Action: wait {}
Reasoning: Retrieving IMDb ID for movie
Agent message: The IMDb ID for "1 Mile to You" (2017) is "tt2182433".
IMDb ID for '1 Mile to You (2017)': tt2182433
Processing: 10 Action Films, Vol. 3
Action: screenshot {}
Reasoning: Searching IMDb for movie ID
Action: click {'button': 'left', 'x': 648, 'y': 70}
Action: wait {}
Reasoning: Searching for "10 Action Films, Vol. 3"
Action: click {'button': 'left', 'x': 360, 'y': 70}
Action: type {'text': '10 Action Films, Vol. 3'}
Action: wait {}
Reasoning: Completing search for action films
Action: keypress {'keys': ['ENTER']}
Action: wait {}
Reasoning: Scrolling for more search results
Action: scroll {'scroll_x': 0, 'scroll_y': 518, 'x': 565, 'y': 635}
Reasoning: Expanding search for more titles
Action: click {'button': 'left', 'x': 225, 'y': 496}
Action: wait {}
Reasoning: Scrolling for "10 Action Films, Vol. 3"
Action: scroll {'scroll_x': 0, 'scroll_y': 548, 'x': 600, 'y': 701}
Action: scroll {'scroll_x': 0, 'scroll_y': 630, 'x': 662, 'y': 695}
Reasoning: Refining search for action films
Action: click {'button': 'left', 'x': 355, 'y': 67}
Action: type {'text': 'Action Films Vol. 3'}
IMDb ID for '10 Action Films, Vol. 3': None
Processing: 10 Cloverfied Lane/Cloverfield:
Action: screenshot {}
Reasoning: Searching IMDb for movie details
Action: type {'text': '10 Cloverfield Lane/Cloverfield:'}
Action: wait {}
Reasoning: Selecting "10 Cloverfield Lane" details
Action: click {'button': 'left', 'x': 336, 'y': 94}
Reasoning: Reentering search term for suggestions
Action: type {'text': '10 Cloverfield Lane/Cloverfield:'}
Reasoning: Scrolling up to find IMDb ID
Action: scroll {'scroll_x': 0, 'scroll_y': -501, 'x': 493, 'y': 155}
Action: scroll {'scroll_x': 0, 'scroll_y': -486, 'x': 668, 'y': 210}
Action: scroll {'scroll_x': 0, 'scroll_y': -466, 'x': 672, 'y': 144}
Action: scroll {'scroll_x': 0, 'scroll_y': -528, 'x': 702, 'y': 115}
Reasoning: Accessing movie page using ID
Agent message: I've found the IMDb Movie ID for "10 Cloverfield Lane." It's "tt1179933." Can I help you with anything else related to this movie?
IMDb ID for '10 Cloverfied Lane/Cloverfield:': tt1179933
Processing: 10 Years (2012)
Action: screenshot {}
Reasoning: Searching IMDb for "10 Years" movie
Action: click {'button': 'left', 'x': 330, 'y': 67}
Action: wait {}
Action: type {'text': '10 Years (2012)'}
Action: wait {}
Reasoning: Clicking to see all results
Action: click {'button': 'left', 'x': 327, 'y': 511}
Reasoning: Re-entering search for "10 Years"
Action: type {'text': '10 Years (2012)'}
Reasoning: Selecting popular matches for movie search
Action: click {'button': 'left', 'x': 238, 'y': 496}
Reasoning: Scrolling up to select matches
Action: scroll {'scroll_x': 0, 'scroll_y': -531, 'x': 388, 'y': 159}
Action: scroll {'scroll_x': 0, 'scroll_y': -612, 'x': 443, 'y': 98}
Action: scroll {'scroll_x': 0, 'scroll_y': -464, 'x': 444, 'y': 134}
Reasoning: Exploring more popular matches results
Action: click {'button': 'left', 'x': 243, 'y': 496}
Action: wait {}
Reasoning: Refining search for "10 Years (2012)"
Action: click {'button': 'left', 'x': 332, 'y': 68}
Action: type {'text': '10 Years 2012'}
IMDb ID for '10 Years (2012)': None
Processing: Nightmare Before Christmas (1993
Action: screenshot {}
Action: click {'button': 'left', 'x': 281, 'y': 68}
Agent message: I see the IMDb search bar. I'll search for "Nightmare Before Christmas (1993)" to find the movie's page and retrieve its IMDb ID.
Action: click {'button': 'left', 'x': 400, 'y': 68}
Action: type {'text': 'Nightmare Before Christmas (1993)'}
Action: wait {}
Action: click {'button': 'left', 'x': 328, 'y': 149}
Action: wait {}
Action: click {'button': 'left', 'x': 531, 'y': 38}
Agent message: I've found the IMDb page for "The Nightmare Before Christmas." To provide you with the movie's IMDb ID, I'll inspect the page URL since it typically contains this information.
Action: click {'button': 'left', 'x': 693, 'y': 35}
Agent message: The URL is highlighted and visible in the address bar. The IMDb ID for "The Nightmare Before Christmas" is `tt0107688`.
IMDb ID for 'Nightmare Before Christmas (1993': tt0107688
Processing: 10 Things I Hate About You (1999
Action: screenshot {}
Action: screenshot {}
Reasoning: Searching IMDb for 10 Things I Hate
Action: click {'button': 'left', 'x': 327, 'y': 69}
Action: type {'text': '10 Things I Hate About You (1999)'}
Action: wait {}
Reasoning: Selecting 1999 movie from results
Action: click {'button': 'left', 'x': 319, 'y': 114}
Action: wait {}
Reasoning: Checking URL for IMDb movie ID
Action: click {'button': 'left', 'x': 248, 'y': 39}
Reasoning: Extracting movie ID for user
Agent message: The IMDb movie ID for "10 Things I Hate About You (1999)" is tt0147800. Let me know if you need anything else!
IMDb ID for '10 Things I Hate About You (1999': tt0147800
Processing: 10 Things I Hate About You, Vol.
Action: screenshot {}
Action: screenshot {}
Agent message: I see the IMDb page for "10 Things I Hate About You". The URL in the address bar includes an identifier seemingly assigned to this movie by IMDb – it's located between its two sections of forward slashes in the URL. The IMDb movie ID for "10 Things I Hate About You" is `tt0147800`. Would you like further information about this movie?
IMDb ID for '10 Things I Hate About You, Vol.': tt0147800
Processing: Princess Bride (1987)
Action: screenshot {}
Reasoning: Searching IMDb for The Princess Bride
Action: click {'button': 'left', 'x': 271, 'y': 70}
Action: type {'text': 'Princess Bride (1987)'}
Action: wait {}
Action: wait {}
Reasoning: Retrying search for "Princess Bride"
Action: scroll {'scroll_x': 0, 'scroll_y': -384, 'x': 297, 'y': 229}
Action: scroll {'scroll_x': 0, 'scroll_y': -436, 'x': 302, 'y': 132}
Action: scroll {'scroll_x': 0, 'scroll_y': -465, 'x': 351, 'y': 129}
Action: scroll {'scroll_x': 0, 'scroll_y': -522, 'x': 327, 'y': 125}
Reasoning: Typing search query for Princess Bride
Action: type {'text': 'Princess Bride (1987)'}
Action: scroll {'scroll_x': 0, 'scroll_y': -432, 'x': 336, 'y': 127}
Reasoning: Activating search bar, retrying query
Action: scroll {'scroll_x': 0, 'scroll_y': -429, 'x': 343, 'y': 128}
Action: scroll {'scroll_x': 0, 'scroll_y': -1191, 'x': 308, 'y': 133}
Action: click {'button': 'left', 'x': 306, 'y': 69}
Action: type {'text': 'Princess Bride (1987)'}
IMDb ID for 'Princess Bride (1987)': None
Processing: 10,000 B.C. (2008)
Action: screenshot {}
Reasoning: Searching IMDb for "10,000 B.C."
Action: click {'button': 'left', 'x': 484, 'y': 71}
Action: type {'text': '10,000 B.C. (2008)'}
Action: keypress {'keys': ['ENTER']}
Reasoning: Clicking on "10,000 BC" movie result
Action: click {'button': 'left', 'x': 306, 'y': 97}
Reasoning: Clicking on correct movie entry
Action: click {'button': 'left', 'x': 226, 'y': 256}
Action: wait {}
Reasoning: Retrieving unique movie ID for user
Agent message: The IMDb movie ID for "10,000 B.C. (2008)" is tt0443649, which you can see in the URL of its IMDb page. Can I assist you with anything else?
IMDb ID for '10,000 B.C. (2008)': tt0443649
Processing: Babadook (2014)
Action: screenshot {}
Reasoning: Searching IMDb for Babadook (2014)
Action: click {'button': 'left', 'x': 613, 'y': 69}
Action: type {'text': 'Babadook'}
Action: click {'button': 'left', 'x': 657, 'y': 70}
Action: wait {}
Reasoning: Opening details for "The Babadook"
Action: click {'button': 'left', 'x': 223, 'y': 251}
Action: wait {}
Reasoning: Confirming details of "The Babadook"
Agent message: The IMDb movie ID for "The Babadook" (2014) is "tt2321549". Would you like any more details or assistance regarding this movie?
IMDb ID for 'Babadook (2014)': tt2321549
Results saved to imdb_cua_results.csv
"""
