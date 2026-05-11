with base as (
    select
        date,
        ticker,
        close_price
    from {{ ref('stg_prices') }}
),

metrics as (
    select
        date,
        ticker,
        close_price,

        round(avg(close_price) over (
            partition by ticker
            order by date
            rows between 6 preceding and current row
        ), 2) as ma_7d,

        round(avg(close_price) over (
            partition by ticker
            order by date
            rows between 29 preceding and current row
        ), 2) as ma_30d,

        round(
            (close_price - lag(close_price) over (partition by ticker order by date))
            / lag(close_price) over (partition by ticker order by date) * 100
        , 2) as pct_change_daily

    from base
)

select * from metrics
