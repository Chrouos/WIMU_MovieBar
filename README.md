# WIMU_MovieBar

# Setting
create a new file name `.env` to save the default settings
```
EMAIL="change to your email address"
PASSWD="change to your password"
cookie_path_dir="./cookies/"
```

## Start
```py
# Movie-TV-Recommendations => 66207bb286188d2c9787a941 (use the id to connect to the assistant)
hugging_chat_movie.change_assistant(_assistant_id="66207bb286188d2c9787a941")

# Change to the assistant than query the problem 
hugging_chat_movie.query(
    _query="告訴我歌喉讚的主角是誰?", 
)
```