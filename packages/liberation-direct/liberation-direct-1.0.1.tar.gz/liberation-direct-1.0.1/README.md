# liberation-direct
[![PyPI version](https://badge.fury.io/py/liberation-direct.svg)](https://badge.fury.io/py/liberation-direct)

A parser for Libération's live feed page. 

The French newspaper Libération has a [live feed](http://www.liberation.fr/direct) where they regularly post short summaries of current events.
This package parses that feed, finds the latest summary and converts it into markdown. 

Example usage to retrieve the summary : 

```python
from liberation_direct import LiberationDirect
summary = LiberationDirect().get_news_summary_markdown()
print(summary)
```



