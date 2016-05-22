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


The following tools divide into groups and those groups correspond to large
chunks of work in any data science project.

### Fetch

e.g. curl find , mysql
e.g. Selenium/REST apis


### Select

e.g. grep sql awk etc

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

![egsql](https://raw.githubusercontent.com/REU-SOS/SOS/master/img/sql.png)

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

(Exercise for the reader: what does the `-mtime` flag do?. Hint: `man find`.)

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