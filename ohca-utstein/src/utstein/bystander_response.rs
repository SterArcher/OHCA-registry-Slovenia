use serde::Serialize;
use sqlx::MySqlPool;

/// The Bystander Response CPR field
#[derive(Debug, Serialize)]
pub struct BystanderResponse {
    pub bystander_cpr: BystanderCPR,
    pub bystander_aed: BystanderAED,
}

impl BystanderResponse {
    pub async fn new(pool: &MySqlPool) -> Self {
        Self {
            bystander_cpr: BystanderCPR::new(pool).await,
            bystander_aed: BystanderAED::new(pool).await,
        }
    }
}

/// The Bystander Response CPR field
///
/// # Field mappings
///
/// * No Bystander CPR - `no_bcpr` is the number of rows where `bystanderResponse` = 0
/// * Bystander CPR - `bcpr` is the number of rows where `bystanderResponse` = 1 or 2
/// * CC Only - `cc_only` is the number of rows where `bystanderResponse` = 1 or 2
/// * CC Or Vent - `cc_or_vent` is the number of rows where `bystanderResponse` = 2
/// * Unknown -`unknown` is the number of rows where `bystanderResponse` = -1 or NULL
#[derive(Debug, Serialize)]
pub struct BystanderCPR {
    pub no_bcpr: i64,
    pub bcpr: i64,
    pub cc_only: i64,
    pub cc_or_vent: i64,
    pub unknown: i64,
}

impl BystanderCPR {
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            BystanderCPR,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = 0) AS "no_bcpr!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = 1 OR bystanderResponse = 2) AS "bcpr!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = 1 OR bystanderResponse = 2) AS "cc_only!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = 2) AS "cc_or_vent!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = -1 OR bystanderResponse IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

/// The Bystander Response AED field
///
/// # Field mappings
///
/// * Shock - `no_shock` is the number of rows where `bystanderAED` = 1
/// * No Shock CPR - `shock` is the number of rows where `bystanderAED` = 0
/// * Unknown - `unknown` is the number of rows where `bystanderAED` = -1 or NULL
#[derive(Debug, Serialize)]
pub struct BystanderAED {
    pub no_shock: i64,
    pub shock: i64,
    pub unknown: i64,
}

impl BystanderAED {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            BystanderAED,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE bystanderAED = 1) AS "no_shock!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderAED = 0) AS "shock!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderAED = -1 OR bystanderAED IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
