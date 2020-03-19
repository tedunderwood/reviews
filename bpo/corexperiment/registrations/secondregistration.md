second registration
===================

These experiments continue to explore the questions we were posing in our earlier inquiry. Especially this question:

`Do genre categories generally become more crisply defined or more closely knit as we move from the late 19c, through the 20c, to the present?`

Both of the experiments below are based on the intuition that the coherence and "tightness" of generic clustering in different periods can be assessed by measuring the difference between the average (random) distances between books and the distances measured between pairs of books that share a genre. The greater the difference, the more strongly books appear to be sorted by genre. This measure is loosely analogous to one called [silhouette value](https://en.wikipedia.org/wiki/Silhouette_(clustering)). The difference is that the silhouette strategy is designed for complete partitioning of a single dataset, and we need to evaluate a window that slides down a timeline.

While the distances between word vectors derived from book texts don't have obvious inherent significance in themselves, we know from our previous experiments that these distances do in practice correlate with the accuracy of predictive models--and also with predictive models of *reviews*. There is also [some previous research](https://www.aclweb.org/anthology/W18-4507/) that directly connects all of these measures to human perceptions of generic similarity and difference. So we do have some reason to treat these distances as a proxy for human judgment, although they are to be sure an imperfect proxy.

first experiment: genres assigned by librarians
------------------------------------------------

First, we plan to test the coherence of the genre categories defined by the librarians who assigned Library of Congress subject and genre headings recorded in HathiTrust metadata, from 1860 to 2010.

We grouped LoC genre and subject headings into nineteen categories. For instance "Mystery fiction" and "Detective and mystery stories, American" belong to the same category.

Next we will measure in-genre distance by selecting pairs of books in the same category, and measuring the cosine distance between their texts, using a vector of relative frequencies constructed with the 2500 most common words in the entire corpus. We will use tf-idf scaling to adjust the vectors--reflecting our intuition that relatively uncommon words are more important in discriminating genres than their sheer frequency might suggest.

(We could alternately do no adjustment, or scale all the words to have equal weight--i.e., compare z scores of the frequencies. We have tried both of these things in a previous experiment, and it didn't make a great deal of difference. A pattern durable enough to be of real significance for us should probably hold true across most methodological details of this kind.)

We will only compare books published within ten years of each other, according to our metadata. Call these books Ax and Ay (genre A, in years x and y).

As a control for each in-genre comparison, we will compare the first book in genre A (Ax) to a randomly selected book in year y (Ry), and the second book (Ay) to a randomly selected book in year x (Rx). We will try two different forms of "random selection": one is to randomly select a book from the list of books assigned to other genres. Another is to randomly select a book from a subset of books that were genuinely plucked randomly from HathiTrust (including books without any genre categorization). We consider the second more reliable, but the difference between these measurements might also be of interest.

So the overall measurement is

    ((Ax to Ry + Rx to Ay) / 2) - (Ax to Ay)

We'll date each measurement at the midpoint of years x and y.

**Hypothesis to test:**

We expect that there is some year Y in the second half of the twentieth century, such that average generic closeness (outgenre_distance - ingenre_distance) increases from 1860 to that year, and decreases thereafter, where "increases" and "decreases" describe a correlation with time. We expect the increase from 1860 to Y to be statistically significant at p < .05. The decrease thereafter might not be significant if we're comparing aggregate yearly values, though we would expect significance when we test the correlation with time on individual pairs of books.

second experiment: genre categories derived from a topic model of Kirkus Reviews
---------------------------------------------------------------------------------

The chief objection to our first experiment will be that we're using genre categories assigned retrospectively, mostly by late-twentieth-century librarians. It is possible that genres would seem more cohesive toward the end of the timeline because the genre categories were created in that period, and are simply a better fit for books at the end of the timeline.

There are several ways to address this concern; by summer, we'll be able to use explicit genre categories derived from the index of the *Book Review Digest.* But in the meantime we can use book reviews as a source of genre-like categories that were assigned by readers closer to the date of a book's publication.

After optimizing the number of topics, we produced an 80-topic model of Kirkus book reviews from 1930 to 2010. We manually inspected the model to identify 23 topics that seemed genre-*like*. We didn't expect a 1:1 mapping between topics and library genre labels, but we did try to exclude topics that were, for instance, organized around different types of evaluative language rather than different *kinds* of books.

We will evaluate these 23 topics in the same way as we evaluated the 19 library-assigned categories above. In other words, we'll select pairs of books in the same review topic, measure the Ax-Ay distance, and then compare it to the average of Ax-Ry and Rx-Ay. We'll plot the differences between in-topic and out-topic distance across a timeline.

**Hypotheses to test:**

The measurement we're making here is not purely a measurement of the cohesiveness of known groups. It is better understood as a measure of the *alignment* between review-descriptions and book-texts. If the categories inferred from reviews are also strongly marked in the books, there will be a big difference between in-topic and out-topic distance. If those categories are not strongly aligned, the difference may be smaller.

We tentatively interpret the strength of alignment as an indication that genre categories are widely recognized and shared between writers and readers.

So the first hypothesis we offer is that the average out-topic/in-topic difference, aggregated by year, will correlate with the yearly measurement in our first experiment. If this is true, we'll conclude that the retrospective character of categories in our first experiment was not the only source of the observed pattern. We're really measuring how strongly books were sorted into reception categories at the time of publication.

We also, secondarily, hypothesize that the out-topic/in-topic difference will in general be greatest when a topic is most prevalent in the model. In other words, when a "science fiction" topic is just beginning to emerge in reception, books may not yet be very clearly sorted into that category. But when it reaches its peak (measured as the proportion of words in year Y assigned to the topic), we would expect it to be a more prominent category in reception.

To formalize this as a hypothesis we can test: if we measure out-topic/in-topic difference for topic X in year Y, and the total prevalence of the topic in year Y, and aggregate those measurements across all years and topics, we expect a very small but significant (p < .05) correlation between the two variables.

It would also be interesting if this correlation were improved by sliding the two sets of measurements relative to each other on the timeline. In other words, do topics tend to reach peak prevalence *before*, or *after*, books are most clearly sorted into the topic? We'll pose that question for now in an exploratory way; it might help us frame a hypothesis about the causal relations between writing and reception.

