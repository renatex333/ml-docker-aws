drop table if exists sales_analytics.scoring_ml_renatolf1;

create table sales_analytics.scoring_ml_renatolf1 as
select 
    store_id,
    null as total_sales,
    current_date + i as date_sale
from 
    generate_series(1, 6) as i
cross join 
    (select distinct store_id from sales.item_sale) as stores
order by 
    store_id,
    date_sale;

select
    store_id,
    date_part('year', CAST(date_sale AS DATE)) as year,
    date_part('month', date_sale) as month,
    date_part('day', date_sale) as day,
    date_part('dow', date_sale) as weekday
from
	sales_analytics.scoring_ml_renatolf1
order by
	store_id,
	year,
	month,
	day,
	weekday;
