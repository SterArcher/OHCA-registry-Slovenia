use std::{
    fs::{read_to_string, File},
    io::Write,
};

use handlebars::Handlebars;
use sqlx::MySqlPool;
use utstein::Utstein;

pub mod utils;
pub mod utstein;

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();

    let database_url = std::env::var("DATABASE_URL").unwrap();
    let pool = MySqlPool::connect(&database_url).await.unwrap();

    let utstein = Utstein::new(&pool).await;

    let mut file = File::create("utstein.json").unwrap();
    let serialized = serde_json::to_string_pretty(&utstein).unwrap();
    file.write(serialized.as_bytes()).unwrap();

    let raw_html = read_to_string("index.html").unwrap();

    let reg = Handlebars::new();
    let html = reg.render_template(&raw_html, &utstein).unwrap();

    let mut html_file = File::create("utstein.html").unwrap();
    html_file.write(html.as_bytes()).unwrap();
}
