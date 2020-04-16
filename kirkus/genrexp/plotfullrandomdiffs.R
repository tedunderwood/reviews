# Plots the difference between in-genre comparisons and comparisons
# to a random sample of volumes identified as fiction.

library(ggplot2)
data <- read.csv('loc_results.tsv', sep = '\t')

dates = c()
diffs = c()

for (i in 1860:2009) {
  thesediffs = data$fullrandomdiff[data$meandate > i - 10 & data$meandate < i + 10]
  diffs = c(diffs, median(thesediffs))
  dates = c(dates, i)
}

df <- data.frame(meandate = dates, diff = diffs)

p <- ggplot(df, aes(x = meandate, y = diff)) + 
  geom_line(color = 'firebrick', size = 1) +
  theme_bw() + ggtitle('Difference between in-genre and random comparisons') +
  scale_x_continuous("", breaks = c(1860, 1900, 1950, 2000)) +
  scale_y_continuous('cosine distance') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16),
        legend.position = 'none')

tiff("fullrandomdiffs.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)