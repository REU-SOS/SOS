<img align=right height=200 src="http://www.chantetter.nl/it-fun3/go-away.jpg"><img align=right height=200 src="http://www.blogking.biz/wp-content/uploads/Woothemes_Ninjas.jpg">
    
# Ninja.rc

Download:

- This file: [ninja.rc](ninja.rc)
- Entire ninja system [ninja.zip](../ninja.zip)

________

```bash
#!/usr/bin/env bash

# For pretty version of this code, see
# https://github.com/REU-SOS/SOS/blob/master/src/ninja/ninjarc.md

########################################################
# ninja.rc : command line tricks for data mining
# Copyright (c) 2016 Tim Menzies tim@menzies.us

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
########################################################

# INSTALL:

# 1. Download https://goo.gl/rNmPcV (is a zip file)
# 2. unzip that zip file
# 3. cd ninja
# 4. sh ninja

# USAGE:

# Here=$(pwd) bash --init-file ninja.rc -i

# TIP: place the above line into a file "ninja" and call with
#
#    sh ninja

## 0 ###################################################

# TIP: start with examples of how to call this code

# TIP: know your seed (so you can reproduce 'random' runs)

Seed=1

eg1() { ok; crossval 2 2 data/soybean.arff   $RANDOM j48 nb; }
eg2() { egX data/jedit-4.1.arff $Seed
	statsX 
      }

egX() { ok
	local what=`basename $1 | sed 's/.arff//' `
	crossval 5 5 $1 $2 rbfnet bnet j48 nb > $Tmp/egX
	gawk  '/true/ {print $2,$10}' $Tmp/egX > $Tmp/egX.pd
	gawk  '/true/ {print $2,$11}' $Tmp/egX > $Tmp/egX.pf	
      }

statsX() {
    echo "pd"; python stats.py < $Tmp/egX.pd
    echo "pf"; python stats.py < $Tmp/egX.pf	
}

# example output from "eg2" (rbfnet looks best for this data)

# pd
# rank ,         name ,    med   ,  iqr
# ----------------------------------------------------
#    1 ,           nb ,      45  ,    18 (   ------  *  -|---           ),27, 41, 45, 52, 64
#    1 ,          j48 ,      47  ,    25 ( -------    *  |---           ),22, 38, 47, 56, 64
#    2 ,       rbfnet ,      56  ,    10 (         ----  * -----        ),42, 50, 56, 59, 73
#    2 ,         bnet ,      58  ,    17 (       ------  |*   ------    ),37, 50, 58, 67, 81

# pf
# rank ,         name ,    med   ,  iqr
# ----------------------------------------------------
#    1 ,           nb ,       8  ,     6 (    --   * ----|-             ), 4,  6,  8, 10, 15
#    2 ,       rbfnet ,       9  ,     7 (    ----- *    |-----         ), 4,  8,  9, 14, 19
#    2 ,          j48 ,      10  ,    10 (   -----   *   |  ------      ), 3,  7, 10, 16, 21
#    2 ,         bnet ,      13  ,     8 (        ---   *|   --         ), 7, 10, 13, 17, 19

## 1 ###################################################
# TIP: uncomment the next line to get debug information

#set -x

## 2 ####################################################
# CONFIG Stuff

# 2a) magic strings

Me=demo1

# 2b) $Tmp for short-lived throwaways and $Safe for slow-to-reproduce files

Tmp="/tmp/$USER/$$" # A place to store BIG files. Warning: /tmp has limits on some sites
Safe="$HOME/tmp/safe/$Me"

# 2c) $Raw = source of raw data; $Cooked= pre-processed stuff

Raw=$Here
Cooked="$Safe"

# 2d) java libraries

Jar="$Here/weka.jar"
Weka="java -Xmx1024M -cp $Jar "

# 2e) Write edtior config files somewhere then tweak call
#     to editor to use thos files

Ed="/Applications/Emacs.app/Contents/MacOS/Emacs"
Edot="/tmp/edot$$"

e() { $Ed -q -l "$Edot" $* &  # $Edot defined below 
}

cat << 'EOF' > $Edot
(progn

  (setq require-final-newline    t) 
  (setq next-line-add-newlines nil) 
  (setq inhibit-startup-message  t)
  (setq-default fill-column     52)
  (setq column-number-mode       t)
  (setq make-backup-files      nil) 
  (transient-mark-mode           t)
  (global-font-lock-mode         t)
  (global-hl-line-mode           0)  
  (xterm-mouse-mode              t)
  (setq scroll-step              1)
  (show-paren-mode               t))

(setq display-time-day-and-date t) (display-time) 
(setq-default indent-tabs-mode nil) 

(fset 'yes-or-no-p 'y-or-n-p) 

(setq frame-title-format
  '(:eval
    (if buffer-file-name
        (replace-regexp-in-string
         "\\\\" "/"
         (replace-regexp-in-string
          (regexp-quote (getenv "HOME")) "~"
          (convert-standard-filename buffer-file-name)))
      (buffer-name))))

(add-hook 'python-mode-hook
   (lambda ()
      (setq indent-tabs-mode nil
            tab-width 2
            python-indent 2)))

EOF

## 3 ##################################################
# SILLY: print a ninja, just once (on first load)

if [ "$Splashed" != 1 ] ; then
    Splashed=1
    tput setaf 3 # changes color 
    cat <<-'EOF'
          ___                                                             
         /___\_/                                                          
         |\_/|<\                         Command line ninjas!
         (`o`) `   __(\_            |\_  Attack!                               
         \ ~ /_.-`` _|__)  ( ( ( ( /()/                                   
        _/`-`  _.-``               `\|   
     .-`      (    .-.                                                    
    (   .-     \  /   `-._                                                
     \  (\_    /\/        `-.__-()                                        
      `-|__)__/ /  /``-.   /_____8                                        
            \__/  /     `-`                                               
           />|   /                                                        
          /| J   L                                                        
          `` |   |                                                            
             L___J                                                        
              ( |
             .oO()                                                        
_______________________________________________________
EOF
    tput sgr0 # color back to black
    
fi

## 3 ##################################################
# THINGS TO DO AT START, AT END

# 3a) print name and license

echo "ninja.rc v1.0 (c) 2016 Tim Menzies, MIT (v2) license"
echo

ok() { # 3b) need a place for all the stuff that makes system usable
    dirs;
    ninjarc
    zips
}

dirs() { # 3c) create all the required dirs
    mkdir -p $Safe $Tmp $Raw $Cooked
}
zips() { # make a convenient download 
    (cd ..
     zip -r ninja.zip -u ninja \
	 -x '*.zip' -x '*.DS_Store' -x '.gitignore' \
	 2> /dev/null
    )
}
ninjarc() { # pretties
    if  [ "ninja.rc" -nt "ninjarc.md" ]; then
    (cat <<-'EOF'  
<img align=right height=200 src="http://www.chantetter.nl/it-fun3/go-away.jpg"><img align=right height=200 src="http://www.blogking.biz/wp-content/uploads/Woothemes_Ninjas.jpg">
    
# Ninja.rc

Download:

- This file: [ninja.rc](ninja.rc)
- Entire ninja system [ninja.zip](../ninja.zip)

________

```bash
EOF
     cat ninja.rc
     echo '```' 
    ) > ninjarc.md
    fi 
}

# TIP: 3d) no matter now this program ends, clean on exit

trap zap 0 1 2 3 4 15 # catches normal end, Control-C, Control-D etc
zap() { echo "Zapping..." ; rm -rf $Tmp; }

# TIP: 3e) Define a convenience function to reload environment

reload() { . $Here/ninja.rc ; }
	
## 4 ######################################################
# TIP: useful shell one-liners

# change the prompt to include "NINJA" and the local dirs
here() { cd $1; basename $PWD; }

PROMPT_COMMAND='echo  -ne "NINJA:\033]0; $(here ..)/$(here .)\007"
PS1=" $(here ..)/$(here .) \!> "'

# print to screen
fyi() { echo "$@" 1>&2; } 

# other
alias ls='ls -G'                 ## short format
alias ll='ls -la'                ## long format
alias l.='ls -d .* --color=auto' ## Show hidden files
alias cd..='cd ..' ## get rid of a common 'command not found' error
alias ..='cd ..' # quick change dir command
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias .3='cd ../../../'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'

# git tricks
gitpush() {
    ready
    git status
    git commit -am "saving"
    git push origin master
}
gitpull() {
    ready
    git pull origin master
}
ready() {
    ok
    gitting
}
gitting() {
    git config --global core.editor "`which nano`"
    git config --global credential.helper cache
    git config credential.helper 'cache --timeout=3600'
}

## 5 #####################################################
# TIP: Write little shell scripts for standard actions

killControlM() { tr -d '\015'; } 
downCase()     { tr A-Z a-z; }
stemming()     { perl $Here/stemming.pl  ; }
stops()        {  gawk ' 
       NR==1 {while (getline < Stops)  Stop[$0] = 1;
                                while (getline < Keeps)  Keep[$0] = 1; 
                             }
                            { for(I=1;I<=NF;I++) 
                                  if (Stop[$I] && ! Keep[$I]) $I=" "
                      print $0
                          }' Stops="$Here/stop_words.txt" \
                               Keeps="$Here/keep_words.txt" 
                            }
prep()  { killControlM | downCase | 
                  stemming | stops; }

## 6 ######################################################
# TIP: write convenience functions for learners

# In the following there are 2 kinds of functions: "xx" and "xx10".

# The former needs a train and test set (passed in as $1, $2 and
# used by the "-t $1 and -T $2" flags.

# The latter functions ("xx10") accept one data file $1 which is
# used in a 10-way cross-val by "-t $1".

linearRegression(){
	local learner=weka.classifiers.functions.LinearRegression 
	$Weka $learner -S 0 -R $3 -p 0 -t $1 -T $2
}
bnet(){
        local learner=weka.classifiers.bayes.BayesNet
	$Weka $learner -p 0 -t $1 -T $2 -D \
	    -Q weka.classifiers.bayes.net.search.local.K2 -- -P 2 -S BAYES \
	    -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 
}
bnet10(){
        local learner=weka.classifiers.bayes.BayesNet
	$Weka $learner -i -t $1 -D \
	    -Q weka.classifiers.bayes.net.search.local.K2 -- -P 2 -S BAYES \
	    -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 
}
nb() {
 	local learner=weka.classifiers.bayes.NaiveBayes
	$Weka $learner -p 0 -t $1 -T $2  
}
nb10() {
	local learner=weka.classifiers.bayes.NaiveBayes
	$Weka $learner -i -t $1   
}
j48() {
	local learner=weka.classifiers.trees.J48
	$Weka $learner -p 0 -C 0.25 -M 2 -t $1 -T $2
}
j4810() {
	local learner=weka.classifiers.trees.J48
	$Weka $learner	-C 0.25 -M 2 -i -t $1 
}
zeror() {
        local learner=weka.classifiers.rules.ZeroR
	$Weka $learner -p 0 -t $1 -T $2
}
zeror10() {
        local learner=weka.classifiers.rules.ZeroR
	$Weka $learner -i -t $1
}
oner() {
        local learner=weka.classifiers.rules.OneR
	$Weka $learner -p 0 -t $1 -T $2
}
oner10() {
        local learner=weka.classifiers.rules.OneR
	$Weka $learner -i -t $1
}
rbfnet(){
        local learner=weka.classifiers.functions.RBFNetwork
	$Weka $learner -p 0 -t $1 -T $2 -B 2 -S 1 -R 1.0E-8 -M -1 -W 0.1
}
rbfnet10(){
        local learner=weka.classifiers.functions.RBFNetwork
	$Weka $learner -i -t $1 -B 2 -S 1 -R 1.0E-8 -M -1 -W 0.1
}
ridor() {
       local learner=weka.classifiers.rules.Ridor
	$Weka $learner -F 3 -S 1 -N 2.0 -p 0 -t $1 -T $2 
}
ridor10(){
       local learner=weka.classifiers.rules.Ridor
       $Weka $learner -F 3 -S 1 -N 2.0 -i -t $1
}
adtree() {
       local learner=weka.classifiers.trees.ADTree
       $Weka $learner -B 10 -E -3 -p 0 -t $1 -T $2
}
adtree10() {
       local learner=weka.classifiers.trees.ADTree
       $Weka $learner -B 10 -E -3 -p 0 -i -t $1
}
## 7 ######################################################
# Longer data mining functions

# 7a) just print the actual and predicted values.
wantgot() { gawk '/:/ {
                      split($2,a,/:/); actual    = a[2] 
                      split($3,a,/:/); predicted = a[2]
                      print actual, predicted }'
}

# 7b) print the learer and data set before generating the
#     actual and predicted values
trainTest() {
    local learner=$1
    local train=$2
    local test=$3
    echo "$learner $data"
    $learner $train $test | wantgot
}

# 7c) Know your a,b,c,d s 
abcd() { python3 $Here/abcd.py; }

# 7d) Generate data sets for an m*n cross-val. Call learners on each.
crossval() {
    local m=$1
    local n=$2
    local data=$3
    local r=$4
    shift 4
    local learners=$*
    killControlM < $data |
    gawk 'BEGIN                 { srand('$r') }
          /^.RELATION/,/^.DATA/ { header= header "\n" $0; next } 
          $0                    { Row[NR] = $0 }
          END                   { 
           for(i=1; i<=m; i++)
             for(j=1; j<=n; j++)  {
               arff  = i "_" j ".arff"
               test  = dir "/test"  arff
               train = dir "/train" arff
               print header  >test
               print header  >train
               for(r in Row) { 
                 if (rand() < 1/n) 
                   print(Row[r]) >> test
                 else
                   print(Row[r]) >> train }}}
         ' n=$n m=$m dir=$Tmp 
    echo $Tmp
    cd $Tmp
    for learner in $learners; do
	for((i=1; i<=$m; i++)); do
	    fyi "$learner $i"
	    for((j=1; j<=$n; j++)); do
              local arff="${i}_${j}.arff"		
	      trainTest $learner train$arff test$arff | abcd
	   done
	done
    done
    cd $Here
}


## 8 #####################################################
## any start up actions?
ok

######################################################
# Todo
# #pipe into a while and if
#— tow different pies
#make: don’t redo
#nohup

# pattern
#fetch : curl find mysql
#select: grep sql awk etc
#transform: sort, head, tail, sed, gawk
#learn
#report
#visualize: gnuplot,gvpr
```
