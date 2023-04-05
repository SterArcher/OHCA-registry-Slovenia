use std::fs::File;
use std::io::Write;
use std::net::SocketAddr;

use anyhow::Result;
use clap::{Parser, Subcommand, ValueEnum};
use dialoguer::theme::ColorfulTheme;
use dialoguer::Password;
use handlebars::Handlebars;
use sqlx::MySqlPool;
use utstein::Utstein;

pub mod utils;
pub mod utstein;

#[derive(Parser)]
#[command(
    version,
    about,
    long_about = "You can pass either the 'user', 'db' and 'host' parameters and get prompted for the password, or pass in the entire connection string using the 'c' parameter"
)]
struct Cli {
    #[arg(value_enum, default_value_t=Output::Json)]
    output: Output,

    #[arg(short = 'o')]
    output_filename: Option<String>,

    #[command(subcommand)]
    connection: ConnectionCommands,
}

#[derive(Subcommand)]
enum ConnectionCommands {
    #[command(arg_required_else_help = true)]
    Credentials {
        /// The database user
        #[arg(long, short = 'u')]
        user: String,

        /// The database name
        #[arg(long, short = 'd')]
        db: String,

        /// Host:port address of the database ie. '192.168.1.2:3306'
        #[arg(long, short = 'i')]
        host: SocketAddr,
    },
    #[command(arg_required_else_help = true)]
    Connect {
        /// A connection string formatted to 'mysql://{user}:{password}@{host}:{port}/{db}'
        #[arg(long, short = 'c')]
        connection_string: String,
    },
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Output {
    /// Outputs the report in a HTML file format with the necesarry CSS styling imbedded
    Html,

    /// Outputs the report in a machine readable JSON format
    Json,
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    let connection_string = match cli.connection {
        ConnectionCommands::Credentials { user, db, host } => {
            let password = Password::with_theme(&ColorfulTheme::default())
                .with_prompt("Database password")
                .interact()?;

            format!("mysql://{user}:{password}@{host}/{db}")
        }
        ConnectionCommands::Connect { connection_string } => connection_string,
    };

    let pool = MySqlPool::connect(&connection_string).await?;

    println!("Successfully connected to the database. Running queries...");

    let utstein = Utstein::new(&pool).await;

    println!("Queries ran successfully. Outputting to the selected format...");

    match cli.output {
        Output::Json => {
            let filename = cli.output_filename.unwrap_or("utstein.json".into());
            let mut file = File::create(filename)?;
            let serialized = serde_json::to_string_pretty(&utstein)?;
            file.write(serialized.as_bytes())?;
        }
        Output::Html => {
            let raw_html = include_str!("index.html");
            let reg = Handlebars::new();
            let html = reg.render_template(&raw_html, &utstein)?;

            let filename = cli.output_filename.unwrap_or("utstein.html".into());
            let mut html_file = File::create(filename)?;
            html_file.write(html.as_bytes())?;
        }
    }

    println!("Outputting successfull. Exiting");

    Ok(())
}
