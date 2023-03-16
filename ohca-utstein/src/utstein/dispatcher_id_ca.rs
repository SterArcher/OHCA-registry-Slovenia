use serde::Serialize;
use sqlx::MySqlPool;

/// The Dispatcher ID CA (Dispatcher Identified Cardiac Arrests) field
///
/// # Field mappings
///
/// * Yes - `yes` is the number of rows where `dispIdentifiedCA` = 1
/// * No - `no` is the number of rows where `dispIdentifiedCA` = 0
/// * Unknown - `unknown` is the number of rows where `dispIdentifiedCA` is -1 or NULL
#[derive(Debug, Serialize)]
pub struct DispatcherIdCA {
    pub yes: i64,
    pub no: i64,
    pub unknown: i64,
}

impl DispatcherIdCA {
    /// Generates a new DispatcherIdCA struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    pub async fn new(pool: &MySqlPool) -> Self {
        // using the `sqlx::query_as!` you can specify what the output type the query should return
        // so we don't need to do any explicit mapping of the columns
        sqlx::query_as!(
            DispatcherIdCA,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE dispIdentifiedCA = 1) AS "yes!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispIdentifiedCA = 0) AS "no!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispIdentifiedCA = -1 OR dispProvidedCprinst IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
