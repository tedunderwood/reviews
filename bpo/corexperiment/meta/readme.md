metadata for first experiment on bpo reviews
============================================

Several metadata tables for the experiment.

**grouped_books.tsv** is the main one. Each row in this table points to a *set* of htrcids (books) and bpoids (reviews) that have been identified as referring to the same title and author. The book itself is identified by a bookid.

To convert the strings in the table into Python sets I recommend ast.literal_eval:

    import ast
    idset = ast.literal_eval(pandastable['field'])

For the review texts, see [**all_fic_reviews.txt**](https://github.com/tedunderwood/reviews/tree/master/bpo/filtered), where review texts that have been filtered by a fiction model are paired with bpoids.

**common_book_genres.tsv** is a list of subject and genre headings that occur in **grouped_books,** sorted by frequency.

Each row in **genre_categories_for_exp2.tsv** lists a group of headings that will be used to define a single genre in [experiment 2b of the first registration.](https://github.com/tedunderwood/reviews/blob/master/bpo/corexperiment/registrations/firstregistration.md)
