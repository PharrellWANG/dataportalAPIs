On Fri, Nov 25, 2016 at 11:24 AM, He, Ye <ye.he@livelyimpact.com> wrote:

Dear Pharrel,

Some minor changes and refer to the below:

1. for the Flight Arrival API, please only keep those status contains "At gate" and "("

2. for the Flight Departure API, please only keep those status contains "Dep"

3. redundant DEBUG output from Stock api:

4. for Temperature API, we shall keep 9 items, containing a "Now" record indicating the current hour, e.g., Here "11AM" should be marked as "Now", and please add one more record of "7PM"

5. Temperature API, first letter of "time" and "temperature" should be in upper case

6. Stock API, see if you can change the field name from "Index" to "index" (first letter lower case)

Thank you!