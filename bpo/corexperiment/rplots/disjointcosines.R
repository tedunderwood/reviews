this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

library(ggplot2)
library(dplyr)
library(ggrepel)
expd <- read.csv('/Users/tunder/Dropbox/python/reviews/bpo/corexperiment/results/splitcomparisons.tsv', sep = '\t')
bookresults <- expd[expd$comparisontype == 'booktext', ]
reviewresults <- expd[expd$comparisontype == 'reviewtext', ]

hmeans <- with(bookresults, tapply(htrcdiff, cat, median))
bmeans <- with(reviewresults, tapply(bpodiff, cat, median))
labels = names(bmeans)

genrecos <- data.frame(book.dist = hmeans, review.dist = bmeans, 
                       labels = labels)

p <- ggplot(genrecos, aes(book.dist, review.dist)) + 
  theme_bw() +
  geom_point(alpha = 0.9, color = 'firebrick') +
  scale_y_continuous('How much in-genre reviews are closer than random') +
  scale_x_continuous('How much in-genre books are closer than random') +
  geom_text_repel(aes(book.dist, review.dist, label = labels), force = 6, box.padding = 0.25, 
                  point.padding = 0.25, max.iter = 1600, size = 4.1, min.segment.length = 0.8,
                  family = "Avenir Next Medium") +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

tiff("disjointcosines.tiff", height = 8, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)