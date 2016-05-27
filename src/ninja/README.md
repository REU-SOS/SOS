<img align=right width=500 src="http://www.pentaho.com/sites/default/files/14-067-pentaho-ninja-campaign-v12.jpg">


# Ninja tricks for Data Science

## Install and Test

1. wget https://github.com/REU-SOS/SOS/raw/master/src/ninja.zip
2. unzip ninja.zip
3. cd ninja
4. sh ninja
5. eg2

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
 
By the way, for an explanation of "pd" and "pf" go to [top right, page1](http://menzies.us/07precision.pdf).

## USAGE

```bash
Here=$(pwd) bash --init-file ninja.rc -i
```

TIP: place the above line into a file `ninja` and call with:

```bash
$ sh ninja
```
