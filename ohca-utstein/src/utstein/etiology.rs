use serde::Serialize;
use sqlx::MySqlPool;

/// The Pathogenesis field
///
/// # Field mappings
///
/// * Medical - `medical` is the number of rows where `pathogenesis` = 0
/// * Trauma - `trauma` is the number of rows where `pathogenesis` = 1
/// * Overdose - `overdose` is the number of rows where `pathogenesis` = 3
/// * Drowning - `drowning` is the number of rows where `pathogenesis` = 2
/// * Electrocution - `electrocution` is the number of rows where `pathogenesis` = 4
/// * Asphyxial - `asphyxial` is the number of rows where `pathogenesis` = 5
/// * Not Recorded - `not_recorded` is the number of rows where `pathogenesis` = -1 or NULL
#[derive(Debug, Serialize)]
pub struct Etiology {
    pub medical: i64,
    pub trauma: i64,
    pub overdose: i64,
    pub drowning: i64,
    pub electrocution: i64,
    pub asphyxial: i64,
    pub not_recorded: i64,
}

impl Etiology {
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Etiology,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 0) AS "medical!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 1) AS "trauma!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 3) AS "overdose!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 2) AS "drowning!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 4) AS "electrocution!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 5) AS "asphyxial!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = -1 or pathogenesis IS NULL) AS "not_recorded!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
