n = number of users
x = number of conversions
p = probability of conversion = (x / n)
se = standard error of p = sqrt((p * (1 - p)) / n)
z = confidence percentage //Confidence Interval	  85%	1.440   90%  	1.645   95%	  1.960   99%	  2.576




confidence interval = p ± (z * se) //Z for 90% is 1.645

// table of the total number of patients
select 
  count(1) as n, 
  sum(case when converted then 1 else 0 end) as x
from users
group by date_trunc('month', created_at);

//1->Calculate the conversation rate, p.
//2->Using p, calculate the standard error, se.
//3->Compute the low and high confidence intervals.
//4->Include the original p conversion rate as our mid estimate.
select 
  rates.n as users, 
  rates.x as conversions, 
  p - se * z as low, 
  intervals.p as mid, 
  p + se * z as high 
from (
  select 
    rates.*, 
    sqrt(p * (1 - p) / n) as se -- calculate se
  from (
      select conversions.*, 
      x / n::float as p -- calculate p
    from ( 
      -- Our conversion rate table from above
      select 
        count(1) as n, 
        sum(case when converted then 1 else 0 end) as x
      from users
      group by date_trunc('month', created_at);
    ) conversions
  ) rates
) intervals

//if (gotta google ifs in sql) the database is over 100 members then use this other method

select 
  rates.n as users, 
  rates.x as conversions, 
  p - se * z as low, 
  intervals.p as mid, 
  p + se * z as high 
from (
  select 
    rates.*, 
    sqrt(p * (1 - p) / n) as se -- calculate se
  from (
    select 
      conversions.*, 
      (x + z) / (n + z*2)::float as p -- calculate p //adding constants to numerator and denominator to smooth out large and tiny numbers
    from ( 
      -- Our conversion rate table from above
      select 
        count(1) as n, 
        sum(case when converted then 1 else 0 end) as x
      from users
      group by date_trunc('month', created_at);
    ) conversions
  ) rates
) intervals
