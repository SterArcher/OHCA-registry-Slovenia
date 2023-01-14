use std::{fs::File, io::Write};

use sqlx::MySqlPool;

mod confidence_intervals;
mod types;
//mod Confidence_Intervals;

use types::Utstein;

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();

    let database_url = std::env::var("DATABASE_URL").unwrap();

    let pool = MySqlPool::connect(&database_url).await.unwrap();

    let utstein = Utstein::new(&pool).await;

    let mut file = File::create("utstein.json").unwrap();
    let serialized = serde_json::to_string_pretty(&utstein).unwrap();
    file.write(serialized.as_bytes()).unwrap();

    // let mut writer = csv::Writer::from_path("utstein.csv").unwrap();
    // writer.serialize(&utstein).unwrap();
    // writer.flush().unwrap();

    // println!("{:#?}", utstein);
}
