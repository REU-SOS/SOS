# Cycles and Tools for Data Science Processes

_(Credits: some of the following come from [Diomidis
Spinellis' most excellent
slides](https://drive.google.com/file/d/0ByPAm2ABBQPHU1JLQlJ5eGZCTkE/view))_

According to experts in software development, human learning is cyclic:

+ If we don't make mistakes we don't learn things
  and if we don't learn things, we don't grow. And
  since doing it right the first time is not an
  option, we have to have feedback loops.  -- Kent
  Beck.

As with software, so to with
data science. [Fayyad et al. (1996)](bib.md#fayyad96) offer the classic definition of data science, as applied to real-world activities:

+ KDD (knowledge discovery in databases) is the non-
  trivial process of identifying valid, novel,
  potentially useful, and ultimately understandable
  patterns in data.

The following figure summarizes their approach. 

![kdd
 cycle](https://www.researchgate.net/profile/Martin_Shepperd/publication/220277672/figure/fig1/AS:277448081068032@1443160185199/Fig-3-The-KDD-cycle-From-11.png)

Many aspects of this figure are insightful and
worthy of careful study. For example, as shown in
this figure, data science is just a small part of
the total process. Even just gaining permission to
access data can be a long process requiring
extensive interaction with business user
groups. Copying large amounts of data from one
source to another can also consume a large amount of
time. Once data is accessed, then raw data typically
requires extensive manipulation before it is
suitable for mining. This is:

+ TIP: _Most of “data science” is actually “data
  pre- processing._ Before any learner can execute,
  much effort must be expended in selecting and
  accessing the data to process, pre-processing, and
  transforming it some learnable form.

The above figure also clearly illustrates the cyclic nature of data science:

+ Usually, finding one pattern prompts new questions
  such as “why does that effect hold?” or “are we
  sure there is no bug in step X of the
  method?”. Each such question refines the goals of
  the data science process, which leads to another
  round of the whole process.  + In the initial
  stages of a project, engineers try different
  methods to generate the feedback that let users
  refine and mature the goals of the project.  +
  Real world data is highly “quirky” and inductive
  engineers often try different methods before they
  discover how to find patterns in the data.


The repetitive nature of data science implies:

+ TIP: _In any industrial application, the data
  science method is repeated multiples times_ to
  either answer an extra user question, make some
  enhancement and/or bug fix to the method, or to
  deploy it to a different set of user.

This, in turn, has implications on tool choice:

+ TIP: _Thou shall not click:_ For serious studies,
  to ensure repeatability, the entire analysis
  should be automated using some high level
  scripting language; e.g. Scala, [R-script, Python,
  Matlab, or Bash](bib.md#nelson11).

## Kinds of Cycles

The above diagram, written in 1996, is a little
light on details. Twenty years later, we can add
numerous details on those cycles. Specifically,
there are three kinds of cycles:

- The _semantic cycle_: 
     - Analysts use their domain knowledge to look for any quirks or errors in the data processing. 
     - By the way, with data, best assume guilty till proven innocent; i.e. consider all data as bad data until we can have found what processes are introducing systematic biases (a.k.a. errors) into that data. Once that is known, the data can be repaired (reversing the bias) and the reasoning can continue.
- The _goal cycle_ :
     - Analysts show data science products to their clients, then use their feedback to refine the goals of the project.
- The _tool chain cycle_:
     - Analysts extend and automate their tool chain.


## The Tool-Chain Cycle

One distinguishing feature of successful
data scientists is how many tools they already master,
and how fast they can master new tools.
This is needed since industrial data
scientists may try multiple algorithms each day, to
generate some novel and insightful feedback to the
users.

Below are listed some of the tools used by data
scientists. For a newbie, it is a long, long list
and those newbs might protest "can't I do everything
in (insert favorite language here)?".

The short answer is ``yes``- there are many pretty GUI tools that
let you do data manipluations with just a flick of a switch.

But the longer answer is ``no``-- especially if you want to be prepared for the
particular and specific concerens of your next data science tasks.

More specifically, when faced with a totally new domain, data science projects usually "walk" from right to left along the following curve:

![image](https://cloud.githubusercontent.com/assets/29195/15624371/55036118-2454-11e6-9e2c-3c2e968e5838.png)

In this process:

- Initially, at the right-hand-side, analysts try many one-off-queries as they talk more to business users and learn more about the domain as they
  poke around for some way into the data.
- Subsequently, towards the middle, a small number of queries are found to return the most insightful answers and the analysis focuses on the implications
  of just those critical queries;
- Finally, on the left-hand-side, the analysis stabilizes around a very small number of most insightful queries and actions. When these particular focused queries and actions get used most often, then it is time to build them into your tool chain as standard click-and-shoot queries for the general audience.

So you'll always be dealing with a lot, and we mean a lot, of tools (at least, at the start of an analysis).
The following tools divide into groups and those groups correspond to large
chunks of work in any data science project:

0. Platform
1. Fetch
2. Select
3. Transform
4. Tune
5. Learn
6. Visualize
7. Report
8. Package

______

### 0. Platform


+ Dev Environments    
    + A good terminal emulator (if you are a command line ninja); e.g. iTERM2 (if Mac)
    + Cloud clouding environemnts; e.g [Cloud9](http://c9.io)-- hey presto, instant LINUX, no install: <a href="https://cdn.c9.io/nc-3.1.2564-59d36da3/static/homepage/images/c9-web/top-carrousel-1.png"><img src="https://cdn.c9.io/nc-3.1.2564-59d36da3/static/homepage/images/c9-web/top-carrousel-1.png" width=400 align=middle></a>
    
+ CPU farms
    + AWS, Azure, etc
    + Spark (Elastic Search, log stash)
    + HPC, batch submit of large jobs (local to NC State: [instructions](https://github.com/ai-se/HPC-Clusters):  <a href="https://ncsu.edu/hpc/Images/Xeon2.jpg"><img align=middle
    src="https://ncsu.edu/hpc/Images/Xeon2.jpg" width=300></a>
    + HPCC (lexis nexis)
+ Misc
    + tiny.cc (URL management) 
    + Lastpass (or some other multi-platform password manager)
+ Co-ordination
    + Github (*)
    + Slack  (*)
    + [sharelatex (*)](http://sharelatex.com), <a href="https://www.sharelatex.com/blog/images/redesign-editor-preview.png"><img
        src="https://www.sharelatex.com/blog/images/redesign-editor-preview.png" align=middle width=400></a>

(*) Worth paying for the "free+1" level service.

______

### 1. Fetch


+ e.g. curl find , <a href="https://www.mysql.com/" target="_blank">mysql</a> <img width=500 align=middle src="https://dev.mysql.com/doc/refman/5.7/en/images/cluster-replication-ipv6.png">
+ e.g. Selenium/REST apis
+ Data sources
       + Mechanical Turk (recall the IRB)
       + [Promise REPO](http://openscience.us/repo)
       + Some others (and many, many more besides):  
       
![image](https://cloud.githubusercontent.com/assets/29195/15624025/881bf622-244b-11e6-884c-ed0af0364894.png)


______

### 2. Select

+ e.g. grep sql awk etc
+ e.g. MongoDB/<a href="http://redis.io" target="_blank">Redis</a> <img width=500 align=middle src="http://s.radar.oreilly.com/files/2013/03/redis-data-structures.png">


______

### 3. Transform

+ e.g.  sort, head, tail, sed, gawk
+ e.g. <a href="https://azure.microsoft.com/en-us/services/functions/" target="_blank">Azure functions</a>, etc. <img width=400 align=middle src="http://www.conceptdraw.com/How-To-Guide/picture/Computer-and-Networks-Azure-Windows-Azure-Network-and-Computes-Architecture.png">


______

### 4. Tune

Warning, experimental, but tuning may soon be a very big topic in
SE data science:

- [IST'16 journal](https://github.com/timm/timm.github.io/blob/master/pdf/16tunelearners.pdf)
- [Icse'16 conference](http://chakkrit.com/assets/papers/tantithamthavorn2016icse.pdf).

+ [jmetal](http://jmetal.sourceforge.net/): meta-heuristic search: <a href="http://dynamobim.org/wp-content/uploads/forum-assets/mra1242neo-tamu-edu/10/19/Optimo.gif"><img src="http://dynamobim.org/wp-content/uploads/forum-assets/mra1242neo-tamu-edu/10/19/Optimo.gif" width=400 align=middle></a>

______

### 5. Learn

+ e.g. <a href="http://www.cs.waikato.ac.nz/ml/weka/index.html" target="_blank">weka</a> (see [command-line ninja](https://github.com/REU-SOS/SOS/tree/master/src/ninja)    + e.g. R, Matlab <img width=400 align=middle src="http://weka.sourceforge.net/explorer_screenshots/ClassifyPanel.png">
+ e.g. <a href="http://scikit-learn.org/stable/" target="_blank">scikit</a>, cloud apis: watson, microsoft, etc. <img width=400 align=middle src="http://scikit-learn.org/stable/_static/ml_map.png">


______

### 6. Visualize

+ e.g. gnuplot,gvpr, graphviz (dot)
+ e.g. <a href="https://github.com/d3/d3/wiki/Gallery" target="_blank" >d3</a><img width=400 align=middle src="https://cloud.githubusercontent.com/assets/29195/15612794/371f3c54-23fe-11e6-90f5-06d22133e70d.png">
+ e.g. Kibana <a href="https://www.elastic.co/guide/en/kibana/current/tutorial-visualizing.html"><img src="https://www.elastic.co/guide/en/kibana/current/images/tutorial-visualize-pie-3.png" width=400 align=middle></a>


______

### 7. Report

+ e.g. Google docs
        + Sheets 
        + Slides
        + Docs
+ e.g. <a href="https://www.latex-project.org/" target="_blank">latex</a> <img width=400 align=middle src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/LaTeX_diagram.svg/650px-LaTeX_diagram.svg.png">

+ e.g. markdown, github pages
+ e.g. <a href="http:://pandoc.org" target-"_blank">Pandoc</a> : translates between these formats: <a href="http://pandoc.org/diagram.jpg"><img width=200 align=middle src="http://pandoc.org/diagram.jpg"></a>
+ References:
       + Fee-based services (free via NC State):
               [IEEE Xplore](http://ieeexplore.ieee.org/Xplore/home.jsp),
               [ACM digital library](http://dl.acm.org/);
       + Free:
               [Google Scholar](https://scholar.google.com/),
               [DbLp](http://dblp.uni-trier.de/db/conf/icse/icse2016c.html).
       

______

### 8.  Package

+ e.g. Make, package management systems (e.g. pip, luarocks, etc/)
+ e.g. <a href="https://www.docker.com/" target="_blank">Docker</a>, ansible, maven, npm, grunt <img width=500 align=middle src="https://docs.docker.com/engine/article-img/architecture.svg">


______

## Unix Tools

There are two main "families" of tools you should be familiar with:

- Ye Olde Unix shell tools (cat, grep, sed, awk, make, etc) which, while not-so-young,
  are still oh-so-useful.
- More recent web-aware tools (Selenium, JSON tools, maven, etc).

The UNIX shell tools push data from sources through filters along pipes:

```bash
command
command < inputFile
command > outputFile
command1 | command2 # pipes
command &           # run in background
```

The shell is a general programming langauge:

```bash
e=expansion
$e
$(command)
'literal string'
"string with \$ $e"
```

Command can run sequetially or conditionally:

```bash
command1 ; command2
(command1 ; command2) # in a sub-shell
command1 || command2  # do command2 only if command1 fails
command1 && command2  # do command2 only if command1 succeeds
```

Usual conditionals and loops:

```bash
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

Some shell examples follow.


### curl and wget

- `curl` handles more protocols
- `wget` can recrusively fetch slides

```bash
while read ticker
   curl -o $ticker.html \
   "http://www.reuters.com/finance/stocks/ratios?symbol=$ticker&rpc=66#management"
done <ticker_symbols
```

### mysql, sqlplus, osql, sqlite3, psql, odbc

![egsql](https://raw.githubusercontent.com/REU-SOS/SOS/master/img/sql.png)

```bash
# fyi 'instr' finds starting location of a string
mysql -s db \
  -e "select distinct substr(name, 1,length(name) - instr(reverse(name), '/'))
      from FILES" |
xargs ls -di      |
awk '{print $1}'  |
sort -u |
wc -l
```



### ssh

```bash
# compress there, uncompress her

$ ssh host.example.com tar cf – dir | tar xf -
```

### Pulling from Repos

The `cvs annotat`e command displays the most recent change for each line of a file in the repository.

```
$ cvs annotate f |
awk '{print $2}' |
sort    |
uniq -c |
sort -rn
```

By the way, the idiom `sort | uniq -c | sort -rn` is
pretty common.  The output shows how often lines
appear, sorted in order of that frequency.
E.g. the above outputs

```
1652 spy
1104 polina
827 ajk
372 dds
279 panos
124 mastorad
75 mm
16 nd
2 nmil
1 pappas
```

### grep

First, we need regular expressions:


```
a
.
k*
[a-z]
[^a-z]
^a
b$
\.
\[
\*
(a.b)
\1
a|b c+ d?
{9}
{,9} 
```

back to grep

```
grep '^From: ' /usr/mail/$USER # your mail
grep '[0-9]\{3\}-[0-9]\{4\}'  # {999-9999, like phone numbers}
```

### awk

An awk program is a lists of `pattern {action}` pairs.
The default `pattern` is "1" (i.e. for all records do)
and the default `action` is `print` (i.e. print record).

```
awk '/^x/     { print $2 }
     $2 == $3 { a[$2]++ }
     END      { print x }

# print sum of number in field3

$ tar tvf vmmemctl.tar | awk '{s += $3} END {print s}'
```

### sort (works for massive files) 

```
sort
-numeric-sort
-reverse
--key=2nr
--unique
--field-separator=:

$ tar tvf vmmemctl.tar | sort +2n
```

### sed


```
s/if(/if (/;s/do{/do {/
/^ \*/s/ *\*$//
s/^struct \(.*\) {/\1/p
's/\(Beetles - One - \)\(.*\)
mv "\1\2" "\2"/p' |
sed 's/\(House of Cards US -3x\)\(..\)\( - Chapter \)\(..\)\(.*\)/mv "\1\2\3\4\5" "S03E\2 - Chapter \4.srt"/' | sh

# make a directory of songs from a Beatles album
$ ls |
sed -n 's/\(Beatles - One - \)\(.*\) /\ mv "\1\2" "\2"/p' |
sh
 ```


### find

```
find . -name foo # or with regular expressions `find -name 'foo.*'
find . -type f   # find files
find . -type d   # find dirs
```

e.g.

```
$ find build  -name '*.class' -type f -mtime -7
```

(Exercise for the reader: what does the `-mtime` flag do?. Hint: `man find` (or see [explain shell](http://explainshell.com/explain?cmd=find+build++-name+%27*.class%27+-type+f+-mtime+-7)))

### So many more:

- tr, fmt, cut, paste, head, tail, uniq,
- date,rev,tac, comm,
- exec, test, diff, tee, sendmail, openssl
- gvpr (comes with graphviz). A graph walking langauge

```bash
BEG_G {
  $tvtype = TV_fwd;
  $tvroot = node($, ARGV[0]);
}
N [$tvroot = NULL; 1]
END_G {
  induce($T);
  write($T);
  exit(0);
}
```

### And the rest

And, when the above fail you:

- perl, python ruby, lua, scala
- e.g. see [How to use Ruby instead of sed and awk](http://nithinbekal.com/posts/ruby-sed-awk/)
