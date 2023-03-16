use serde::Serialize;
use sqlx::MySqlPool;

/// The Resuscitation Attempted field
///
/// # Field mappings
///
/// * count - `count` is the number of rows where `cprEMS` = 1
/// * VT - `vt` is the number of rows where `iniRythm` = 0 or `firstMonitoredRhy` = 1 or 2 or `ecgOptions` contains 22
/// * PEA - `pea` is the number of rows where `firstMonitoredRhy` = 4 or 0 or `iniRythm` = 1 or `echOptions` contains 25
/// * ASYS - `asys` is the number of rows where `firstMonitoredRhy` = 5 or `iniRythm` = 1 or `ecgOptions` contains 24
/// * Brady - `brady` is the number of rows where `firstMonitoredRhy` = 6 or `ecgOptions` contains 2 or 3
/// * AED Non-shockable - `aed_non_shockable` is the number of rows where `firstMonitoredRhy` = 0
/// * AED Shockable - `aed_shockable` is the number of rows where `firstMonitoredRhy` = 1 or `iniRythm` = 0
/// * Not recorded - `not_recorded` is the number of rows where `iniRythm` is NULL
/// * Unknown - `unknown` is the number of rows where `iniRythm` is -1
#[derive(Debug, Serialize)]
pub struct RescAttempted {
    pub count: i64,
    // pub vf: i64, missing?
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
        sqlx::query_as!(
            RescAttempted,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE cprEMS = 1) as "count!: i64",
                    (SELECT COUNT(*) FROM cases 
                        WHERE iniRythm = 0 
                        OR firstMonitoredRhy = 1 
                        OR firstMonitoredRhy = 3
                        OR ecgOptions = 22
                    ) AS "vt!: i64",
                    (SELECT COUNT(*) FROM cases 
                        WHERE firstMonitoredRhy = 4
                        OR iniRythm = 1
                        OR ecgOptions = 25
                        OR firstMonitoredRhy = 0    
                    ) AS "pea!: i64",
                    (SELECT COUNT(*) FROM cases 
                        WHERE firstMonitoredRhy = 5
                        OR iniRythm = 1
                        OR ecgOptions = 24
                    ) AS "asys!: i64",
                    (SELECT COUNT(*) FROM cases 
                        WHERE firstMonitoredRhy = 6
                        OR ecgOptions = 2
                        OR ecgOptions = 3
                    ) AS "brady!: i64",
                    (SELECT COUNT(*) FROM cases WHERE firstMonitoredRhy = 0) AS "aed_non_shockable!: i64",
                    (SELECT COUNT(*) FROM cases WHERE iniRythm = 0 OR firstMonitoredRhy = 1) AS "aed_shockable!: i64",
                    (SELECT COUNT(*) FROM cases WHERE iniRythm IS NULL) AS "not_recorded!: i64",
                    (SELECT COUNT(*) FROM cases WHERE iniRythm = -1) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
