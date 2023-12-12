# Feeds extention
If no extention is specified on running, this extention will be enabled. 

```bash
# in "paperboy" dir
python main.py
```

or you can specify explicitly
```bash
# in "paperboy" dir
python main.py -e feeds
```

### Configure
The configuration files are in the `config/feeds` dir.

| File name | Description |
|----------|-------------|
|`feed_urls.txt`        |List of feed urls to fetch|
|`prompt_summarize.txt` |The prompt to ask ChatGPT to summarize|
