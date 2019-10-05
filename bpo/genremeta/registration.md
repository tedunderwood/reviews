First registration
------------------------

We are building a collection of reviews of English-language fiction that will stretch from the early nineteenth century to the early twenty-first. 

This collection may ultimately cast light on many aspects of literary history, including literary judgment and gender bias. But in this project, we propose to use it to pose questions about genre. 

For instance, Why do new genre categories emerge, and why do old ones disappear? Are genre categories perceptible first in literary production (as a cluster of similarities between books) or in literary reception (as a cluster of similarities between reviews)? How firm are the boundaries between the things we call "subject categories", "market segments," "literary movements," and "genres"?

The immediate goal of this first registration is simply to explore assumptions about the way the verbal similarity between fictional texts does (or doesn't) map onto verbal similarity between reviews.

We will test this by comparing the predictive accuracy of models trained on groups of book-texts to the accuracy of models trained on groups of reviews (for those same books). We believe there will turn out to be some relationship, but we don't know how strong the relationship will be.

In each case a positive category (e.g. "folklore") will be contrasted to a contrast set that excludes the positive category (e.g. "folklore_contrast").

We will compare the strength of the boundary between groups of fictional texts to the strength of the boundary between groups of reviews, to understand how closely readers' characterization of fiction is related to the linguistic differences in the texts.

Three important caveats about the experiment:

1) First, we know the experiment is under-powered. We have at this point a relatively small sample of novels matched to reviews (9,140) and more importantly a very small sample of genre tags. So we can only create fourteen categories for this initial exploration. We are not necessarily expecting to see p < .05.

2) We know there is an admixture of 5-10% nonfiction in our collection, and we have not manually removed it for this experiment.

3) We acknowledge that not all of the categories we are testing would normally be called "genres." Some would probably be called subject categories (e.g. books about North America), or audience categories (e.g. juvenile fiction). A couple of the categories are "controls," selected more or less randomly.

This means that any conclusions we draw from the experiment will not apply with great force specifically to reasoning about "genre." 

But then, the boundary between a genre and a subject is in reality quite blurry (which is why subject classifications could be used for so long as a stand-in for classification by genre). For instance, "historical fiction" and "war stories" are usually treated as genres, although they could just as well be understood as subjects. Even "Western stories" and "mysteries"--which are more stylized in form than the average historical novel--have a subject-like dimension. In any case, it makes sense to get an overview of this problem before zooming in on the subset of it that most readers would characterize as a question about genre proper.

In place of a p < .05 criterion, we can offer a few descriptive hypotheses. A) We would expect relatively random categories ('random' and 'unmarked') to be harder to classify than generic categories like ('novel' and 'romance'). B) We also expect loose generic categories (like 'novel' and 'romance') to be harder to classify than more specialized categories (like 'war stories' and 'folklore'). C) We expect the relations in A and B to hold both in fictional texts and in reviews.