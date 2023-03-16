use serde::Serialize;
use sqlx::MySqlPool;

#[derive(Debug, Serialize)]
pub struct HospitalProcess {
    // reperfusion
    pub attempted: i64,

    // targeted temp control
    pub indicated_done: i64,
    pub indicated_not_done: i64,
    pub not_indicated: i64,
    pub unknown: i64,

    // organ donation
    pub organ_donation: i64,
}

impl HospitalProcess {
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            HospitalProcess,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE reperfusionAttempt IS NOT NULL OR reperfusionAttempt != -1) AS "attempted!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm BETWEEN 1 AND 3) AS "indicated_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 4) AS "indicated_not_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 5) AS "not_indicated!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = -1 OR ttm IS NULL) AS "unknown!: i64",
                    (SELECT COUNT(*) FROM cases WHERE organDonation = 1) AS "organ_donation!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap()
    }
}
