The correlations between book distance and review distance
==========================================================

This subsection of the **reviews** repository documents the experiments described in the ADHO 2020 paper "Book Reviews and the Consolidation of Genre." Authors include Kent Chang, Yuerong Hu, Shubhangi Singhal, Wenyi Shang, Aniruddha Sharma, Ted Underwood, Jessica Witte, and Peizhen Wu.

general question
----------------

Do the textual similarities between categories of fiction (genres, subjects, audience categories) correlate with the similarities between human *descriptions* of the same categories (e.g. in book reviews)?

folder structure
----------------

The subfolder **meta** contains metadata used in the experiment.

**registrations** includes the text of preregistered plans guiding the experiment; for the frozen public version of these plans see the Open Science Framework.

A lot of the code that actually runs experiments is in the folder **wmd**. That rather weird name is a legacy of a time when we thought we'd be using Word Mover's Distance for the experiment. We ended up finding better methods, but the acronym remains, and this folder still contains the code for measurements of ordinary cosine distance.

**predictive** contains two Jupyter notebooks that do predictive modeling of books, and reviews, respectively.

**rplots** contains code used to produce visualizations.

where to get data not provided here
-----------------------------------

A github repository isn't a good place for large data files, so most of the data and metadata supporting this project are located instead (with our preregistrations) at [our Open Science Framework page.](https://osf.io/a3749/)

There you can find, for instance,

**grouped_books.tsv,** which is the central metadata file. Each row represents what we considered--for the provisional purposes of this experiment--a single "title." The **htrcids* column may group multiple HathiTrust volume IDs (say, if it's a multivolume work), and the **bpoids** column will group multiple reviews from British Periodicals Online, if more than one review was identified as pointing to this title. There is also a single **bookid** beginning with "B"; it tends to be used internally in our code as a shared identified for this whole cluster of volumes and reviews.

The grouped_books metadata has some basic information about each book, like author and title. For fuller information about the books, you can see ["NovelTM Datasets for English-Language Fiction,"](https://github.com/tedunderwood/noveltmmeta) pairing the htids to rows in **volumemeta.tsv**.

For fuller information about the reviews (e.g. the periodicals they were drawn from) you want **metadata4allBPOreviews.tsv.zip** at our OSF site. This includes metadata for many reviews not used in our experiment; to identify the ones we used, you will need to pair the **bpoids** in **grouped_books.tsv** with rows in **metadata4allBPOreviews.tsv.zip**.

Information about the texts of books, and reviews, can be found in the OSF site as **bookvectors.tsv.zip** and **reviewvectors.tsv.zip.** These are numeric tables reporting the relative frequencies of the top 2500 features in both book and review collections; frequencies have already been multiplied by inverse document frequency. In the final experiments we went further and used StandardScaler from scikit-learn to convert the values in each column to z scores.
