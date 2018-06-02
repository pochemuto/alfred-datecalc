Alfred Date Calc
================

**Roadmap**

-  number expressions ☑️
    
    ```
    (1 + 3) * 4 => 13
    ```

- simple unit support ☑️

    ```
    1 day + 5 minutes / 2 => minute(1442.5)
    ```

- unit convert ☑️

    ```
    (5 days) week => week(0.714285714286)
    ```

- number formatting ☑️

    ```
    22/7, #.#### => 3.1429
    4/5, 0.0000 => 0.8000
    ```

- complex unit ☑️

    ```
    1 month + 14 days => duration(month(1), week(2))
    ```

- date calculation

    ```
    now + 1 month => date(2018-02-12 12:23:36)
    ```

- date input

    ```
    7 may => date(2018-05-07 12:23:36)
    7 may 1987 => date(1987-05-07 12:23:36)
    1959-12-35 => date(1959-12-35 12:23:36)
    ```

- constants

    ```
    now => date(2018-01-12 12:23:36)
    yesterday => date(2018-01-11 12:23:36)
    today - tomorrow => day(-1)
    ```

- date format

    ```
    tomorrow, timestamp => 1527952314
    now, day of week => day_of_week(tuesday)
    ```

