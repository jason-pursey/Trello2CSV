# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:15:32 2020

@author: jp99911
"""

from datetime import datetime
import csv, json, re

fields_to_capture = [ "id", "name", "status", "due", "labels"
        ]

def load_data ( fields_to_capture ):
    lists = { }
    trello_extract = [ ]

    with open ( "trellodata.json" ) as file:
        trello_data = json.load ( file )
    
    for list_record in trello_data["lists"]:
        lists [ list_record["id"] ] = list_record["name"]

    for card in trello_data["cards"]:
        if ( card["closed"] == False ):
            idx = len ( trello_extract )
            trello_extract.append ( [ ] )

            #key = get_field ( card, "key" )
            print ( "Record: " + str ( card ) )
            trello_extract[idx] = { }
            trello_extract[idx]["id"] = card["idShort"]
            trello_extract[idx]["name"] = card["name"]
            trello_extract[idx]["status"] = lists[card["idList"]]
            if "due" in card:
                trello_extract[idx]["due"] = re.sub(r"^([0-9]{4}\-[0-9]{2}\-[0-9]{2}).*$", r"\1", str(card["due"]))
            if trello_extract[idx]["due"] == "None": trello_extract[idx]["due"] = ""
            if "labels" in card:
                for label in card["labels"]:
                    if "labels" in trello_extract[idx]:
                        trello_extract[idx]["labels"] += ", " + label["name"]
                    else:
                        trello_extract[idx]["labels"] = label["name"]

    print ( "Extract: " + str(trello_extract) )
    return trello_extract

trello_extract = load_data ( fields_to_capture )

extract_file = "Trello Extract " + ".csv"#datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".csv"
row_count = 0
with open ( extract_file, "w", newline='' ) as file:
    csvwriter = csv.DictWriter ( file, fieldnames = fields_to_capture )
    csvwriter.writeheader ( )
    for card in trello_extract:
        #if row_count == 0:
        #    header = ticket.keys ( )
        #    csvwriter.writerow ( header )
        #    row_count += 1
        csvwriter.writerow ( card )
    file.close ( )