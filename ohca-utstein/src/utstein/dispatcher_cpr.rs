use serde::Serialize;
use sqlx::MySqlPool;

/// The Dispatcher CPR (Dispatcher provided CPR instructions) field
///
/// # Field mappings
///
/// * Yes - `yes` is the number of rows where `dispProvidedCPRinst` = 1
/// * No - `no` is the number of rows where `dispProvidedCPRinst` = 0
/// * Unknown - `unknown` is the number of rows where `dispProvidedCPRinst` is -1 or NULL
#[derive(Debug, Serialize)]
pub struct DispatcherCPR {
    pub yes: i64,
    pub no: i64,
    pub unknown: i64,
}

impl DispatcherCPR {
    /// Generates a new DispatcherCPR struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            DispatcherCPR,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE dispProvidedCPRinst = 1) AS "yes!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispProvidedCPRinst = 0) AS "no!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispProvidedCPRinst = -1 OR dispProvidedCprinst IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
