third registration
===================

Having gotten generally positive results from our second experiment, we want to refine our methods and do one last experiment.

First a quick summary of results from the last set of experiments.

results from second experiment
-------------------------------

The main question we posed was whether genre boundaries become strongest in the second half of the twentieth century. Formally, is there is some year Y in the second half of the twentieth century, such that average generic closeness (outgenre_distance - ingenre_distance) increases from 1860 to that year, and decreases thereafter, where "increases" and "decreases" describe a correlation with time. We expect both correlations to be significant at p < .05, if we compare the differences for individual pairs of books to the midpoint dates for those pairs.

We asked this using LoC genre labels assigned by librarians. The answer was "yes": there was a significant rise to some point in the later 20c, and a significant decline thereafter, for all of the measurement methods we proposed.

We also posed a sub-experiment using "genres" inferred from a topic model of *Kirkus* book reviews from the 1930s forward. We hypothesized that the strength of genre boundaries (outgenre-ingenre differences) would correlate significantly with the pattern in the LoC data; the answer was yes.

Finally, we speculated that in the genres inferred from book reviews, the genre would be most distinct from other books when the genre was largest (that is, in years when more books are assigned to the genre). Here, we could reject the null hypothesis as a single test across all genres; r = .057, p = .018. Considering individual genres, a Bonferroni correction for multiple comparisons only allowed us to say with confidence that the pattern held for topic 30 (erotic fiction).

motivation for third experiment
--------------------------------

Although we got statistically significant results for all of the experiments, we found the LoC data somewhat tricky to interpret, for several reasons:

1. We had selected volumes to ensure a relatively even spread across genres in each period. This is one relevant way of testing the strength of the genre system (allowing each genre to count equally). But readers might also want to know whether the hypothesis holds across a representative random sample of books—-one often dominated by particular genres in particular periods (e.g. historical fiction in the 19c).
2. Our "fully random" contrast dataset was too small to produce a smooth curve.
3. We found that *all* distances were declining in the first half of the timeline. After some investigation, we decided this was because the tf-idf weighting we were using gives a lot of weight to a small number of common words, and the frequencies of those words were more variable early in the timeline because of straightforward aspects of 19c fiction: some volumes are quite short, and others are written substantially in dialect, so that "the" gets systematically replaced by "de," for instance. Details like this may only affect a few words, but those words have a lot of weight when the vector is adjusted by tf-idf. As a result, distances are generally larger in the 19c, making it hard to interpret the significance of changing *differences* between distances (the trend does follow the pattern we predicted, but with noisy variation). Weighting vectors with Delta (converting frequencies to z scores) is recommended by many authorities, and was considered as a possibility in our second registration; in this case the Delta measure would have the specific benefit that it's not as strongly affected by the peculiarities of nineteenth-century fiction.

To address these concerns (and a few others), we propose another version of the LoC experiment, with these adjustments:

+ we will use almost 2x the total number of books (more than 6000), and in particular almost 3x more "fully random" books (around 1100),
+ also sample volumes in a more strictly random way (allowing genre proportions to vary), and sample them more evenly across the timeline
+ keep the sizes of those books relatively constant (by excluding volumes < 11000 words and truncating ones > 60000 words),
+ manually groom the list to exclude obvious nonfiction, and
+ weight word-frequency vectors using the Delta logic rather than tf-idf, guided by the arguments in [Evert et al.](https://academic.oup.com/dsh/article/32/suppl_2/ii4/3865676)


