# SQL query results

## Q1 SELECT / WHERE - cheap books in stock

```sql
SELECT title, price_gbp FROM books WHERE in_stock = 1 AND price_gbp < 20
```

Rows returned: 16

```
                                                                          title  price_gbp
                                                           In a Dark, Dark Wood      19.63
                                                               A Murder in Time      16.64
                                         That Darkness (Gardiner and Renner #1)      13.92
                                           Tastes Like Fear (DI Marnie Rome #3)      10.69
                                        A Study in Scarlet (Sherlock Holmes #1)      16.73
                                                     Hide Away (Eve Duncan #20)      11.84
                                                              Playing with Fire      13.71
                                      The Cuckoo's Calling (Cormoran Strike #1)      19.21
                                                              The Girl You Lost      12.29
                                      The Girl In The Ice (DCI Erika Foster #1)      15.85
                                                                    Lilac Girls      17.28
                                     The Constant Princess (The Tudor Court #1)      16.62
                              A Spy's Devotion (The Regency Spies of London #1)      16.97
                                                                    The Project      10.65
The Restaurant at the End of the Universe (Hitchhiker's Guide to the Galaxy #2)      10.92
                                                               Ready Player One      19.07
```

## Q2 ORDER BY + LIMIT - 10 most expensive books

```sql
SELECT title, price_gbp, price_inr FROM books ORDER BY price_gbp DESC LIMIT 10
```

Rows returned: 10

```
                                                                 title  price_gbp  price_inr
                                         Boar Island (Anna Pigeon #19)      59.48    6275.14
The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70    6087.35
                                      A Year in Provence (Provence #1)      56.88    6000.84
                                                   The Past Never Ends      56.50    5960.75
                                      The Last Painting of Sara de Vos      55.55    5860.52
                               A Flight of Arrows (The Pathfinders #2)      55.53    5858.42
                                                        Dune (Dune #1)      54.86    5787.73
                 Murder at the 42nd Street Library (Raymond Ambler #1)      54.36    5734.98
                                        The Last Mile (Amos Decker #2)      54.21    5719.16
                                   1st to Die (Women's Murder Club #1)      53.98    5694.89
```

## Q3 DISTINCT - rating values present

```sql
SELECT DISTINCT rating FROM books ORDER BY rating
```

Rows returned: 5

```
 rating
      1
      2
      3
      4
      5
```

## Q4 IN - books rated 4 or 5

```sql
SELECT title, rating FROM books WHERE rating IN (4, 5) ORDER BY rating DESC, title
```

Rows returned: 32

```
                                                                                   title  rating
                                                      1,000 Places to See Before You Die       5
                                                 A Flight of Arrows (The Pathfinders #2)       5
                                       A Spy's Devotion (The Regency Spies of London #1)       5
                                                  A Time of Torment (Charlie Parker #14)       5
                                                                  Between Shades of Gray       5
                                                                                    Join       5
                                                                            Mrs. Houdini       5
                The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)       5
                                                                       The Girl You Lost       5
                                                                   The Passion of Dolssa       5
                                                                            The Red Tent       5
                                                       The Silkworm (Cormoran Strike #2)       5
                                                                  Voyager (Outlander #3)       5
                       What Happened on Beale Street (Secrets of the South Mysteries #2)       5
                                                                     While You Were Mine       5
                                                                       A Paris Apartment       4
                                                        A Year in Provence (Provence #1)       4
                                                                                   Arena       4
                                        Delivering the Truth (Quaker Midwife Mystery #1)       4
                        Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond       4
                                Having the Barbarian's Baby (Ice Planet Barbarians #7.5)       4
                                                                   Lost Among the Living       4
                                   Murder at the 42nd Street Library (Raymond Ambler #1)       4
                                                                        Ready Player One       4
                                                                           Sharp Objects       4
                                                               The Marriage of Opposites       4
                                         The Murder of Roger Ackroyd (Hercule Poirot #4)       4
                                     The Mysterious Affair at Styles (Hercule Poirot #1)       4
                  The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)       4
                                                                     The Past Never Ends       4
William Shakespeare's Star Wars: Verily, A New Hope (William Shakespeare's Star Wars #4)       4
                                         World Without End (The Pillars of the Earth #2)       4
```

## Q5 BETWEEN - mid-priced books (GBP 10 to 20)

```sql
SELECT title, price_gbp FROM books WHERE price_gbp BETWEEN 10 AND 20 ORDER BY price_gbp
```

Rows returned: 16

