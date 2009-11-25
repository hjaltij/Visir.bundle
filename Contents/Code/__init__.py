# Created by Hjalti Jakobsson
# hjalti@hjaltijakobsson.com, modified by Tryggvi Larusson tryggvi.larusson@gmail.com

import re
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

PLUGIN_PREFIX   = "/video/visir"
CACHE_HTML_TIME = 3200
VISIR_URL       = "http://vefmidlar.visir.is/"
VISIR_DAY_URL   = "http://vefmidlar.visir.is/?channelID=&Date="

################################################################################

def Start():

    # Add the MainMenu prefix handler
    Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, 'Visir', 'icon-default.png', 'art-default2.jpg')

    # Set up view groups
    Plugin.AddViewGroup("Detail", viewMode = "List", mediaType = "items")

    # Set the default cache time
    HTTP.SetCacheTime(14400)

    # Set the default MediaContainer attributes
    MediaContainer.title1 = 'Visir'
    MediaContainer.content = 'List'
    MediaContainer.art = R('art-default2.jpg')

def MainMenu():

    dir = DaysList()
    return dir
        
def DaysList():
      
    dir = MediaContainer(art =  R('art-default2.jpg'), title1 = "Visir", viewGroup = "List")
    
    beintWMVURL="mms://veftv.live.visir.is/stod2"
    dir.Append(WindowsMediaVideoItem(beintWMVURL , width=1280, height=720, title = "Stod2 Beint", subtitle=None, summary=None, duration=None, thumb=None, art=None))
    
    page = XML.ElementFromURL(VISIR_URL, isHTML = True, cacheTime = CACHE_HTML_TIME)
    items = page.xpath("//select[@id='ctl00_cp1_MediaBrowserDateSelection1_dateDropDownList']/option")
    
    for day in items:
        dayURL = VISIR_DAY_URL+day.attrib["value"]
        dir.Append(Function(DirectoryItem(ParseDayPage, title = day.text, thumb = None), url = dayURL))
        
    return dir
        
def ParseDayPage(sender, url):
    
    dir = MediaContainer(art = R('art-default2.jpg'), title1 = None, viewGroup = "List")
    
    Log(url)
    dayPage = XML.ElementFromURL(url, isHTML = True, cacheTime = CACHE_HTML_TIME)
    
    items = dayPage.xpath("//table[@class='Playlist']/tr/td[2]/a")
    
    for item in items:
        epURL = VISIR_URL+item.attrib["href"]
        dir.Append(WindowsMediaVideoItem(ParseVideo(epURL) , width=1280, height=720, title = item.text.encode('Latin-1').decode('utf-8'), subtitle=None, summary=None, duration=None, thumb=None, art=None))
        
    return dir
    
def ParseVideo(url):
    page = HTTP.Request(url, cacheTime = CACHE_HTML_TIME)
    referenceFileURL = re.search(r'<param\s+name=\"FileName\"\s+value=\"([^"]+)"\s+/>', page).group(1)
    referenceFile = HTTP.Request(referenceFileURL, cacheTime = CACHE_HTML_TIME)

    videoURL = re.search(r'<REF\sHREF=\"([^"]+)\"/>', referenceFile).group(1)
    
    return videoURL