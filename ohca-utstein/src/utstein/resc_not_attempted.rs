use serde::Serialize;
use sqlx::MySqlPool;

/// The Resuscitation Not Attempted field
///
/// # Field mappings
///
/// * Count - `count` is the number of rows where `CPRdone` = 0
/// * DNAR (Did not attempt resuscitation) - `dnar` is the number of rows where `noCPR` = 4 from the `cases` table
/// * Obviously dead - `obviously_dead` is the number of rows where `noCPR` = 5 from the `cases` table
/// * Signs of Life - `signs_of_life` is the sum of the column `casesCirculation` and `casesFutile` from the `systems` table
#[derive(Debug, Serialize)]
pub struct RescNotAttempted {
    pub count: i64,
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
                    (SELECT COUNT(*) FROM cases WHERE CPRdone = 0) AS "count!: i64",
                    (SELECT COUNT(*) FROM cases WHERE noCPR = 4) AS "dnar!: i64",
                    (SELECT COUNT(*) FROM cases WHERE noCPR = 5) AS "obviously_dead!: i64",
                    (SELECT SUM(casesCirculation) + SUM(casesFutile) FROM systems) AS "signs_of_life!: i64"
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
