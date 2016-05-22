# Cycles Within Data Science Procceses

_(Credits: some of the following come from [Diomidis Spinellis' most excellent slides](https://drive.google.com/file/d/0ByPAm2ABBQPHU1JLQlJ5eGZCTkE/view))_

According to experts in software development, human learning is cyclc:

+ If we don't make mistakes we don't learn things and if we don't learn things, we don't grow. And since doing it right the first time is not an option, we have to have feedback loops.  -- Kent Beck.

As with software, so to with
data science. [Fayyad et al. (1996)](bib.md#fayyad96) offer the classic definition of data science, as applied to real-world activities:

+ KDD (knowledge discovery in databases) is the non- trivial process of identifying valid, novel, potentially useful, and ultimately understandable patterns in data.

The following figure summarizes their approach. 

![kdd cycle](https://www.researchgate.net/profile/Martin_Shepperd/publication/220277672/figure/fig1/AS:277448081068032@1443160185199/Fig-3-The-KDD-cycle-From-11.png)

Many aspects of this figure are insightful and worthy of careful study. For example, as shown in this figure,   data science is just a small part of the total process. Even just gaining permission to access data can be a long process requiring extensive interaction with business user groups. Copying large amounts of data from one source to another can also consume a large amount of time. Once data is accessed, then raw data typically requires extensive manipulation before it is suitable for mining. This is:

+ TIP:  _Most of “data science” is actually “data pre- processing._ Before any learner can execute, much effort must be expended in selecting and accessing the data to process, pre-processing, and transforming it some learnable form.

The above figure also clearly illustrates the cyclic nature of data science:

+ Usually, finding one pattern prompts new questions such as “why does that effect hold?” or “are we sure there is no bug in step X of the method?”. Each such question refines the goals of the data science process, which leads to another round of the whole process.
+ In the initial stages of a project, engineers try different methods to generate the feedback that let users refine and mature the goals of the project.
+ Real world data is highly “quirky” and inductive engineers often try different methods before they discover how to find patterns in the data.


The repetitive nature of data science implies:

+ TIP: _In any industrial application, the data science method is repeated multiples times_ to either answer an extra user question, make some enhancement and/or bug fix to the method, or to deploy it to a different set of user.

This, in turn, has implications on tool choice:

+  TIP: _Thou shall not click:_ For serious studies, to ensure repeatability, the entire analysis should be automated using some high level scripting language; e.g. [R-script, Python, Matlab, or Bash](bib.md#nelson11).

## Kinds of Cycles

The above diagram, written in 1996, is a little light on details. Twenty years later, we can add numerous details on those cycles. Specifically, there are three kinds of cycles:

- The _semantic cycle_: 
     - Analysts use their domain knowledge to look for any quirks or errors in the data processing. 
     - By the way, with data, best assume guilty till proven innocent; i.e. consider all data as bad data until we can have found what processes are introducing systematic biases (a.k.a. errors) into that data. Once that is known, the data can be repaired (reversing the bias) and the reasoning can continue.
- The _goal cycle_ :
     - Analysts show data science products to their clients, then use their feedback to refine the goals of the project.
- The _tool chain cycle_:
     - Analysts extend and automate their tool chain.


## The Tool-Chain Cycle

### Fetch

e.g. curl find 

e.g. mysql
e.g. Selenium/REST apis


### Select

e.g. grep sql awk etc

e.g.

![egsql](https://raw.githubusercontent.com/REU-SOS/SOS/master/img/sql.png)


e.g. MongoDB/Redis

### Transform

e.g.  sort, head, tail, sed, gawk


e.g. Azure functions, etc.

### Learn

e.g. weka (see [command-line ninja](https://github.com/REU-SOS/SOS/tree/master/src/ninja)

e.g. R

e.g. scikit, cloud apis: watson, microsoft, etc.

### Visualize

e.g. gnuplot,gvpr, graphviz (dot)

e.g. d3

### Report

e.g. latex

e.g. markdown, github pages

e.g. Pandoc

### Package

e.g. Make, package management systems (e.g. pip, luarocks, etc/)

e.g. Docker, ansible, maven, npm, grunt

## Unix Tools

There are two main "families" of tools you should be familiar with:

- Ye Olde Unix shell tools (cat, grep, sed, awk, make, etc) which, while not-so-young,
  are still oh-so-useful.
- More recent web-aware tools (Selenium, JSON, maven, etc).

The UNIX shell tools push data from sources through filters along pipes:

```
command
command < inputFile
command > outputFile
command1 | command2 # pipes
command &           # run in background
```

The shell is a general programming langauge:

```
e=expansion
$e
$(command)
'literal string'
"string with \$ $e"
```

Command can run sequetially or conditionally:

```
command1 ; command2
(command1 ; command2) # in a sub-shell
command1 || command2  # do command2 only if command1 fails
command1 && command2  # do command2 only if command1 succeeds
```

Usual conditionals and loops:

```
if command; then
   commands
fi

while command; do
  commands
done

while read var; do
   commands
done

# looping over lists
for var in a b c; do
   commands # that can access $var
done

# looping over numerics
for((x=1;x<=10;x++); do
   commands # that can access $x
done

case word in
pattern1) commands1;;
pattern2) commands2;;
esac
```

### Fetching with Shell

`curl` and `wget`

- `curl` handles more protocols
- `wget` can recrusively fetch slides

```
while read ticker; do
  .
```
