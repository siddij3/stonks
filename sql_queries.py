query_1 = """
select DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s0.date_time) / 30) * 30 minute) as s0_date_time,
s0.dow_io,
s1.dow_io as `dow_io_0.5h`,
s2.dow_io as `dow_io_1h`,
s3.dow_io as `dow_io_1.5h`,
s4.dow_io as `dow_io_2h`,
s5.dow_io as `dow_io_2.5h`

from stock_indexes as s0

left join stock_indexes as s1 on DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s1.date_time) / 30) * 30 minute)
						 		= DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s0.date_time) / 30) * 30 + 30 minute)

left join stock_indexes as s2 on DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s2.date_time) / 30) * 30 minute)
						 		= DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s0.date_time) / 30) * 30 + 60 minute)

left join stock_indexes as s3 on DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s3.date_time) / 30) * 30 minute)
						 		= DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s0.date_time) / 30) * 30 + 90 minute)

left join stock_indexes as s4 on DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s4.date_time) / 30) * 30 minute)
						 		= DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s0.date_time) / 30) * 30 + 120 minute)

left join stock_indexes as s5 on DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s5.date_time) / 30) * 30 minute)
						 		= DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', s0.date_time) / 30) * 30 + 150 minute)

;"""

query_quotes = """
select  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t0.date_time) / 30) * 30 minute) ) as t0_date_time,
t0.price,
t1.price as `price-0.5h`,
t2.price as `price-1h`,
t3.price as `price-1.5h`,
t4.price as `price-2h`,
t5.price as `price-2.5h`,

-- RSI extensions
t0.rsi,
t1.rsi as `rsi-0.5h`,
t2.rsi as `rsi-1h`,
t3.rsi as `rsi-1.5h`,
t4.rsi as `rsi-2h`,
t5.rsi as `rsi-2.5h`
from quotes as t0

left join quotes as t1 on  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t1.date_time) / 30) * 30 minute) )
								=  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t0.date_time) / 30) * 30 - 30 minute) )

left join quotes as t2 on  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t2.date_time) / 30) * 30 minute) )
								=  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t0.date_time) / 30) * 30 - 60 minute) )

left join quotes as t3 on  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t3.date_time) / 30) * 30 minute) )
								=  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t0.date_time) / 30) * 30 - 90 minute) )

left join quotes as t4 on  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t4.date_time) / 30) * 30 minute) )
								=  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t0.date_time) / 30) * 30 - 120 minute) )

left join quotes as t5 on  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t5.date_time) / 30) * 30 minute) )
								=  (DATE_ADD('1000-01-01 00:00:00', Interval FLOOR(TIMESTAMPDIFF(MINUTE, '1000-01-01 00:00:00', t0.date_time) / 30) * 30 - 150 minute) )

;





"""