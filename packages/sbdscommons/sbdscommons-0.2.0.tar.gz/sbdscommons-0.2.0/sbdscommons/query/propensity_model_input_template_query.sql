-- QUERY for the model input
-- Getting the transactions
WITH transaction_table_step1 AS
	(SELECT
	    sor.customer_id_hash,
	    sor.product_group_id_hash,
	    DATE_TRUNC('day', sor.created) AS timestamp_day,
	    DATE_DIFF('days', c.created, TO_DATE('{reference_date}', 'YYYY-MM-DD')) AS nr_days_as_customer,
	    SUM(sor.quantity * p.stats_cans) AS nr_cans,
	    SUM(sor.quantity * sor.out_price_inc_vat) AS amount_spent_incl_vat,
	    DATE_DIFF('days', DATE_TRUNC('day', sor.created), TO_DATE('{reference_date}', 'YYYY-MM-DD')) AS days_since
	FROM view.sales_order_row sor
	INNER JOIN view.product p ON p.product_id_hash = sor.product_id_hash
	INNER JOIN view.customer c ON c.customer_id_hash = sor.customer_id_hash
	WHERE sor.site_name = 'Snusbolaget.se'
	    AND p.category = 'SNUS'
	    AND sor.product_type = '10'
	    AND NOT p.is_sample_product
	GROUP BY
	    sor.customer_id_hash,
	    sor.product_group_id_hash,
	    DATE_TRUNC('day', sor.created),
	    DATE_DIFF('days', c.created, TO_DATE('{reference_date}', 'YYYY-MM-DD'))
	)
, transaction_table_step2 AS
	(SELECT
		    tt1.customer_id_hash,
		    tt1.product_group_id_hash,
		    tt1.timestamp_day,
		    tt1.nr_days_as_customer,
		    tt1.nr_cans,
		    tt1.amount_spent_incl_vat,
		    tt1.days_since,
			MIN(tt1.days_since) OVER(PARTITION BY tt1.customer_id_hash) AS latest_purchase_days_since,
			tt1.days_since - (MIN(tt1.days_since) OVER(PARTITION BY tt1.customer_id_hash)) AS days_before_last_purchase
	FROM transaction_table_step1 tt1
	)
, selected_transactions AS
	(SELECT t.customer_id_hash, t.product_group_id_hash
		, SUM(t.amount_spent_incl_vat) AS amount_spent_incl_vat
		, SUM(t.nr_cans) AS nr_cans
	FROM transaction_table_step2 t
	WHERE t.days_before_last_purchase BETWEEN {min_days_since} AND {max_days_since}
		AND t.nr_days_as_customer >= {nr_days_as_customer}
	GROUP BY customer_id_hash, product_group_id_hash
	)
-- Adding cookie data
, cookie_data AS
	(SELECT
	    so.customer_id_hash,
	    spv.product_group_id_hash,
	    DATE(spv.timestamp) as date,
	    COUNT(DISTINCT spv.timestamp) AS webclick_count,
	    DATE_DIFF('days', DATE(spv.timestamp), TO_DATE('{reference_date}', 'YYYY-MM-DD')) AS days_since
	FROM "view".session_product_view spv
	LEFT JOIN "view".session s ON s.user_session_id_hash = spv.user_session_id_hash
	LEFT JOIN "view".sales_order so ON so.order_id_hash = s.order_id_hash
	WHERE so.customer_id_hash IS NOT NULL
	GROUP BY
	    so.customer_id_hash,
	    spv.product_group_id_hash,
	    days_since,
	    date
	 )
, selected_cookie_data AS
	(SELECT cd.customer_id_hash, cd.product_group_id_hash
		, SUM(cd.webclick_count) as webclick_count
	FROM cookie_data cd
	WHERE cd.days_since BETWEEN {min_days_since} AND {max_days_since}
	GROUP BY cd.customer_id_hash, cd.product_group_id_hash
	)
, trans_click as
	(SELECT st.*
		, scd.webclick_count
	FROM selected_transactions st
	LEFT JOIN selected_cookie_data scd
	ON st.customer_id_hash = scd.customer_id_hash
		AND st.product_group_id_hash = scd.product_group_id_hash
	)
, segments AS
    (SELECT c.customer_id_hash
        -- Assigning NULL segments to the biggest segments
        , COALESCE(c.segment, 'DIY_male_brand_loyalist') AS segment
    FROM "view".customer c
    )
SELECT tc.*
	, seg.segment
FROM trans_click tc
LEFT JOIN segments seg
ON tc.customer_id_hash = seg.customer_id_hash
