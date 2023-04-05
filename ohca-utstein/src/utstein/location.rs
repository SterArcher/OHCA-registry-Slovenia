use serde::Serialize;
use sqlx::MySqlPool;

/// The Location field
///
/// # Field mappings
///
/// * Home - `home` is the number of rows where `location` = 0
/// * Work - `work` is the number of rows where `location` = 1
/// * Recreation - `rec` is the number of rows where `location` = 2
/// * Public -  `public` is the number of rows where `location` = 4
/// * Education -  `educ` is the number of rows where `location` = 6
/// * Nursing -  `nursing` is the number of rows where `location` = 5
/// * Street - `street` is the number of rows where `location` = 3
/// * Other -  `other` is the number of rows where `location` = 7
/// * Unknown - `unknown` is the number of rows where `iniRythm` is -1 or NULL
#[derive(Debug, Serialize)]
pub struct Location {
    pub home: i64,
    pub work: i64,
    pub rec: i64,
    pub public: i64,
    pub educ: i64,
    pub nursing: i64,
    pub street: i64,
    pub other: i64,
    pub unknown: i64,
}

impl Location {
    /// Generates a new RescAttempted struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
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
                    (SELECT COUNT(*) FROM cases WHERE location = 3) AS "street!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 7) AS "other!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = -1 OR location IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
