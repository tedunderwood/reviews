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

==>  To get a sample for manual tagging, **scrape_review_sample1.py** and **..._sample2.py** randomly sample these matched-review tables, and create two different subsets. The first of the two scripts put its sample in the **meta/** folder. The second put its sample in the **newmeta/** folder.

The difference between the two is first of all that the first sample was 1800-1919, and the second was 1830-1939. Also the first of the two scripts supplements its sample of matched fiction with a small sample of more-random selections from the **allreviews.py.** 

**We actually used rows 0 to 299 from the first sample, and 300 forward from the second.**