create or replace view sales_analytics.view_abt_train_renatolf1 as
	select
	    store_id,
	    SUM(price) as total_sales,
	    date_part('year', CAST(date_sale AS DATE)) as year,
	    date_part('month', date_sale) as month,
	    date_part('day', date_sale) as day,
	    date_part('dow', date_sale) as weekday
	from
		sales.item_sale
	where 
		date_sale < current_date - 1
	group by
		date_sale,
		store_id
	order by
		store_id,
		year,
		month,
		day,
		weekday;
