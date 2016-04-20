# Sample reviews for a Research Report

The reviews for this paper, submitted to the Information Softwre Technology journal,
are unusually brief. Why? 

Was it because the the semantic content was amazing brilliant, insightful, etc etc? Maybe, but unlikely.

More likely it was because this research report adopted enough of the standard conventions to make it
very easy for the reviewers to parse the content.

## Reviewer #1: 

The paper is very well structured and reasoned. The
experimentation drives to the conclusions. The topic is significant
for the journal scope. The novelty is quite good. The technical
background is al suitable. The references support well the topic.

I have no concerns with the publication of this paper

## Reviewer #2: 

This is an interesting and quite well written paper that
puts the case for performing tuning optimization studies before using
data miners to find (for example) defect predictors from static code
measures. The authors used open source systems and ran the
differential evolution algorithm to explore the tuning space before
testing the tunings using hold-out data. The authors claim that the
method can efficiently find tunings that improve the detection of
precision. This paper makes strong claims that could have a major
impact on the way that software analytics is performed in the future.
As such it represents an important contribution to the field. The
final sentence of the paper "it should be possible to radically
simplify optimization and data mining with a single system that
rapidly performs both tasks" indicates an important potential benefit
of this research.

However, I think there are 3 problems with the paper that need to be
corrected prior to publication.

1. I am concerned about the reproduction of work from elsewhere.
Although the relevant paper and book are cited in section 2.3 ([27,
28]) the amount of material that is reproduced is surprisingly large.
I am also unsure what "presenting some new results from Rahman et al.
[28]" actually means.  It would obviously be wrong to present other
researchers' results as if newly discovered but I doubt that this is
the intention. Indeed, on checking the other paper, there is no
obvious overlap. This needs to be clarified.
2. I think the way that the results are presented does not do justice
to the findings in the abstract (that the improvements are large, and
the tuning is simple). In particular, tables 8 and 9 are not very
clear; why show the naive column?
3. I am distracted by the frequent use of footnotes. If the material
is important and worthy of mention then it should be included in the
main body of the paper. However, a reference to the relevant work may
be sufficient and is sometimes preferable to using a footnote.


_Detailed comments_

Abstract: 'Since the (1) the' - delete 'the'  
Section 2.1: runtimes ->   runtime  
a phenomenon makes -> a phenomenon that makes  
Section 2.2: but the cost -> but at the cost  
optimizers ->  optimizes  
better to silent -> better to be silent  
Section 2.3: 'assessment effectiveness increases exponentially with assessment effort.' - is this really what you want to say?  
'the confidence C' - another C? (we had C for configuration options previously)...

The 'Easy to use' paragraph is taken nearly verbatim from [28], as are
the 'widely-used', and 'useful' paragraphs.

Section 2.5: parameters needed for> parameters for
Eq 1 - what are d and T? - please use a where clause
Avoid footnote 5 - use a reference to PCA  instead
asks the InfoGain -> asks the InfoGain algorithm

attriubutes -> attributes

Section 4.2: answering issue -> answering this issue
have not been equalled -> has not been equalled
regression in in -> regression in
CART, would -> CART, which would

The paper would benefit from being proofread carefully, to remove a
number of typos.





