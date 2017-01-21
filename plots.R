library(ggplot2)
library(dplyr)
library(stringr)
library(GGally)
library(lubridate)
setwd(getwd())

plot.dat <- read.csv('output/counts.csv') %>%
  select(keyword, keyword_count) %>%
  unique() %>%
  arrange(desc(keyword_count)) %>%
  filter(keyword_count>10) %>%
  mutate(keyword = str_wrap(keyword, width=10)) %>%
  mutate(keyword=factor(keyword, keyword)) 
jpeg('output/keyword_count.jpeg', width=1000, height=650)
ggplot(plot.dat, aes(x=keyword, y=keyword_count)) + 
  geom_bar(stat='identity') + 
  theme_minimal()  +
  ggtitle('Most frequent keywords') +
  ylab('count') + 
  theme(axis.text=element_text(size=12),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size=14),
        plot.title = element_text(size=16, face='bold'))
dev.off()

plot.dat <- read.csv('output/counts.csv') %>%
  select(section, section_count) %>%
  unique() %>%
  arrange(desc(section_count)) %>%
  filter(section_count>1) %>%
  mutate(section = str_wrap(section, width=8)) %>%
  mutate(section=factor(section, section)) 
jpeg('output/section_count.jpeg', width=1000, height=650)
ggplot(plot.dat, aes(x=section, y=section_count)) + 
  geom_bar(stat='identity') + 
  theme_minimal()  +
  ggtitle('Most frequent section') +
  ylab('count') + 
  theme(axis.text=element_text(size=12),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size=14),
        plot.title = element_text(size=16, face='bold'))
dev.off()

plot.dat <- read.csv('output/infl.csv') %>% mutate(fb_comments=comments)
jpeg('output/influence.jpeg', width=1000, height=650)
ggpairs(plot.dat, columns=c('nyt_comments', 'reactions', 'shares', 'fb_comments')) +
  theme_minimal() + 
  theme(axis.text=element_text(size=12),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size=14),
        plot.title = element_text(size=16, face='bold'))
dev.off()

plot.dat <- read.csv('output/infl.csv') %>%
  mutate(pub_date = date(pub_date)) %>%
  group_by(pub_date) %>%
  summarise(count = n())
jpeg('output/time_series.jpeg', width=1000, height=650)
ggplot(plot.dat, aes(x=pub_date, y=count)) + 
  geom_line(size=1.25) + 
  theme_minimal()  +
  ggtitle('Climate Change articles over time') +
  ylab('count') + 
  xlab('date') +
  theme(axis.text=element_text(size=12),
        axis.title.x = element_text(size=14),
        axis.title.y = element_text(size=14),
        plot.title = element_text(size=16, face='bold'))
dev.off()

plot.dat$weekend <- wday(plot.dat$pub_date) %in% c(1, 7)
jpeg('output/time_series_wkend.jpeg', width=1000, height=650)
ggplot(plot.dat, aes(x=pub_date, y=count)) + 
  geom_bar(aes(y=weekend*max(count)), stat='identity', fill='grey', alpha=.5) +
  geom_line(size=1.25) + 
  theme_minimal()  +
  ggtitle('Climate Change articles over time (weekend highlighted)') +
  ylab('count') + 
  xlab('date') +
  theme(axis.text=element_text(size=12),
        axis.title.x = element_text(size=14),
        axis.title.y = element_text(size=14),
        plot.title = element_text(size=16, face='bold'))
dev.off()

df <- read.csv('output/infl.csv') %>% filter(!is.na(influence))
df2 <- read.csv('output/counts.csv') %>% 
  group_by(id) %>%
  mutate(trump = "Trump, Donald J" %in% keyword) %>%
  select(id, trump)

plot.dat <- left_join(df, df2) %>% unique()
jpeg('output/trump_effect.jpeg', width=1000, height=650)
ggplot(plot.dat, aes(x=trump, y=influence)) + 
  geom_point(position=position_jitter(width=.1), alpha=.5) +
  stat_summary(fun.y=mean, geom='point', size=3, color='red') +
  stat_summary(fun.data=mean_cl_boot, geom='errorbar', width=.25, color='red') +
  theme_minimal()  +
  ggtitle('Trump Effect') +
  scale_x_discrete(labels=c('No Trump', 'Trump')) +
  theme(axis.text=element_text(size=12),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size=14),
        plot.title = element_text(size=16, face='bold'))
dev.off()

print(t.test(plot.dat$influence~plot.dat$trump))
