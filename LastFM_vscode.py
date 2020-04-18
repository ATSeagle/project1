#dependencies

import pandas as pd
import requests
import json
from pprint import pprint
from config import lastfm_api

#Create Top Love Songs DataFrame to populate with info retrieved from LastFM
top_songs_df=pd.DataFrame({
    "Rank": [],
    "Song Name": [],
    "Artist": [],
    "Duration": [],
    "Album": []
})
# top_songs_df

#INSTRUCTIONS FROM WEBSITE
    #note: Use UTF-8 to encode arguments when calling API methods.
    #limit (Optional) : The number of results to fetch per page. Defaults to 50.
    #page (Optional) : The page number to fetch. Defaults to first page.

#Set the parameters to LastFM API calls. Method and Limit are empty so we can adjust them to specific calls\
#like get_top_tracks or track.getInfo

params={
    "tag": "love",
    "api_key": lastfm_api,
    "format": "json",
    "method":"",
    "limit": ""
}

base_url= "http://ws.audioscrobbler.com/2.0/?"
example_url= "/2.0/?method=tag.gettoptracks&tag=disco&api_key=YOUR_API_KEY&format=json"    #taken from website


#API call for 1000 songs using tag.getTopTracks
params["limit"]=1000
params["method"]= "tag.gettoptracks"

response=requests.get(base_url, params=params).json()
# pprint(response)

#The 1000 songs are in a list under "response["tracks"]["track"]". I generated a df so I can iterate through the rows to\
#retrieve info
#This way it's also easier to retrieve urls for secondary API calls

results_df=pd.DataFrame(response["tracks"]["track"])
results_df.head()


#The 1000 songs are in a list under "response["tracks"]["track"]"
results=response["tracks"]["track"]

for index, row in results_df.iterrows():
    song= results[index]["name"]     
    artist= results[index]["artist"]["name"]
    print(f'Info retrieved for song:{song} by {artist}')
    
    #Retrieve info about date release of album and track duration
    try:
        song_url=f'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={lastfm_api}\
                    &track={song}&artist={artist}&format=json'
        song_response=requests.get(song_url).json()
        print(f'-->Retrieving album name for {song} by {artist}')
        album=song_response["track"]["album"]["title"]

#       #Trying to retrieve album info to check release date but couldn't find any info besides wiki page
#       album_url=f'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={lastfm_api}\
#                         &artist={artist}&album={album}&format=json'
#       album_response=requests.get(album_url).json()
#       pprint(album_response)
    except (KeyError, IndexError, ValueError):
        print(f'----Missing field/result for {album} by {artist}. Skipping----')
    
    #Populate df
    try:
        top_songs_df.loc[index, "Rank"]=results[index]["@attr"]["rank"]
        top_songs_df.loc[index, "Song Name"]=results[index]["name"]
        top_songs_df.loc[index, "Artist"]=results[index]["artist"]["name"]
        top_songs_df.loc[index, "Duration"]=results[index]["duration"] 
        top_songs_df.loc[index, "Album"]=song_response["track"]["album"]["title"]
            
    except (KeyError, IndexError):
        print(f'----Missing field/result for {song} by {artist}. Skipping----')


#Display dataframe and save as csv
top_songs_df.to_csv("csv/top_love_songs.csv")
top_songs_df

#Check if all rows of the df have been populated
#NOTE: not all songs have duration info (0). If we want to use duration to answer questions, we need to fill in the gaps
#NOTE: some albums are missing?
top_songs_df.count()  


#MAYBE  GOOD TO DO JUST FOR THE PRESENTATION, DURATION IN SECONDS IS EASIER TO MANIPULATE FOR THE ANALYSIS
#Convert seconds in HH:MM:SS format
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
#     hour = seconds // 3600    #we don't need hours
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
#     return "%d:%02d:%02d" % (hour, minutes, seconds)
    return "%02d:%02d" % (minutes, seconds)

# Example 
n = 259
print(convert(n))

###TRYING TO RETRIEVE RELEASE ALBUM INFO

##Test with Cher and Believe album as shown in LastFM website
# album_url=f'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={lastfm_api}\
#             &artist=Cher&album=Believe&format=json'

# album_response=requests.get(album_url).json()
# pprint(album_response)    