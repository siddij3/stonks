use mydb;
SET @interval_mins = 30;
SET @begin_datetime = '1000-01-01 00:00:00';

select date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t0.date_time) / @interval_mins) * @interval_mins minute), '%Y-%m-%d %H:%i') as t0_date_time,
t0.price,
t1.price as `price - 0.5h`,
t2.price as `price - 1h`,
t3.price as `price - 1.5h`,
t4.price as `price - 2h`,
t5.price as `price - 2.5h`,

-- RSI extensions
t0.rsi,
t1.rsi as `rsi-0.5h`,
t2.rsi as `rsi-1h`,
t3.rsi as `rsi-1.5h`,
t4.rsi as `rsi-2h`,
t5.rsi as `rsi-2.5h`
from quotes as t0

left join quotes as t1 on date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t1.date_time) / @interval_mins) * @interval_mins minute), '%Y-%m-%d %H:%i')
								= date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t0.date_time) / @interval_mins) * @interval_mins - 30 minute), '%Y-%m-%d %H:%i')

left join quotes as t2 on date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t2.date_time) / @interval_mins) * @interval_mins minute), '%Y-%m-%d %H:%i')
								= date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t0.date_time) / @interval_mins) * @interval_mins - 60 minute), '%Y-%m-%d %H:%i')

left join quotes as t3 on date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t3.date_time) / @interval_mins) * @interval_mins minute), '%Y-%m-%d %H:%i')
								= date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t0.date_time) / @interval_mins) * @interval_mins - 90 minute), '%Y-%m-%d %H:%i')

left join quotes as t4 on date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t4.date_time) / @interval_mins) * @interval_mins minute), '%Y-%m-%d %H:%i')
								= date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t0.date_time) / @interval_mins) * @interval_mins - 120 minute), '%Y-%m-%d %H:%i')

left join quotes as t5 on date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t5.date_time) / @interval_mins) * @interval_mins minute), '%Y-%m-%d %H:%i')
								= date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, t0.date_time) / @interval_mins) * @interval_mins - 150 minute), '%Y-%m-%d %H:%i')

order by t0_date_time DESC limit 20;
;



