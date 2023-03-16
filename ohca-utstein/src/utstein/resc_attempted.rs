use serde::Serialize;
use sqlx::MySqlPool;

/// The Resuscitation Attempted field
///
/// Filters all the cases, with the following filters:
///
/// * `bystanedResponse` is 1 or 2,
/// * or `bystanderAED` is 1 or 2,
/// * or `mechanicalCPR` is 1, 2 or 3.
///
/// # Field mappings
///
/// * VF - `vf` is the number of rows where `firstMonitoredRhy` = 1
/// * VT - `vt` is the number of rows where `firstMonitoredRhy` = 2
/// * PEA - `pea` is the number of rows where `firstMonitoredRhy` = 3
/// * ASYS - `asys` is the number of rows where `firstMonitoredRhy` = 4
/// * Brady - `brady` is the number of rows where `firstMonitoredRhy` = 5
/// * AED Non-shockable - `aed_non_shockable` is the number of rows where `firstMonitoredRhy` = 6
/// * AED Shockable - `aed_shockable` is the number of rows where `firstMonitoredRhy` = 7
/// * Not recorded - `not_recorded` is the number of rows where `firstMonitoredRhy` is NULL
/// * Unknown - `unknown` is the number of rows where `firstMonitoredRhy` is -1
#[derive(Debug, Serialize)]
pub struct RescAttempted {
    pub vf: i64,
    pub vt: i64,
    pub pea: i64,
    pub asys: i64,
    pub brady: i64,
    pub aed_non_shockable: i64,
    pub aed_shockable: i64,
    pub not_recorded: i64,
    pub unknown: i64,
}

impl RescAttempted {
    /// Generates a new RescAttempted struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    pub async fn new(pool: &MySqlPool) -> Self {
        // Query with a common table expression - CTE
        // Read more at https://mariadb.com/kb/en/with/

        // First create a temporary table, where the only columns is `firstMonitorRhy`
        // Then get results from that table according to the required filter
        sqlx::query_as!(
            RescAttempted,
            r#"
                WITH rescucitaion AS 
                (
                    SELECT
                        firstMonitoredRhy
                    FROM cases
                    WHERE bystanderResponse BETWEEN 1 AND 2
                    OR bystanderAED BETWEEN 1 AND 2
                    OR mechanicalCPR BETWEEN 1 AND 3
                )
                SELECT
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 1) AS "vf!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 2) AS "vt!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 3) AS "pea!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 4) AS "asys!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 5) AS "brady!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 6) AS "aed_non_shockable!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 7) AS "aed_shockable!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy IS NULL) AS "not_recorded!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = -1) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
