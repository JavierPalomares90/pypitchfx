#!/usr/bin/env python
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import gids as gds
import argparse
from datetime import datetime

'''
Python tool to scrape pitchf/x data from mlb's website.
Inspired by pitchfx package written in R
Author: Javier Palomares
'''

def gids2urls(gids):
    urls = []
    root = "http://gd2.mlb.com/components/game/mlb"
    for gid in gids:
       elements = gid.split('_') 
       year = elements[1]
       month = elements[2]
       day = elements[3]
       url = "{root}/year_{year}/month_{month}/day_{day}/{id}".format(root=root,year=year,month=month,day=day,id=gid)
       urls.append(url)
    return urls



def makeUrls(start=None,end=None,gids=None):
    if gids is None:
        if start is None or end is None:
            raise Exception("Need to specify start or end")
        gids = gds.get_gids()
        subset_gids = get_subset_gids(gids,start,end)
        return gids2urls(subset_gids)
        
        
def get_subset_gids(gids,first,last):
    list = []
    first_dt = datetime.strptime(first,"%Y-%m-%d")
    last_dt = datetime.strptime(last,"%Y-%m-%d")
    for gid in gids:
        elements = gid.split('_')
        gid_dt = datetime.strptime(elements[1]+"-"+elements[2]+"-"+elements[3],"%Y-%m-%d")
        if(first_dt <= gid_dt and gid_dt <= last_dt):
            list.append(gid)
    return list
        

def scrape(start,end,game_ids=None,suffix="inning/inning_all.xml",db_connection=None):
    if game_ids is None:
        game_dir = makeUrls(start,end)
    else:
        game_dir = makeUrls(gids=game_ids)
    for url in game_dir:
        print(url)
    pass
    
def get_args():
    parser = argparse.ArgumentParser(description='Scrape data')
    parser.add_argument('-s','--start')
    parser.add_argument('-e','--end')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    start = args.start
    end = args.end
    scrape(start,end)

if __name__=="__main__":
    main()
