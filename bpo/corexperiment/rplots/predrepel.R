this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

library(ggplot2)
library(dplyr)
library(ggrepel)
revpred <- read.csv('/Users/tunder/Dropbox/python/reviews/bpo/corexperiment/predictive/predictive1reviews.tsv', sep = '\t')
bookpred <- read.csv('/Users/tunder/Dropbox/python/reviews/bpo/corexperiment/predictive/predictive1books.tsv', sep = '\t')
pred <- data.frame(books = bookpred$meanvalidation, reviews = revpred$meanvalidation, 
                       labels = bookpred$genre)

p <- ggplot(pred, aes(books, reviews)) + 
  theme_bw() +
  geom_point(alpha = 0.8, color = 'firebrick') +
  scale_y_continuous('Accuracy for reviews') +
  scale_x_continuous('Accuracy for book texts') +
  geom_text_repel(aes(books, reviews, label = labels), force = 5.8, box.padding = 0.3, 
                  point.padding = 0.25, max.iter = 1500, size = 4.3, min.segment.length = 0.8,
                  family = "Avenir Next Medium") +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

tiff("figure2.tiff", height = 8, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)