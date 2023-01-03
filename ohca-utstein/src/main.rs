use std::time::Duration;

use sqlx::mysql::MySqlPoolOptions;
use sqlx::MySqlPool;

//mod confidence_intervals;
mod types;
mod util;

#[tokio::main]
async fn main() {
    dotenv::dotenv().ok();

    let database_url = std::env::var("DATABASE_URL").unwrap();

    let pool = MySqlPoolOptions::new()
        .max_connections(1)
        .acquire_timeout(Duration::from_secs(10))
        .connect(&database_url)
        .await
        .unwrap();

    let cases = get_cases(&pool).await;

    println!("{cases}");
}

async fn get_cases(pool: &MySqlPool) -> String {
    let cases = sqlx::query!(r#"SELECT * FROM cases"#)
        .fetch_all(pool)
        .await
        .unwrap();

    dbg!(&cases[0]);

    "".into()
}
