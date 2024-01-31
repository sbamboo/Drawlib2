import os
import readchar

from .terminal import draw as pos_print
from .libs.conUtils import clear

# region KEYBOARD

# Function to get a single keypress
def get_keypress():
    '''INTERNAL: Function to get a keypress'''
    return readchar.readchar()

# Function to get the up-key
def getup(keylow):
    '''INTERNAL: Function to give the up-key for your os.'''
    if os.name == 'nt':
        return keylow == "h"
    else:
        return keylow == "a"

# Function to get the down-key
def getdown_key(keylow):
    '''INTERNAL: Function to give the down-key for your os.'''
    if os.name == 'nt':
        return keylow == "p"
    else:
        return keylow == "b"

# Function to get the enter-key
def getent_key(keylow):
    '''INTERNAL: Function to give the enter-key for your os.'''
    if os.name == 'nt':
        return keylow == "\r"
    else:
        return keylow == "\n"

# Function to get the space-key
def getspc_key(keylow):
    '''INTERNAL: Function to give the spce-key for your os.'''
    if os.name == 'nt':
        return keylow == " "
    else:
        return keylow == " "

# endregion

# region FORMATTERS
def getItemFormatting(stripAnsi=bool,checked=bool,selected=bool,formatting=dict):
    '''INTERNAL: Function to apply the correct formatting to an item.'''
    v = None
    if stripAnsi == True:
        v = ""
    else:
        if checked == True:
            if selected == True:
                v = formatting.get("item_selected_checked")
            else:
                v = formatting.get("item_normal_checked")
        else:
            if selected == True:
                v = formatting.get("item_selected")
            else:
                v = formatting.get("item_normal")
        if formatting.get("partial_name") != None and formatting.get("partial_name") != "" and selected == False:
            v += formatting.get("partial_name")
    if v == None:
        v = ""
    return v

def getDescFormatting(stripAnsi=bool,selected=bool,formatting=dict):
    '''INTERNAL: Function to apply the correct formatting to an description.'''
    v = None
    if stripAnsi == True:
        v = ""
    else:
        if formatting.get("partial_desc") != None and formatting.get("partial_desc") != "" and selected == False:
            v = formatting.get("partial_desc")
    if v == None:
        v = ""
    return v

def getBoxFormatting(stripAnsi=bool,checked=bool,selected=bool,formatting=dict):
    '''INTERNAL: Function to apply the correct formatting to a selectionbox.'''
    v = None
    if stripAnsi == True:
        v = ""
    else:
        if selected == False:
            if checked == True:
                v = formatting.get("box_checked")
            else:
                v = formatting.get("box_unchecked")
    if v == None:
        v = ""
    return v

# endregion FORMATTERS

# region HELPERS
def format_size(size):
    '''INTERNAL: Helper to get correct data-size suffix in bytes not bits.'''
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    suffix_index = 0
    while size >= 1024 and suffix_index < len(suffixes)-1:
        suffix_index += 1   # increment the index of the suffix
        size /= 1024.0      # apply the division
    return f"{size:.2f}{suffixes[suffix_index]}"

class positional_printer():
    '''INTERNAL: Class for printing lines with pos.'''
    def __init__(self,pos=tuple):
        self.pos = pos
        self.yind = 0
    def print(self,i=str):
        pos_print(self.pos[0],self.pos[1]+self.yind,i)
        self.yind+=1
    def rs(self):
        self.yind = 0

def prepANSI(string):
    '''INTERNAL: Function to placehold ANSI sequences in a string.'''
    ANSI_PREFIX = "\033["
    ANSI_SUFFIX = "m"
    def replace_ansi(match):
        ansi_code = match.group(1)
        color_code = ansi_code.lstrip(ANSI_PREFIX).rstrip(ANSI_SUFFIX)
        return f"%{color_code}%"
    import re
    pattern = re.compile(f"({re.escape(ANSI_PREFIX)}\d+{re.escape(ANSI_SUFFIX)})")
    replaced_string = re.sub(pattern, replace_ansi, string)
    return replaced_string

def handleANSI(string):
    '''INTERNAL: Function to un-placegold ANSI sequences in a string.'''
    ANSI_PREFIX = "\033["
    ANSI_SUFFIX = "m"
    def replace_ansi(match):
        color_code = match.group(1)
        space = " "*len("%"+str(color_code)+"%")
        _len = len( f"{ANSI_PREFIX}{color_code}{ANSI_SUFFIX}{space}" )
        return f"{ANSI_PREFIX}{color_code}{ANSI_SUFFIX}".center(_len)
    import re
    pattern = r"%(\d+)%"
    replaced_string = re.sub(pattern, replace_ansi, string)
    return replaced_string

