with source as (
    select
        date,
        ticker,
        round(close_price, 2) as close_price,
        ingested_at
    from raw_prices
)

select * from source
