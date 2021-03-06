from typing import List

from .exception import *
from .waifu import AsyncWaifu
from .func import *

async def GenerateWaifuAsync(seeds: list=None, step=0)-> AsyncWaifu:
    # There is no way to get only one waifu, so we generate 16 and pick the first one
    r = await GenerateWaifusAsync(seeds, step)
    return r[0]

async def GenerateWaifusAsync(seeds: list=None, step=0) -> List[AsyncWaifu]:
    """
        Generate 16 waifus

        `seeds`: Generate a waifu based on a waifu seed
    """

    # Getting ready to send a resp to the API
    waifu_obj = {} # The waifu object to send to the api.
    waifus = [] # All the waifu's the API sends back to us.
    waifu_obj['step'] = max(0, min(3, step)) # Sets the steps. Makes sure it is in the range of 0 - 3
    
    if waifu_obj['step'] > 0: # Checks if we are in step 1, 2, or 3
        waifu_obj['currentGirl'] = seeds # Adds the seed to the waifu object to be sent.
        if not isvalidseed(waifu_obj['currentGirl']): # Checks if the seed is a valid seed that can be sent.
            raise WaifuInvalidSeed("No valid 'Waifu' or 'Seeds' provided")

    fet = await fetch_async("generate", waifu_obj)
    
    resp = await valid_async_response(fet) # Everything is ok! Send the request.

    if "newGirls" not in resp: # Checking if we did not get any new waifus
        raise WaifuInvalidResponse(f"Expected 'newGirls' in resp, got {resp}.")

    generatedWaifus = resp['newGirls'] # Get the new waifus
    
    for x in generatedWaifus: # Make a new Waifu object for all waifus generated
        waifus.append(AsyncWaifu(base64=x['image'], seeds=x['seeds']))

    return waifus