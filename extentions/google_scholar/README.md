# google_scholar
## Preparation
```bash
# in extentions/google_scholar dir
pip install -r requirements.txt
```

## Configurations
The configuration files are in the `config/google_scholar` dir.

| File name | Description |
|----------|-------------|
|`search_keywords.txt`        |List of feed urls to fetch|
|`prompt_summarize.txt` |The prompt to ask ChatGPT to summarize|

### Search Keywords
You can customize the search keywords by editing `search_keywords.txt`.  
Each line is a keyword. The search will be performed for each line.

```python 
# examples
deep learning
machine learning 

# You can also use AND / OR operator
transformer OR attention
```

### Summarization Prompt
You can change the summarization prompt by editing `prompt_summarize.txt`.


### Search Optimization
You can customize the search & summarization size by environment variables.

| Environment Variable | Description |
|----------|-------------|
|`SEARCH_LIMIT`|The maximum number of papers to search.|
|`BATCH_SIZE`|The number of papers to summarize at once.|