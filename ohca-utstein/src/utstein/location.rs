use serde::Serialize;
use sqlx::MySqlPool;

#[derive(Debug, Serialize)]
pub struct Location {
    pub home: i64,
    pub work: i64,
    pub rec: i64,
    pub public: i64,
    pub educ: i64,
    pub nursing: i64,
    pub other: i64,
    pub unknown: i64,
}
//7 and 6 are switched
impl Location {
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Location,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE location = 0) AS "home!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 1) AS "work!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 2) AS "rec!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 4) AS "public!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 6) AS "educ!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 5) AS "nursing!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 7) AS "other!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = -1 OR location IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