# endregion HELPERS

# Function to display the list of items
def single_select_display_items(selected_index, items, selkey, selTitle="Select an option:", selSuffix=None, dispWidth="vw", stripAnsi=False, formatting={"item_selected":"\x1b[32m","item_normal":"","selector":""}, prMode="std", posPrModeCoords=None, clearing=False):
    '''INTERNAL: Helper function to render a single-item selection.'''
    # get dispWidth
    width,height = os.get_terminal_size()
    if dispWidth == "vw": dispWidth = width
    if dispWidth == "vh": dispWidth = height
    if clearing == True:
        clear()
    # create print obj
    if prMode.lower() == "std":
        local_print = print
    else:
        if posPrModeCoords == None:
            posPrModeCoords = (0,1)
        local_print = positional_printer(posPrModeCoords).print
    # get the length of the longest key
    max_key_length = max(len(key) for key in items.keys())
    # print
    if stripAnsi == True:
        local_print(selTitle)
    else:
        local_print("\x1b[0m"+selTitle) # include reset to fix wrong-coloring
    for i, key in enumerate(list(items.keys())):
        # get the org-value based on selkey
        if selkey == "" or selkey == None:
            ovalue = items[key]
        else:
            ovalue = items[key][selkey]
        if "ncb:" not in ovalue:
            value = "{" + ovalue + "}"
        else:
            value = ovalue.replace("ncb:","")
        # concat a string using left-adjusted keys
        string = f"  {key.ljust(max_key_length)}   {value}"
        # if over dispwidth cut with ... to correct size (indep of key-length)
        if len(string) > dispWidth-2:
            if "ncb:" not in ovalue:
                off = 10+max_key_length                                               # numerical amnt to cut (10 is what worked and the next is so it reacts on key-len)
                string = string.replace(value,ovalue[:dispWidth-off] + "...") # chn string based on cutoff
            else:
                off = 12+max_key_length                                               # numerical amnt to cut (12 is what worked and the next is so it reacts on key-len)
                string = string.replace(value,"{"+ovalue[:dispWidth-off] + "..."+"}") # chn string based on cutoff
        # print the string with formatting if enabeld
        if i == int(selected_index):
            if stripAnsi == True:
                string = ">" + string[1:] # add the >
            else:
                string = f"{formatting['selector']}>" + string[1:] # add the >
            if stripAnsi == True:
                local_print(f"{string}")
            else:
                local_print(f"{formatting['item_selected']}{string}\x1b[0m")
        else:
            if stripAnsi == True:
                local_print(f"{string}")
            else:
                local_print(f"{formatting['item_normal']}{string}\x1b[0m")
    # print suffix msg
    if selSuffix != None:
        local_print(selSuffix)

# Main function to show a dictionary based on the dict.value.<key> / or dict.value (if selkey = ""/None)
def single_selector(nameDescDict=dict, selKey="desc", sti=0, selTitle="Select an option:", selSuffix=None, dispWidth="vw", stripAnsi=False, formatting={"item_selected":"\x1b[32m","item_normal":"","selector":""}, prMode="std", posPrModeCoords=None, clearing=False):
    """
    Function to show a single-item selection from a dictionary.
    Add "ncb:" to your value to ommit the curly brackets.
    """
    selected_index = sti # start index
    disp = True
    while True:
        # display the items if disp = True
        if disp == True:
            single_select_display_items(selected_index, nameDescDict, selKey, selTitle, selSuffix, dispWidth, stripAnsi, formatting, prMode, posPrModeCoords, clearing)
        else:
            disp = True
        # check keys and change selected index depends on keys
        key = get_keypress()
        if getup(key.lower()):
            selected_index = selected_index - 1
            # roll-over
            if selected_index < 0: selected_index = len(nameDescDict)-1
        elif getdown_key(key.lower()):
            selected_index = selected_index + 1
            # roll-over
            if selected_index > len(nameDescDict)-1: selected_index = 0
        elif getent_key(key.lower()):
            return list(nameDescDict.keys())[selected_index]
        elif key.lower() == "q" or key.lower() == "\x1b":
            return None
        # if no key pressed set disp to false, so it wont redisp on an-uncaught key
        else:
            disp = False

