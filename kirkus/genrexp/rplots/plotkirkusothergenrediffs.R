# Plots the difference between in-genre comparisons and comparisons
# to volumes assigned to a different genre.

library(ggplot2)
data <- read.csv('kirkus_results.tsv', sep = '\t')

kdiffs = c()
kdates = c()

for (i in 1934:2006) {
  thesediffs = data$othergenrediff[data$meandate >= i - 3 & data$meandate <= i + 3]
  kdiffs = c(kdiffs, median(thesediffs))
  kdates = c(kdates, i)
}

df <- data.frame(meandate = kdates, diff = kdiffs)

p <- ggplot(df, aes(x = meandate, y = diff)) + 
  geom_line(color = 'dodgerblue', size = 1) +
  theme_bw() + ggtitle('Difference between in-genre and other-genre comparisons (Kirkus)') +
  scale_x_continuous("") +
  scale_y_continuous('cosine distance') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16),
        legend.position = 'none')

tiff("kirkusothergenrediffs.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)