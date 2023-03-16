use serde::Serialize;
use sqlx::MySqlPool;

/// The Resuscitation Not Attempted field
///
/// # Field mappings
///
/// * All Cases - `all_cases` is the difference of the sum of the columns `attendedCAs` and `attemptedResusc` from the `systems` table
/// * DNAR (Did not attempt resuscitation) - `dnar` is the sum of the column `casesDNR` from the `systems` table
/// * Obviously dead - `obviously_dead` is the number of rows where `deadOnArrival` = 1 from the `cases` table
/// * Signs of Life - `signs_of_life` is the sum of the column `casesCirculation` from the `systems` table
#[derive(Debug, Serialize)]
pub struct RescNotAttempted {
    pub all_cases: i64,
    pub dnar: i64,
    pub obviously_dead: i64,
    pub signs_of_life: i64,
}

impl RescNotAttempted {
    /// Generates a new RescNotAttempted struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            RescNotAttempted,
            r#"
                SELECT
                    (SELECT SUM(attendedCAs) - SUM(attemptedResusc) FROM systems) AS "all_cases!: i64",
                    (SELECT SUM(casesDNR) FROM systems) AS "dnar!: i64",
                    (SELECT COUNT(*) FROM cases WHERE deadOnArrival = 1) AS "obviously_dead!: i64",
                    (SELECT SUM(casesCirculation) FROM systems) AS "signs_of_life!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()

        // Self {
        //     all_cases: record.all_cases.unwrap().to_i64().unwrap(),
        //     dnar: record.dnar.unwrap().to_i64().unwrap(),
        //     obviously_dead: record.obviously_dead.unwrap().to_i64().unwrap(),
        //     signs_of_life: record.signs_of_life.unwrap().to_i64().unwrap(),
        // }
    }
}
