bpo
=========

Extracting a sample of fiction book reviews from British Periodicals Online.

This is easier said than done. After limiting to ObjectType "Review" and SubjectTerms "English literature," one still has 476,800 reviews, only a small fraction of which are reviews of fiction. (Many are still reviews of nonfiction.) We have deployed several strategies to sharpen the focus:

1. Fuzzy matching the review title ("RecordTitle") with known titles of long-19c novels (and author names).

2. Manually evaluating a sample of reviews, to assess whether they're fiction

3. Predictive modeling, trained on the manual sample, to assist fuzzy matching in constructing a final sample.

The pipeline represented here: **scrape_bpo_meta.py** works on the original collection to generate metadata tables including everything; not just reviews. The data at this stage is quite bulky so all the work was done on a cluster.

==> **gather_reviews.py** iterates through those metadata tables to find items that are tagged as "Review" and "English Literature." It collates those into a table called **allreviews.tsv**, which still has 476,814 lines.

==> **match_reviews_2books.py** does fuzzy matching of **allreviews** to [**titlemeta.tsv**](https://github.com/tedunderwood/noveltmmeta/tree/master/metadata) in order to identify reviews that are likely to discuss a specific novel. Doing this creates a sequence of files, **matched_reviews_1800,** **matched_reviews_1810**, and so on. These are still a little bulky for the repo.

==>  To get a sample for manual tagging, **count_reviews.py** randomly samples these matched-review tables. It supplements that with a small sample of more-random selections from the **allreviews.py.** This creates a subset called **selectedrows.tsv**, which is present here in the [**meta/**](https://github.com/tedunderwood/reviews/tree/master/bpo/meta) subfolder.