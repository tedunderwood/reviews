The correlations between book distance and review distance
==========================================================

This subsection of the **reviews* repository documents the experiments described in the ADHO 2020 paper "Book Reviews and the Consolidation of Genre." Authors include Kent Chang, Yuerong Hu, Shubhangi Singhal, Wenyi Shang, Aniruddha Sharma, Ted Underwood, Jessica Witte, and Peizhen Wu.

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