# Function to display the list of items with checkboxes
def multi_select_display_items(selected_index, items, selkey, checked_states, selTitle="Select options (press Enter to toggle):", selSuffix=None, dispWidth="vw", stripAnsi=False, formatting=None, prMode="std", posPrModeCoords=None, clearing=False):
    '''INTERNAL: Helper function to render a multi-item selection.'''
    def_formatting = {"item_selected":"\x1b[32m","item_selected_checked":"\x1b[32m","item_normal":"","item_normal_checked":"","box_unchecked":"","box_checked":""}
    if formatting != None and type(formatting) == dict:
        _formatting = def_formatting.copy()
        _formatting.update(formatting)
        formatting = _formatting
    if clearing == True:
        clear()
    # create print obj
    if prMode.lower() == "std":
        local_print = print
    else:
        if posPrModeCoords == None:
            posPrModeCoords = (0,1)
        local_print = positional_printer(posPrModeCoords).print
    # Get terminal width
    width, _ = os.get_terminal_size()
    if dispWidth == "vw":
        dispWidth = width

    if selTitle != None:
        local_print(selTitle)
    max_key_length = max(len(key) for key in items.keys())
    for i, key in enumerate(list(items.keys())):
        selected = i==selected_index
        if checked_states[i]:
            checkbox = f"{getBoxFormatting(stripAnsi,True,selected,formatting)}[x] "
        else:
            checkbox = f"{getBoxFormatting(stripAnsi,False,selected,formatting)}[ ] "
        if selkey == "" or selkey == None:
            item_desc = items[key]
        else:
            item_desc = items[key]["desc"]
        # check for ncb:
        ncb = False
        if "ncb:" in item_desc:
            ncb = True
            item_desc = item_desc.replace("ncb:","")
        else:
            item_desc = '{'+item_desc+'}'
        # check for btn:
        if "btn:" in item_desc:
            item_desc = "    " + item_desc.replace("btn:","")
            checkbox = ""
        # create string
        checked = True if checked_states[i] else False
        if stripAnsi == False:
            checkbox += "\033[0m"
        string = f"{checkbox}{getItemFormatting(stripAnsi,checked,selected,formatting)}{key.ljust(max_key_length)}  {getDescFormatting(stripAnsi,selected,formatting)}{item_desc}"
        if stripAnsi == False:
            string += "\033[0m"

        # Truncate and fill with ellipsis if the string is too long
        off = 12 + max_key_length  # Numerical amount to cut (12 is what worked)
        if len(string) > dispWidth - 2:
            string = string.replace(item_desc, f"{item_desc[:dispWidth - off]}...")
            if ncb == False and string.endswith("..."):
                string += "}"

        # handle newline
        if "prenl:" in item_desc:
            string = "\n" + string[::-1].replace(":lnerp","",1)[::-1]
        if "posnl:" in item_desc:
            string = string[::-1].replace(":lnsop","",1)[::-1] + "\n"

        if i == selected_index:
            local_print(f"\x1b[32m{string}\x1b[0m")
        else:
            local_print(string)
    if selSuffix is not None:
        local_print(selSuffix)

# Main function to show a dictionary and allow multiple selections
def multi_selector(nameDescDict=dict, selKey="desc", sti=0, selTitle="Select an option: (press q/esc to exit)", selSuffix=None, dispWidth="vw", prechecked=[], stripAnsi=False, formatting=None, prMode="std", posPrModeCoords=None, clearing=False):
    """
    Function to show a mukti-item selection from a dictionary.
    Add "ncb:" to your value to ommit the curly brackets.
    """
    checked_states = [False] * len(nameDescDict)
    selected_index = sti

    for i in prechecked:
        if i >= 0 and i < len(nameDescDict):
            checked_states[i] = True
    disp = True
    while True:
        if disp == True:
            multi_select_display_items(selected_index, nameDescDict, selKey, checked_states, selTitle, selSuffix, dispWidth, stripAnsi, formatting, prMode, posPrModeCoords, clearing)
        else:
            disp = True
        key = get_keypress()

        if getup(key.lower()):
            selected_index -= 1
            # roll-over
            if selected_index < 0: selected_index = len(nameDescDict)-1
        elif getdown_key(key.lower()):
            selected_index += 1
            # roll-over
            if selected_index > len(nameDescDict)-1: selected_index = 0
        elif getent_key(key.lower()) or getspc_key(key.lower()):
            idx = selected_index
            if "btn:" in list(nameDescDict.values())[idx]:
                # handle button
                return [key for i, key in enumerate(nameDescDict.keys()) if checked_states[i]],list(nameDescDict.keys())[idx]
            else:
                checked_states[idx] = not checked_states[idx]
        elif key.lower() == "q" or key.lower() == "\x1b":
            break
        else:
            disp = False

    selected_options = [key for i, key in enumerate(nameDescDict.keys()) if checked_states[i]]
    return selected_options,None