```
                                                                          title  price_gbp
                                                                    The Project      10.65
                                           Tastes Like Fear (DI Marnie Rome #3)      10.69
The Restaurant at the End of the Universe (Hitchhiker's Guide to the Galaxy #2)      10.92
                                                     Hide Away (Eve Duncan #20)      11.84
                                                              The Girl You Lost      12.29
                                                              Playing with Fire      13.71
                                         That Darkness (Gardiner and Renner #1)      13.92
                                      The Girl In The Ice (DCI Erika Foster #1)      15.85
                                     The Constant Princess (The Tudor Court #1)      16.62
                                                               A Murder in Time      16.64
                                        A Study in Scarlet (Sherlock Holmes #1)      16.73
                              A Spy's Devotion (The Regency Spies of London #1)      16.97
                                                                    Lilac Girls      17.28
                                                               Ready Player One      19.07
                                      The Cuckoo's Calling (Cormoran Strike #1)      19.21
                                                           In a Dark, Dark Wood      19.63
```

## Q6 JOIN + GROUP BY - stats per category

```sql
SELECT c.category_name, COUNT(*) AS n_books,
                  ROUND(AVG(b.price_gbp), 2) AS avg_price_gbp,
                  ROUND(AVG(b.rating), 2) AS avg_rating
           FROM books b JOIN categories c ON b.category_id = c.category_id
           GROUP BY c.category_name ORDER BY n_books DESC
```

Rows returned: 4

```
     category_name  n_books  avg_price_gbp  avg_rating
           Mystery       32          31.72        2.94
Historical Fiction       26          33.64        3.23
   Science Fiction       16          33.80        2.25
            Travel       11          39.79        2.73
```

## Q7 JOIN + window function - top 10 rated books per category

```sql
SELECT category_name, title, rating, price_gbp FROM (
               SELECT c.category_name, b.title, b.rating, b.price_gbp,
                      ROW_NUMBER() OVER (PARTITION BY c.category_name
                                         ORDER BY b.rating DESC, b.title) AS rn
               FROM books b JOIN categories c ON b.category_id = c.category_id
           ) WHERE rn <= 10 ORDER BY category_name, rn
```

Rows returned: 40

```
     category_name                                                                                    title  rating  price_gbp
Historical Fiction                                                  A Flight of Arrows (The Pathfinders #2)       5      55.53
Historical Fiction                                        A Spy's Devotion (The Regency Spies of London #1)       5      16.97
Historical Fiction                                                                   Between Shades of Gray       5      20.79
Historical Fiction                                                                             Mrs. Houdini       5      30.25
Historical Fiction                                                                    The Passion of Dolssa       5      28.32
Historical Fiction                                                                             The Red Tent       5      35.66
Historical Fiction                                                                   Voyager (Outlander #3)       5      21.07
Historical Fiction                                                                      While You Were Mine       5      41.32
Historical Fiction                                                                        A Paris Apartment       4      39.01
Historical Fiction                                                                    Lost Among the Living       4      27.70
           Mystery                                                   A Time of Torment (Charlie Parker #14)       5      48.35
           Mystery                 The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)       5      52.30
           Mystery                                                                        The Girl You Lost       5      12.29
           Mystery                                                        The Silkworm (Cormoran Strike #2)       5      23.05
           Mystery                        What Happened on Beale Street (Secrets of the South Mysteries #2)       5      25.37
           Mystery                                         Delivering the Truth (Quaker Midwife Mystery #1)       4      20.89
           Mystery                                    Murder at the 42nd Street Library (Raymond Ambler #1)       4      54.36
           Mystery                                                                            Sharp Objects       4      47.82
           Mystery                                          The Murder of Roger Ackroyd (Hercule Poirot #4)       4      44.10
           Mystery                                      The Mysterious Affair at Styles (Hercule Poirot #1)       4      24.80
   Science Fiction                                                                                     Join       5      35.67
   Science Fiction                                                                                    Arena       4      21.36
   Science Fiction                                 Having the Barbarian's Baby (Ice Planet Barbarians #7.5)       4      34.96
   Science Fiction                                                                         Ready Player One       4      19.07
   Science Fiction William Shakespeare's Star Wars: Verily, A New Hope (William Shakespeare's Star Wars #4)       4      43.30
   Science Fiction                  Life, the Universe and Everything (Hitchhiker's Guide to the Galaxy #3)       2      33.26
   Science Fiction                                                                          Soft Apocalypse       2      26.12
   Science Fiction                                                  The Last Girl (The Dominion Trilogy #1)       2      36.26
   Science Fiction                                              Three Wishes (River of Time: California #1)       2      44.18
   Science Fiction                                   Do Androids Dream of Electric Sheep? (Blade Runner #1)       1      51.48
            Travel                                                       1,000 Places to See Before You Die       5      26.08
            Travel                                                         A Year in Provence (Provence #1)       4      56.88
            Travel                         Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond       4      49.43
            Travel                                                Neither Here nor There: Travels in Europe       3      38.95
            Travel                       See America: A Celebration of Our National Parks & Treasured Sites       3      48.87
            Travel                                                                     Under the Tuscan Sun       3      37.33
            Travel                                                                       A Summer In Europe       2      44.34
            Travel                                                                  It's Only the Himalayas       2      45.17
            Travel                      Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel       2      36.94
            Travel                                                                 The Great Railway Bazaar       1      30.54
```
