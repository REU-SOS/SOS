<img align=right height=200 src="http://www.chantetter.nl/it-fun3/go-away.jpg"><img align=right height=200 src="http://www.blogking.biz/wp-content/uploads/Woothemes_Ninjas.jpg">


# Ninja tricks for Data Science

Code in any language your like. Divide your work into lots of little bits.
For big bits, write seperate files. For little fiddlely bits, write some
short shell scripts. And to glue it all together, write some ninja code.

The result is a live log of your actual processing, something that it is
useful to you for your day to day work _AND_ lets you package things and
pass them on to someone else.


## Install and Test

In a clean directory on a pathname with no spaces, type:

```
wget https://github.com/REU-SOS/SOS/raw/master/src/ninja.zip
unzip ninja.zip
cd ninja
sh ninja    # to start this tool
eg2         # wait a few minutes while some text dribbles by....
<control-d> # to quit this tool
```

If that works, you should see (in a few minutes), a report looking like this
(note, your numbers may differ due to your local random number generator,
which is a lesson in of itself... don't trust results from anywhere else).

     pd
     rank ,         name ,    med   ,  iqr
     ----------------------------------------------------
        1 ,           nb ,      45  ,    18 (   ------  *  -|---           ),27, 41, 45, 52, 64
        1 ,          j48 ,      47  ,    25 ( -------    *  |---           ),22, 38, 47, 56, 64
        2 ,       rbfnet ,      56  ,    10 (         ----  * -----        ),42, 50, 56, 59, 73
        2 ,         bnet ,      58  ,    17 (       ------  |*   ------    ),37, 50, 58, 67, 81

     pf
     rank ,         name ,    med   ,  iqr
     ----------------------------------------------------
        1 ,           nb ,       8  ,     6 (    --   * ----|-             ), 4,  6,  8, 10, 15
        2 ,       rbfnet ,       9  ,     7 (    ----- *    |-----         ), 4,  8,  9, 14, 19
        2 ,          j48 ,      10  ,    10 (   -----   *   |  ------      ), 3,  7, 10, 16, 21
        2 ,         bnet ,      13  ,     8 (        ---   *|   --         ), 7, 10, 13, 17, 19
      __________________________________________________________
 
By the way, for an explanation of "pd" and "pf" go to [top right, page1](http://menzies.us/pdf/07precision.pdf).

## USAGE

```bash
Here=$(pwd) bash --init-file ninja.rc -i
```

TIP: place the above line into a file `ninja` and call with:

```bash
$ sh ninja
```
