# Plots the difference between in-genre comparisons and comparisons
# to a random sample of volumes identified as fiction.

library(ggplot2)
data <- read.csv('annotated_loc_results.tsv', sep = '\t')

# first identify the peak year, considered as the year with the biggest
# positive correlation to y and negative thereafter
biggest = 0
peak = 1859
for (y in 1885 : 1998) {
  res1 = cor.test(data$meandate[data$meandate <= y], data$fullrandomdiff[data$meandate <= y])
  res2 = cor.test(data$meandate[data$meandate >= y], data$fullrandomdiff[data$meandate >= y])
  gap = as.vector(res1$estimate) - as.vector(res2$estimate)
  # cat(y, gap, '\n')
  if (gap > biggest) {
    # cat(y, gap, '\n')
    biggest <- gap
    peak <- y
    pvalues <- c(res1$p.value, res2$p.value)
  }
}
cat('peak: ', peak, '\n')
cat(biggest, '\n')
cat(pvalues, '\n')

dates = c()
diffs = c()

dates = c()
diffs = c()

for (i in 1870:1999) {
  thesediffs = data$fullrandomdiff[data$meandate >= i - 10 & data$meandate <= i + 10]
  diffs = c(diffs, median(thesediffs))
  dates = c(dates, i)
}

df <- data.frame(meandate = dates, diff = diffs)

p <- ggplot(df, aes(x = meandate, y = diff)) + 
  geom_line(color = 'firebrick', size = 1) +
  theme_bw() + ggtitle('Difference between in-genre and random comparisons') +
  scale_x_continuous("", breaks = c(1875, 1900, 1950, 2000)) +
  scale_y_continuous('cosine distance') +
  geom_point(aes(x= peak , y= max(diffs)), colour="darkslategray3", size = 2) +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16),
        legend.position = 'none')

tiff("corrected_fullrandomdiffs.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)