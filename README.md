# gdorking

gdorking, a short-name for Google Dorking ("Google Hacking"), this document is a consolidated breakdown of advanced search queries and filtering to not only used to get the best search results, but also a passive non-obtrusive method of information gathering against unsecured and improperly configured websites.

## Data Sources

This repository auto-generates a list of all the latest Google Dorking queries from the Exploit DB archive. The queries are stored in the [data][data] directory in three different formats: text, markdown, and JSON. The data is updated on a weekly cadence.

- [Text File][textdata]
- [Markdown File][markdowndata]
- [JSON File][jsondata]
- [CSV File][csvdata]

## Operators

- **after:** Search for results from after a particular date.
  - Example: `apple after:2007-06-29`
  
- **allintext:** Search for pages with multiple words in their content.
  - Example: `allintext:apple iphone`

- **allintitle:** Search for pages with multiple words in the title tag.
  - Example: `allintitle:apple iphone`

- **allinurl:** Search for pages with multiple words in the URL.
  - Example: `allinurl:apple iphone`

- **AND:** Search for results related to X and Y.
  - Example: `jobs AND gates`

- **before:** Search for results from before a particular date.
  - Example: `apple before:2007-06-29`

- **cache:** Find the most recent cache of a webpage.
  - Example: `cache:apple.com`

- **define:** Search for the definition of a word or phrase.
  - Example: `define:entrepreneur`

- **ext:** Same as `filetype:`
  - Example: `apple ext:pdf`

- **filetype:** Search for particular types of files (e.g., PDF).
  - Example: `apple filetype:pdf`

- **in:** Convert one unit to another.
  - Example: `$329 in GBP`

- **intext:** Search for pages with a particular word in their content.
  - Example: `intext:apple iphone`

- **intitle:** Search for pages with a particular word in the title tag.
  - Example: `intitle:apple`

- **inurl:** Search for pages with a particular word in the URL.
  - Example: `inurl:apple`

- **map:** Force Google to show map results.
  - Example: `map:silicon valley`

- **movie:** Search for information about a movie.
  - Example: `movie:steve jobs`

- **OR:** Search for results related to X or Y.
  - Example: `jobs OR gates`

- **related:** Search for sites related to a given domain.
  - Example: `related:apple.com`

- **site:** Search for results from a particular website.
  - Example: `site:apple.com`

- **source:** Search for results from a particular source in Google News.
  - Example: `apple source:the_verge`

- **stocks:** Search for stock information for a ticker.
  - Example: `stocks:aapl`

- **weather:** Search for the weather in a location.
  - Example: `weather:san francisco`

- **|:** Same as `OR`
  - Example: `jobs | gates`

- **" ":** Search for results that mention a word or phrase.
  - Example: `"steve jobs"`

- **( ):** Group multiple searches.
  - Example: `(ipad OR iphone) apple`

- **\*:** Wildcard matching any word or phrase.
  - Example: `steve * apple`

- **+:** Concatenates words to detect pages using multiple specific keywords.

- **-:** Search for results that don’t mention a word or phrase.
  - Example: `jobs -apple`

### Deprecated Operators

- **#..#:** Search within a range of numbers.
  - Example: `iphone case $50..$60`

- **inanchor:** Search for pages with backlinks containing specific anchor text.
  - Example: `inanchor:apple`

- **allinanchor:** Search for pages with backlinks containing multiple words in their anchor text.
  - Example: `allinanchor:apple iphone`

- **AROUND(X):** Search for pages with two words or phrases within X words of one another.
  - Example: `apple AROUND(4) iphone`

- **loc:** Find results from a given area.
  - Example: `loc:"san francisco" apple`

- **location:** Find news from a certain location in Google News.
  - Example: `location:"san francisco" apple`

- **daterange:** Search for results from a particular date range.
  - Example: `daterange:11278-13278`

## Contributing

Contributions are welcome! Feel free to submit pull requests to add more operators or improve existing information.

## License

This README file is licensed under the [MIT License][license].

[license]: /LICENSE
[textdata]: ./data/google-dorking.txt
[markdowndata]: ./data/google-dorking.md
[jsondata]: ./data/google-dorking.json
[csvdata]: ./data/google-dorking.csv
[data]: ./data/
