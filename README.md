
## Technical details

This report was created using Python 2.7 and R 3.2.3 on Mac OS 10.11.  

Required libraries (Python):
- [numpy](http://www.numpy.org/)
- [pandas](http://pandas.pydata.org/)

Required libraries (R):
- [ggplot2](http://ggplot2.org/)
- [dplyr](https://github.com/hadley/dplyr)
- [stringr](http://stringr.tidyverse.org/)
- [GGally](https://github.com/ggobi/ggally)
- [lubridate](https://github.com/hadley/lubridate)

All temporary files are stored in `/output` as json or csv. R was used primarily to generate plots and run the statistical test at the end. The plots are stored in jpeg form and stored in `/output` as well. The final report (`report.md`) is located in the top-level directory

## Improvements and next steps

One clear area for improvement of the above analyses is the coverage of influence. Increasing the number of articles with data on influence would allow for a greater degree of certainty with respect to the question of which articles and what topics are influential, and could allow more nuanced analyses. The method I've used to measure influence is flexible enough to allow entering additional measurements of influence. For instance, I could scrape other social media accounts that are likely to have shared articles in this dataset, standardizing the influence metrics for each, before including them in the 'overall' influence metric I used here. 

An alternative or additional method would be to look for which articles in this dataset are linked to within subsequent articles that are published by the NYTimes or other news outlets. While this is not a typical metric for influence in social media data, it's similar to how Google organizes their search results ([PageRank algorithm](https://en.wikipedia.org/wiki/PageRank)).

A second interesting line of inquiry would be to figure out how people respond to certain types of articles. For instance, is the sentiment of comments on Trump articles different from those on non-Trump articles? How do the reactions change after the election in comparison to before?

Finally, should we choose to expand the scope of this analysis beyond the election, we could look at some of these same questions, but with a wider lens - expanding the timeframe back a full year or more. Doing this would let us put this Trump bump in perspective, as well as to focus the exploration more on climate change itself. As it is, this analysis really turned out to be more about the election than anything else. Without some further comparisons, it's difficult to know what to make of these data. Did writing about climate change increase because of Trump? Is this in line with historical trends? Is this trump bump unique to him, or will other big-name politicians see similar increases, especially just after an election?

### How to reproduce
To reproduce code in full, make sure the above librarires are installed as described at the relevant sites.

Next, obtain api keys for the New York Times and Facebook. Instructions for the New York Times API are found [here](https://developer.nytimes.com/). Instructions for the Facebook API are located [here](https://developers.facebook.com/docs/facebook-login/access-tokens). Note for the Facebook API, you will need an app id number and an app secret. 

Open the `HI.sh` file and replace the triple X's with the relevant api key data. To run this file on a Mac, navigate to the directory containing the file and run `sh HI.sh` in the command line. This file will collect data, generate plots, and write the results of the t-test. If you wish to skip the data collection (as it is the most time intensive), you can run the analyes and plots code only by commenting out the first two lines of `HI.sh`.

### References

Some of the code used to scrape the NYTimes facebook page was taken from this blog post:

http://minimaxir.com/2015/07/facebook-scraper/

From start to finish, this project took about 20 hours, with 75% of that spent on the influence problem. The estimate is not exact because much of it was done in 10 to 15 minute increments due to the holidays and my being on vacation. This also had the effect of inflating the amount of time needed to complete the project.
