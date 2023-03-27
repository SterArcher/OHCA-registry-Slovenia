use std::fs::{read_to_string, File};
use std::io::Write;

use anyhow::Result;
use handlebars::Handlebars;
use sqlx::MySqlPool;
use utstein::Utstein;

pub mod utils;
pub mod utstein;

#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv().ok();

    let database_url = std::env::var("DATABASE_URL")?;
    let pool = MySqlPool::connect(&database_url).await?;

    let utstein = Utstein::new(&pool).await;

    let mut file = File::create("utstein.json")?;
    let serialized = serde_json::to_string_pretty(&utstein)?;
    file.write(serialized.as_bytes())?;

    let raw_html = read_to_string("index.html").unwrap();

    let reg = Handlebars::new();
    let html = reg.render_template(&raw_html, &utstein).unwrap();
    let mut html_file = File::create("utstein.html").unwrap();
    html_file.write(html.as_bytes()).unwrap();

    Ok(())
}
