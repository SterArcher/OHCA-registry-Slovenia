use bigdecimal::ToPrimitive;
use serde::Serialize;
use sqlx::MySqlPool;

/// The EMS Process field
///
/// # Field mappings
///
/// * First Defib Time - `first_defib_time` the average of the `defibTime` column
/// * Indicated Done - `indicated_done` is the number of rows where `ttm` = 1 or 2 or 3
/// * Indicated Not Done - `indicated_not_done` is the number of rows where `ttm` = 4
/// * Not Indicated- `not_indicated` is the number of rows where `ttm` = 5
/// * Unknown - `unknown` is the number of rows where `ttm` = -1 or NULL
/// * Drugs Given - `drugs_given` is the number of rows where `drugs` = 1 or 2 or 4
#[derive(Debug, Serialize)]
pub struct EMSProcess {
    pub first_defib_time: f64,

    // targeted temp control
    pub indicated_done: i64,
    pub indicated_not_done: i64,
    pub not_indicated: i64,
    pub unknown: i64,

    // drugs given
    pub drugs_given: i64,
}

impl EMSProcess {
    pub async fn new(pool: &MySqlPool) -> Self {
        let record =   sqlx::query!(
            r#"
                SELECT
                    (SELECT AVG(defibTime) FROM cases) AS first_defib_time,
                    (SELECT COUNT(*) FROM cases WHERE ttm BETWEEN 1 AND 3) AS "indicated_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 4) AS "indicated_not_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 5) AS "not_indicated!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = -1 OR ttm IS NULL) AS "unknown!: i64",
                    (SELECT COUNT(*) FROM cases WHERE drugs = 1 OR drugs = 2 OR drugs = 4) AS "drugs_given!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap();

        Self {
            first_defib_time: record.first_defib_time.unwrap().to_f64().unwrap(),
            indicated_done: record.indicated_done,
            indicated_not_done: record.indicated_not_done,
            not_indicated: record.not_indicated,
            unknown: record.unknown,
            drugs_given: record.drugs_given,
        }
    }
}