def multi_selector_dir(dirpath, sti=0, selTitle="Select an option: (press q/esc to exit)", selSuffix=None, dispWidth="vw", prechecked=[], stripAnsi=False, formatting=None, extraElems=None, prMode="std", posPrModeCoords=None, clearing=False):
    '''Wrapper function to show a mutli-select ui for a folders content.'''
    if os.path.exists(dirpath):
        items = os.listdir(dirpath)
        ditems = {}
        for item in items:
            itempath = os.path.join(dirpath,item)
            if os.path.isdir(itempath):
                subitems = os.listdir(itempath)
                subs = {"files":[],"folders":[]}
                for i in subitems:
                    ip = os.path.join(itempath,i)
                    if os.path.isfile(ip):
                        subs["files"].append(ip)
                    else:
                        subs["folders"].append(ip)
                files_str = None
                folders_str = None
                files_len = len(subs["files"])
                folders_len = len(subs["folders"])
                if files_len > 0:
                    if files_len == 1:
                        files_str = " 1 file"
                    else:
                        files_str = f" {files_len} files"
                if folders_len > 0:
                    if folders_len == 1:
                        folders_str = " 1 folder"
                    else:
                        folders_str = f" {folders_len} folders"
                final_str = ""
                if files_str != None:
                    if folders_str != None:
                        final_str = f"ncb:Has{files_str} and{folders_str}."
                    else:
                        final_str = f"ncb:Has{files_str}."
                else:
                    if folders_str != None:
                        final_str = f"ncb:Has{folders_str}."
                ditems[item] = final_str
            else: ditems[item] = f"ncb:Size: {str(format_size(os.path.getsize(itempath)))}"

        if extraElems != None:
            ditems.update(extraElems)

        sels,selbtn = multi_selector(
            nameDescDict=ditems,
            selKey=None,
            selTitle=selTitle,
            selSuffix=selSuffix,
            dispWidth=dispWidth,
            prechecked=prechecked,
            stripAnsi=stripAnsi,
            formatting=formatting,
            prMode=prMode,
            posPrModeCoords=posPrModeCoords,
            clearing=clearing
        )
        nsels = []
        for sel in sels:
            nsels.append(os.path.join(dirpath,sel))
        return nsels,selbtn
    else:
        return [],selbtn
    
def drawTable(data=dict(), prMode="std", posPrModeCoords=None, clearing=False):
    """
    Function ported from libDrawlib by Simon Kalmi Claesson,
    takes a dictionary and renders it as a table.

    Example:
        ```
        {
            "Header1":["h1elem1","h1elem2"],
            "Header2":["h2elem1","h2elem2"]
        }
        ```
        ```
        Turns into:
        ╭───────────┬───────────╮
        │  Header1  │  Header2  │
        ├-----------┼-----------┤
        │  h1elem1  │  h2elem1  │
        │  h1elem2  │  h2elem2  │
        ╰───────────┴───────────╯
        ```
    """
    # extract the headers from the dictionary keys
    headers = list(data.keys())
    num_columns = len(headers)

    if clearing == True:
        clear()
    # create print obj
    if prMode.lower() == "std":
        local_print = print
    else:
        if posPrModeCoords == None:
            posPrModeCoords = (0,1)
        local_print = positional_printer(posPrModeCoords).print

    # calculate the width of each column
    widths = []

    # iterate over each header to calculate the maximum width of that column
    for header in headers:
        # start by assuming the width is the length of the header string plus two padding spaces
        width = len(header) + 2
        # iterate over each value in the column to find the maximum width of that value
        for value in data[header]:
            # the width of each value is the length of the string plus two padding spaces
            value_width = len(str(value)) + 2
            # update the column width if the value width is greater
            width = max(width, value_width)
        # add the final column width to the list of widths
        widths.append(width)

    # calculate the width of the divider row
    divider_width = sum(widths) + len(widths) - 1

    # render the table
    local_print("╭" + "┬".join("─" * width for width in widths) + "╮")

    # render the header row
    if len(headers) > 0:
        header_row = "│"
        for header, width in zip(headers, widths):
            # center the header string in its column and add padding spaces on either side
            header_row += header.center(width) + "│"
        local_print(header_row)

    # render the divider row
    local_print("├" + "┼".join("-" * width for width in widths) + "┤")

    # render each value row
    if len(headers) > 0:
        for i in range(len(data[headers[0]])):
            value_row = "│"
            for header, width in zip(headers, widths):
                # center the value string in its column and add padding spaces on either side
                value_row += handleANSI( prepANSI(str(data[header][i])).center(width) + "│")
            local_print(value_row)

    # render the bottom of the table
    local_print("╰" + "┴".join("─" * width for width in widths) + "╯")


#custom ui with borderchars