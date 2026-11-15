# pd.read_sql vs pd.merge

## read_sql (first 10)

```
        category_name                                                                     title  rating  price_gbp
0  Historical Fiction                                   A Flight of Arrows (The Pathfinders #2)       5      55.53
1             Mystery  The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)       5      52.30
2             Mystery                                    A Time of Torment (Charlie Parker #14)       5      48.35
3  Historical Fiction                                                       While You Were Mine       5      41.32
4     Science Fiction                                                                      Join       5      35.67
5  Historical Fiction                                                              The Red Tent       5      35.66
6  Historical Fiction                                                              Mrs. Houdini       5      30.25
7  Historical Fiction                                                     The Passion of Dolssa       5      28.32
8              Travel                                        1,000 Places to See Before You Die       5      26.08
9             Mystery         What Happened on Beale Street (Secrets of the South Mysteries #2)       5      25.37
```

## merge (first 10)

```
        category_name                                                                     title  rating  price_gbp
0  Historical Fiction                                   A Flight of Arrows (The Pathfinders #2)       5      55.53
1             Mystery  The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)       5      52.30
2             Mystery                                    A Time of Torment (Charlie Parker #14)       5      48.35
3  Historical Fiction                                                       While You Were Mine       5      41.32
4     Science Fiction                                                                      Join       5      35.67
5  Historical Fiction                                                              The Red Tent       5      35.66
6  Historical Fiction                                                              Mrs. Houdini       5      30.25
7  Historical Fiction                                                     The Passion of Dolssa       5      28.32
8              Travel                                        1,000 Places to See Before You Die       5      26.08
9             Mystery         What Happened on Beale Street (Secrets of the South Mysteries #2)       5      25.37
```

`assert_frame_equal` passed: both have 32 rows and identical values.
