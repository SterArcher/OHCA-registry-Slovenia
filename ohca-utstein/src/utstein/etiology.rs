use serde::Serialize;
use sqlx::MySqlPool;

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
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 1) AS "medical!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 2) AS "trauma!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 3) AS "overdose!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 4) AS "drowning!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 5) AS "electrocution!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 6) AS "asphyxial!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis IS NULL) AS "not_recorded!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
