fiction filter
==============

Some scripts we used to identify a subset of reviews in BPO that are likely to be reviews of fiction.

**parsetexts.py** pairs metadata and texts edited by Witte & Underwood to create **trainingdata.tsv.**

Then we actually do the modeling in **makemodel.ipynb**, optimizing constants with gridsearch. The results of modeling go in the **model/** subfolder.

The model is exported to the campus cluster, where **filter_fiction_for_bpo.py** does the job of applying it across the whole dataset. This requires multiple jobs, each of which take the form, e.g.

    python3 filter_bpo_for_fiction.py ../meta/matched_reviews_1850.tsv reviews1850.tsv

where the first command line argument is an input (metadata) file and the second is the filtered output for a decade.

The modeled results for different decades are concatenated in **concat_results.py**, which also adjusts them to reflect known facts in training data.

Final results are in [all_fic_results.txt](https://www.dropbox.com/s/ybnm2trgl3qizsr/all_fic_reviews.txt?dl=0). Each line is a separate review; the first tab-separated field is a recordID (which should be unique); the second is probability-of-being fiction; the third is the review text.
